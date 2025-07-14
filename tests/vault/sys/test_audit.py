"""test vault secret engine mcp integrations"""

import pytest

from fastmcp import FastMCP, Client

from mcp_bindings import server, provider

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)


@pytest.mark.asyncio
async def test_run() -> None:
    async with Client(mcp) as client:
        provider.provider(mcp)

        # enable: TODO requires options to actually function, and so wait on expanded functionality
        result = await client.call_tool(name='audit-device-enable', arguments={'path': 'tmpfile', 'type': 'file'})
        assert result[0]

        # list
        result = await client.call_tool(name='audit-devices-list')
        assert result[0]

        # disable
        result = await client.call_tool(name='audit-device-disable', arguments={'path': 'tmpfile'})
        assert result[0]
