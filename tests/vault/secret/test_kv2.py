"""test vault kv2 mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_kv2() -> None:
    async with dev.client as client:
        # create_update
        result = await client.call_tool(name='kv2-create-or-update', arguments={'path': 'mysecret', 'secret': {'foo': 'bar', 'baz': 'bat'}})
        assert result.data.get('version') == 1

        # list
        result = await client.call_tool(name='kv2-list')
        assert result.data == ['mysecret']

        # read
        result = await client.call_tool(name='kv2-read', arguments={'path': 'mysecret'})
        assert result.data == {'foo': 'bar', 'baz': 'bat'}

        # patch
        result = await client.call_tool(name='kv2-patch', arguments={'path': 'mysecret', 'secret': {'foobar': 'bazbat'}})
        assert result.data.get('version') == 2

        # metadata
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result.data.get('current_version') == 2

        # delete
        result = await client.call_tool(name='kv2-delete', arguments={'path': 'mysecret'})
        assert result.data.get('success') is True

        # undelete
        result = await client.call_tool(name='kv2-undelete', arguments={'versions': [1, 2], 'path': 'mysecret'})
        assert result.data.get('success') is True
