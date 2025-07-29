"""test vault kv2 mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_kv2() -> None:
    async with utils.mcp_client() as client:
        # create_update
        result = await client.call_tool(name='kv2-create-or-update', arguments={'path': 'mysecret', 'secret': {'foo': 'bar', 'baz': 'bat'}})
        assert result[0]

        # list
        result = await client.call_tool(name='kv2-list')
        assert result[0]

        # read
        result = await client.call_tool(name='kv2-read', arguments={'path': 'mysecret'})
        assert result[0]

        # patch
        result = await client.call_tool(name='kv2-patch', arguments={'path': 'mysecret', 'secret': {'foobar': 'bazbat'}})
        assert result[0]

        # metadata
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result[0]

        # delete
        result = await client.call_tool(name='kv2-delete', arguments={'path': 'mysecret'})
        assert result[0]

        # undelete
        result = await client.call_tool(name='kv2-undelete', arguments={'versions': [1], 'path': 'mysecret'})
        assert result[0]
