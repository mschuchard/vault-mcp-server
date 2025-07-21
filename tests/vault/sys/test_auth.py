"""test vault authentication engine mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_auth() -> None:
    async with utils.mcp_client() as client:
        # enable
        result = await client.call_tool(name='authentication-engine-enable', arguments={'engine': 'kubernetes'})
        assert result[0]

        # list
        result = await client.call_tool(name='authentication-engines-list')
        assert result[0]

        # disable
        result = await client.call_tool(name='authentication-engine-disable', arguments={'mount': 'kubernetes'})
        assert result[0]
