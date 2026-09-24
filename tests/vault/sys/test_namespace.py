"""test vault namespace mcp integrations"""

import json

import pytest
from fastmcp import exceptions

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_namespace_switch() -> None:
    async with dev.client as client:
        lifespan_context = dev.mcp._lifespan_result
        assert lifespan_context is not None

        # switch mutates the adapter shared by every sub-engine handle in the lifespan context
        result = await client.call_tool(name='namespace-switch', arguments={'namespace': 'team-a'})
        assert result.data == {'namespace': 'team-a'}
        assert lifespan_context['client'].adapter.namespace == 'team-a'
        # kv2/pki/identity/transit/sys/database hold a reference to the same adapter, not a copy
        assert lifespan_context['sys']._adapter is lifespan_context['client'].adapter

        # empty string clears the namespace rather than sending an empty X-Vault-Namespace header
        result = await client.call_tool(name='namespace-switch', arguments={'namespace': ''})
        assert result.data == {'namespace': None}
        assert lifespan_context['client'].adapter.namespace is None


@pytest.mark.asyncio
async def test_namespace_list() -> None:
    async with dev.client as client:
        # this dev harness runs OSS/CE Vault; sys/namespaces 404s and list_ degrades to []
        result = await client.call_tool(name='namespace-list')
        assert result.data == []

        result = await client.read_resource(uri='sys://namespaces')
        assert json.loads(result[0].text) == []


@pytest.mark.asyncio
async def test_namespace_create_and_delete_require_enterprise() -> None:
    async with dev.client as client:
        # create/delete don't catch InvalidPath themselves; on OSS/CE the 404 propagates and
        # VaultErrorMiddleware restructures it into a tool error rather than raising unstructured
        with pytest.raises(exceptions.ToolError, match='invalid_path'):
            await client.call_tool(name='namespace-create', arguments={'path': 'team-a'})

        with pytest.raises(exceptions.ToolError, match='invalid_path'):
            await client.call_tool(name='namespace-delete', arguments={'path': 'team-a'})
