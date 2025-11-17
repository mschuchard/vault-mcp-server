"""test mcp provider support"""

import pytest

from mcp.types import Resource, Prompt, Tool

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_provider() -> None:
    async with dev.client as client:
        tools: list[Tool] = await client.list_tools()
        assert len(tools) == 67
        resources: list[Resource] = await client.list_resources()
        assert len(resources) == 4
        prompts: list[Prompt] = await client.list_prompts()
        assert len(prompts) == 2
