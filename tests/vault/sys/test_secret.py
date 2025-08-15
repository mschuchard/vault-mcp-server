"""test vault secret engine mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_secret() -> None:
    async with dev.mcp_client() as client:
        # enable
        result = await client.call_tool(name='secret-engine-enable', arguments={'engine': 'kubernetes'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # list
        result = await client.call_tool(name='secret-engines-list')
        assert len(result.data) > 0

        # disable
        result = await client.call_tool(name='secret-engine-disable', arguments={'mount': 'kubernetes'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None
