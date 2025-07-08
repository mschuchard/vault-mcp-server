"""test mcp provider support"""

import pytest

from fastmcp import FastMCP, Client
from mcp.types import Resource

from mcp_bindings import server, provider

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)


@pytest.mark.asyncio
async def test_run() -> None:
    async with Client(mcp) as client:
        provider.provider(mcp)
        tools = await client.list_tools()
        assert len(tools) == 27
        resources: list[Resource] = await client.list_resources()
        assert len(resources) == 4
