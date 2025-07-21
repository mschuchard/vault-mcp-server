"""test vault policy mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_policy() -> None:
    async with utils.mcp_client() as client:
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
