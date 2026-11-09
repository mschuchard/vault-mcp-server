"""test vault health mcp integrations"""

import json
from unittest.mock import MagicMock

import pytest
import requests

from vault_mcp_server import dev
from vault_mcp_server.vault.sys import health


@pytest.mark.asyncio
async def test_health() -> None:
    async with dev.client as client:
        # read
        result = await client.read_resource(uri='sys://health')
        data = json.loads(result[0].text)
        assert data.get('initialized') is True
        assert data.get('sealed') is False

        result = await client.call_tool(name='health-status-read')
        assert isinstance(result.data, dict)
        assert result.data.get('initialized') is True
        assert result.data.get('sealed') is False
        assert 'version' in result.data
        assert 'cluster_id' in result.data


@pytest.mark.asyncio
@pytest.mark.parametrize('status_code', [429, 472, 473, 501, 503])
async def test_health_non_200_response(status_code: int) -> None:
    # hvac read_health_status returns a raw requests.Response for any non-200 status code, so the body must be decoded
    body = {'initialized': True, 'sealed': status_code == 503, 'standby': status_code == 429, 'version': '1.20.0'}
    response = MagicMock(spec=requests.Response)
    response.status_code = status_code
    response.json.return_value = body

    ctx = MagicMock()
    ctx.request_context.lifespan_context = {'sys': MagicMock()}
    ctx.request_context.lifespan_context['sys'].read_health_status.return_value = response

    assert await health.read_status(ctx) == body


@pytest.mark.asyncio
async def test_health_200_dict_passthrough() -> None:
    # hvac read_health_status returns a parsed dict for http 200
    body = {'initialized': True, 'sealed': False, 'standby': False}

    ctx = MagicMock()
    ctx.request_context.lifespan_context = {'sys': MagicMock()}
    ctx.request_context.lifespan_context['sys'].read_health_status.return_value = body

    assert await health.read_status(ctx) == body
