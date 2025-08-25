"""test vault pki mcp integrations"""

import pytest

from fastmcp import exceptions

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_pki() -> None:
    async with dev.client as client:
        # enable pki
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'pki'})
        except exceptions.ToolError:
            pass

        # create_update
        result = await client.call_tool(name='pki-generate-root', arguments={'type': 'exported', 'common_name': 'example.com'})
        assert result.data.get('certificate') is not None
        assert result.data.get('private_key') is not None
