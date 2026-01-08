"""test hvac vault client"""

import os

from hvac import Client
import pytest

from vault_mcp_server.vault import client


def test_client() -> None:
    # default url
    os.environ['VAULT_TOKEN'] = '1234567890123456789012345678'
    default_client: Client = client.client()
    assert default_client.url == 'http://127.0.0.1:8200'
    assert default_client.token == '1234567890123456789012345678'

    # override url
    os.environ['VAULT_URL'] = 'http://localhost:8200'
    overridden_client: Client = client.client()
    assert overridden_client.url == 'http://localhost:8200'
    assert overridden_client.token == '1234567890123456789012345678'


def test_client_errors() -> None:
    # bad token
    os.environ['VAULT_TOKEN'] = 'abcd1234!'
    with pytest.raises(ValueError, match='invalid token'):
        client.client()

    # bad url
    os.environ['VAULT_URL'] = 'invalid_url'
    with pytest.raises(ValueError, match='invalid vault url'):
        client.client()
