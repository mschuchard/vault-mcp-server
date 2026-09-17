"""test vault seal status mcp integrations"""

import pytest
import json

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_seal() -> None:
    async with dev.client as client:
        # read
        result = await client.read_resource(uri='sys://seal-status')
        data = json.loads(result[0].text)
        assert data.get('sealed') is False

        result = await client.call_tool(name='seal-status-read')
        assert isinstance(result.data, dict)
        assert result.data.get('sealed') is False
        assert 'n' in result.data
        assert 't' in result.data
