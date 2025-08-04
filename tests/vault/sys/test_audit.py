"""test vault audit device mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_audit() -> None:
    async with utils.mcp_client() as client:
        # enable
        result = await client.call_tool(name='audit-device-enable', arguments={'type': 'file', 'options': {'path': '/tmp/vault.audit.log'}, 'path': 'tmpfile'})
        assert result.data.get('success') is True

        # list
        result = await client.call_tool(name='audit-devices-list')
        assert result.data == {'tmpfile/': {'description': '', 'path': 'tmpfile/', 'type': 'file', 'options': {'path': '/tmp/vault.audit.log'}, 'local': False}}

        # disable
        result = await client.call_tool(name='audit-device-disable', arguments={'path': 'tmpfile'})
        assert result.data.get('success') is True
