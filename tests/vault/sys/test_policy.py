"""test vault policy mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_policy() -> None:
    async with utils.mcp_client() as client:
        # create update
        result = await client.call_tool(name='policy-create-or-update', arguments={'name': 'mypolicy', 'policy': {}})
        assert result.data.get('success') is True

        # list
        result = await client.call_tool(name='policies-list')
        assert result.data == ['default', 'mypolicy', 'root']

        # read
        result = await client.call_tool(name='policy-read', arguments={'name': 'mypolicy'})
        assert result.data == {'name': 'mypolicy', 'policy': '{}'}

        # disable
        result = await client.call_tool(name='policy-delete', arguments={'name': 'mypolicy'})
        assert result.data.get('success') is True
