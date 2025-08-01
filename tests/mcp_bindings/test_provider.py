"""test mcp provider support"""

import pytest

from mcp.types import Resource

from tests import utils


@pytest.mark.asyncio
async def test_provider() -> None:
    async with utils.mcp_client() as client:
        tools = await client.list_tools()
        assert len(tools) == 29
        resources: list[Resource] = await client.list_resources()
        assert len(resources) == 4
