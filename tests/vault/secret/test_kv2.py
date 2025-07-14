"""test vault kv2 mcp integrations"""

import pytest

from fastmcp import FastMCP, Client

from mcp_bindings import server, provider

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)


@pytest.mark.asyncio
async def test_run() -> None:
    async with Client(mcp) as client:
        provider.provider(mcp)

        # create_update
        result = await client.call_tool(name='kv2-create-or-update', arguments={'path': 'mysecret', 'secret': {'foo': 'bar', 'baz': 'bat'}})
        assert result[0]

        # list
        result = await client.call_tool(name='kv2-list')
        assert result[0]

        # read
        result = await client.call_tool(name='kv2-read', arguments={'path': 'mysecret'})
        assert result[0]

        # patch
        result = await client.call_tool(name='kv2-patch', arguments={'path': 'mysecret', 'secret': {'foobar': 'bazbat'}})
        assert result[0]

        # metadata
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result[0]

        # delete
        result = await client.call_tool(name='kv2-delete', arguments={'path': 'mysecret'})
        assert result[0]
