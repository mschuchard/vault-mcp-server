"""test mcp response caching middleware"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock

import mcp.types
import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import MiddlewareContext

from vault_mcp_server.mcp_bindings import cache
from vault_mcp_server.vault.sys import namespace


@pytest.fixture
def vault_client() -> SimpleNamespace:
    # stands in for the hvac client, whose adapter holds the active namespace
    return SimpleNamespace(adapter=SimpleNamespace(namespace=None))


@pytest.fixture
def vault_data() -> dict[str | None, str]:
    # stands in for the vault state of each namespace
    return {None: 'root-devices', 'team-a': 'team-a-devices'}


@pytest.fixture
def server_under_test(vault_client: SimpleNamespace, vault_data: dict[str | None, str]) -> FastMCP:
    @asynccontextmanager
    async def lifespan(server: FastMCP) -> AsyncGenerator[dict]:
        yield {'client': vault_client}

    server: FastMCP = FastMCP(name='cache-test', lifespan=lifespan)
    server.add_middleware(cache.VaultResponseCachingMiddleware(read_resource_settings={'ttl': 60}))

    @server.resource('test://devices')
    def read_devices() -> str:
        return vault_data[vault_client.adapter.namespace]

    @server.tool(name='devices-enable')
    def enable_device() -> None:
        vault_data[vault_client.adapter.namespace] = 'enabled-devices'

    @server.tool(name='devices-enable-failing')
    def enable_device_failing() -> None:
        vault_data[vault_client.adapter.namespace] = 'enabled-devices'
        raise RuntimeError('failed after the mutation was applied')

    # the real tool function is registered, so the in-place mutation of the shared adapter is exercised
    server.tool(name_or_fn=namespace.switch, name='namespace-switch')
    return server


@pytest.mark.asyncio
async def test_resource_read_cached_without_tool_call(server_under_test: FastMCP, vault_data: dict[str | None, str]) -> None:
    async with Client(server_under_test) as client:
        first_read = await client.read_resource('test://devices')
        # a change made outside of this server is only visible once the ttl expires
        vault_data[None] = 'out-of-band-devices'
        second_read = await client.read_resource('test://devices')

    assert first_read[0].text == 'root-devices'
    assert second_read[0].text == 'root-devices'


@pytest.mark.asyncio
async def test_tool_call_discards_cached_reads(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        first_read = await client.read_resource('test://devices')
        await client.call_tool(name='devices-enable')
        second_read = await client.read_resource('test://devices')

    assert first_read[0].text == 'root-devices'
    assert second_read[0].text == 'enabled-devices'


@pytest.mark.asyncio
async def test_failed_tool_call_discards_cached_reads(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        first_read = await client.read_resource('test://devices')
        with pytest.raises(ToolError):
            await client.call_tool(name='devices-enable-failing')
        second_read = await client.read_resource('test://devices')

    assert first_read[0].text == 'root-devices'
    assert second_read[0].text == 'enabled-devices'


@pytest.mark.asyncio
async def test_namespace_switch_tool(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        root_read = await client.read_resource('test://devices')
        await client.call_tool(name='namespace-switch', arguments={'namespace': 'team-a'})
        team_read = await client.read_resource('test://devices')
        # an empty string clears the active namespace
        await client.call_tool(name='namespace-switch', arguments={'namespace': ''})
        cleared_read = await client.read_resource('test://devices')

    assert root_read[0].text == 'root-devices'
    assert team_read[0].text == 'team-a-devices'
    assert cleared_read[0].text == 'root-devices'


@pytest.mark.asyncio
async def test_cache_partitioned_by_namespace(server_under_test: FastMCP, vault_client: SimpleNamespace, vault_data: dict[str | None, str]) -> None:
    async with Client(server_under_test) as client:
        root_read = await client.read_resource('test://devices')
        vault_data[None] = 'out-of-band-devices'
        # the namespace changes without any tool call, so only the cache partitioning can prevent a cross namespace read
        vault_client.adapter.namespace = 'team-a'
        team_read = await client.read_resource('test://devices')
        vault_client.adapter.namespace = None
        root_cached_read = await client.read_resource('test://devices')

    assert root_read[0].text == 'root-devices'
    assert team_read[0].text == 'team-a-devices'
    assert root_cached_read[0].text == 'root-devices'


@pytest.mark.asyncio
async def test_resource_read_not_cached_without_request_context() -> None:
    middleware = cache.VaultResponseCachingMiddleware(read_resource_settings={'ttl': 60})
    context = MiddlewareContext(message=mcp.types.ReadResourceRequestParams(uri='test://devices'), fastmcp_context=None, method='resources/read')
    call_next = AsyncMock(return_value='uncached-result')

    # the active namespace is unknown without a request context, so every read must reach the resource
    assert await middleware.on_read_resource(context, call_next) == 'uncached-result'
    assert await middleware.on_read_resource(context, call_next) == 'uncached-result'
    assert call_next.await_count == 2
