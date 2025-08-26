"""test mcp provider support"""

import pytest

from mcp.types import Resource

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_provider() -> None:
    async with dev.client as client:
        tools = await client.list_tools()
        assert len(tools) == 45
        resources: list[Resource] = await client.list_resources()
        assert len(resources) == 4
