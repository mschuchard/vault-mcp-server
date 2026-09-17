"""test vault health mcp integrations"""

import pytest
import json

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_health() -> None:
    async with dev.client as client:
        # read
        result = await client.read_resource(uri='sys://health')
        data = json.loads(result[0].text)
        assert data.get('initialized') is True
        assert data.get('sealed') is False
