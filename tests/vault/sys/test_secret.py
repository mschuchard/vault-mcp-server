"""test vault secret engine mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_secret() -> None:
    async with dev.client as client:
        # enable
        result = await client.call_tool(name='secret-engine-enable', arguments={'engine': 'kubernetes'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # list
        result = await client.call_tool(name='secret-engines-list')
        assert len(result.data) > 0

        # read configuration
        result = await client.call_tool(name='secret-engine-read-configuration', arguments={'mount': 'kubernetes'})
        assert isinstance(result.data, dict)

        # tune configuration
        result = await client.call_tool(
            name='secret-engine-tune-configuration',
            arguments={'mount': 'kubernetes', 'default_lease_ttl': '3600s', 'description': 'Updated Kubernetes secrets engine'},
        )
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # retrieve option (if options were set during enable or tune)
        result = await client.call_tool(
            name='secret-engine-retrieve-option', arguments={'mount': 'kubernetes', 'option_name': 'version', 'default_value': 'not-found'}
        )
        assert result.data is not None

        # move
        result = await client.call_tool(name='secret-engine-move', arguments={'from_path': 'kubernetes', 'to_path': 'k8s'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None

        # verify move by reading configuration at new path
        result = await client.call_tool(name='secret-engine-read-configuration', arguments={'mount': 'k8s'})
        assert isinstance(result.data, dict)

        # disable at new location
        result = await client.call_tool(name='secret-engine-disable', arguments={'mount': 'k8s'})
        assert result.data.get('success') is True
        assert result.data.get('error') is None
