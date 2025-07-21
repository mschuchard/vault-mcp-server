"""test vault audit device mcp integrations"""

import pytest

from tests import utils


@pytest.mark.asyncio
async def test_audit() -> None:
    async with utils.mcp_client() as client:
        # enable: TODO requires options to actually function, and so wait on expanded functionality
        result = await client.call_tool(name='audit-device-enable', arguments={'path': 'tmpfile', 'type': 'file'})
        assert result[0]

        # list
        result = await client.call_tool(name='audit-devices-list')
        assert result[0]

        # disable
        result = await client.call_tool(name='audit-device-disable', arguments={'path': 'tmpfile'})
        assert result[0]
