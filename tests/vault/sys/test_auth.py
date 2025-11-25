"""test vault authentication engine mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_auth() -> None:
    async with dev.client as client:
        # enable
        result = await client.call_tool(name='authentication-engine-enable', arguments={'method_type': 'kubernetes'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # list
        result = await client.call_tool(name='authentication-engines-list')
        assert 'kubernetes/' in result.data
        assert 'token/' in result.data

        # read
        result = await client.call_tool(name='authentication-engine-read', arguments={'path': 'kubernetes'})
        assert isinstance(result.data, dict)
        assert 'default_lease_ttl' in result.data or 'type' in result.data

        # tune
        result = await client.call_tool(
            name='authentication-engine-tune',
            arguments={'path': 'kubernetes', 'default_lease_ttl': 3600, 'max_lease_ttl': 7200, 'description': 'Kubernetes auth method for testing'},
        )
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # read again to verify tune
        result = await client.call_tool(name='authentication-engine-read', arguments={'path': 'kubernetes'})
        assert isinstance(result.data, dict)
        # Verify the tuned values
        assert result.data.get('default_lease_ttl') == 3600 or result.data.get('config', {}).get('default_lease_ttl') == 3600

        # disable
        result = await client.call_tool(name='authentication-engine-disable', arguments={'path': 'kubernetes'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None
