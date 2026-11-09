"""test mcp server support"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastmcp import Client, FastMCP

from vault_mcp_server.mcp_bindings import cache, server
from vault_mcp_server.vault.sys import namespace


def test_server() -> None:
    with patch('vault_mcp_server.mcp_bindings.server.run') as mock_run:
        server.run(transport='stdio')
        mock_run.assert_called_once_with(transport='stdio')


@pytest.mark.asyncio
async def test_server_response_caching() -> None:
    # run constructs the fastmcp object inline, so capture the middleware and transforms that it registers
    with patch('vault_mcp_server.mcp_bindings.server.FastMCP') as mock_fastmcp:
        server.run(transport='stdio')
    caching_middleware: cache.VaultResponseCachingMiddleware = next(
        call.args[0] for call in mock_fastmcp.return_value.add_middleware.call_args_list if isinstance(call.args[0], cache.VaultResponseCachingMiddleware)
    )

    # the hvac client adapter holds the active namespace, and vault data differs between namespaces
    vault_client: SimpleNamespace = SimpleNamespace(adapter=SimpleNamespace(namespace=None))
    vault_data: dict[str | None, str] = {None: 'root-engines', 'team-a': 'team-a-engines'}

    @asynccontextmanager
    async def lifespan(fastmcp_server: FastMCP) -> AsyncGenerator[dict]:
        yield {'client': vault_client}

    # tools are invoked through the call tool transform of the real server, as with an actual client
    mcp: FastMCP = FastMCP(name='server-test', lifespan=lifespan, transforms=mock_fastmcp.call_args.kwargs['transforms'])
    mcp.add_middleware(caching_middleware)
    mcp.tool(name_or_fn=namespace.switch, name='namespace-switch')

    @mcp.resource('test://engines')
    def read_engines() -> str:
        return vault_data[vault_client.adapter.namespace]

    async with Client(mcp) as client:
        root_read = await client.read_resource('test://engines')
        await client.call_tool(name='call_vault_tool', arguments={'name': 'namespace-switch', 'arguments': {'namespace': 'team-a'}})
        team_read = await client.read_resource('test://engines')

    assert root_read[0].text == 'root-engines'
    assert team_read[0].text == 'team-a-engines'
