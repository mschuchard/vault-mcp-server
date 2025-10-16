"""test vault policy mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_policy() -> None:
    async with dev.client as client:
        # create update
        result = await client.call_tool(name='policy-create-or-update', arguments={'name': 'mypolicy', 'policy': {}})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # list
        result = await client.call_tool(name='policies-list')
        assert result.data == ['default', 'mypolicy', 'root']

        # read
        result = await client.call_tool(name='policy-read', arguments={'name': 'mypolicy'})
        assert result.data == {'name': 'mypolicy', 'policy': '{}'}

        # disable
        result = await client.call_tool(name='policy-delete', arguments={'name': 'mypolicy'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # example
        result = await client.get_prompt(name='example-acl-policy')
        assert len(result.messages[0].content.text) > 0
        assert 'secret/data/my-app/*' in result.messages[0].content.text
        assert 'secret/metadata/my-app/*' in result.messages[0].content.text

        # generate
        result = await client.get_prompt(name='generate-acl-policy', arguments={'paths': ['secret/data/my-app/*', 'secret/metadata/my-app/*']})
        assert len(result.messages[0].content.text) > 0
        assert 'secret/data/my-app/*' in result.messages[0].content.text
        assert 'secret/metadata/my-app/*' in result.messages[0].content.text
