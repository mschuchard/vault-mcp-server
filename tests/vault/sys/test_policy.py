"""test vault policy mcp integrations"""

import pytest

from fastmcp import FastMCP, Client

from mcp_bindings import server, provider

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)


@pytest.mark.asyncio
async def test_run() -> None:
    async with Client(mcp) as client:
        provider.provider(mcp)

        # create
        result = await client.call_tool(name='policy-create', arguments={'name': 'mypolicy', 'policy': {}})
        assert result[0]

        # list
        result = await client.call_tool(name='policies-list')
        assert result[0]

        # read
        result = await client.call_tool(name='policy-read', arguments={'name': 'mypolicy'})
        assert result[0]

        # disable
        result = await client.call_tool(name='policy-delete', arguments={'name': 'mypolicy'})
        assert result[0]
