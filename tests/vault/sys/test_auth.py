"""test vault authentication engine mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_auth() -> None:
    async with dev.mcp_client() as client:
        # enable
        result = await client.call_tool(name='authentication-engine-enable', arguments={'engine': 'kubernetes'})
        assert result.data.get('success') is True

        # list
        result = await client.call_tool(name='authentication-engines-list')
        assert 'kubernetes/' in result.data
        assert 'token/' in result.data

        # disable
        result = await client.call_tool(name='authentication-engine-disable', arguments={'mount': 'kubernetes'})
        assert result.data.get('success') is True
