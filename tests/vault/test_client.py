"""test hvac vault client"""

from hvac import Client
import pytest

from vault_mcp_server.vault import client


def test_client(monkeypatch) -> None:
    # default url
    monkeypatch.setenv('VAULT_TOKEN', '1234567890123456789012345678')
    default_client: Client = client.client()
    assert default_client.url == 'http://127.0.0.1:8200'
    assert default_client.token == '1234567890123456789012345678'

    # override url
    monkeypatch.setenv('VAULT_URL', 'http://localhost:8200')
    overridden_client: Client = client.client()
    assert overridden_client.url == 'http://localhost:8200'
    assert overridden_client.token == '1234567890123456789012345678'

    # approle
    monkeypatch.setenv('VAULT_AUTH_METHOD', 'approle')
    monkeypatch.setenv('VAULT_ROLE_ID', 'test-role-id')
    monkeypatch.setenv('VAULT_SECRET_ID', 'test-secret-id')
    approle_client: Client = client.client()
    assert approle_client.is_authenticated()

    # userpass
    monkeypatch.setenv('VAULT_AUTH_METHOD', 'userpass')
    monkeypatch.setenv('VAULT_USERNAME', 'test-user')
    monkeypatch.setenv('VAULT_PASSWORD', 'test-password123')
    userpass_client: Client = client.client()
    assert userpass_client.is_authenticated()


def test_client_errors(monkeypatch) -> None:
    # unknown auth method
    monkeypatch.setenv('VAULT_AUTH_METHOD', 'unknown')
    with pytest.raises(ValueError, match='Unknown auth method'):
        client.client()

    # bad token
    monkeypatch.setenv('VAULT_AUTH_METHOD', 'token')
    monkeypatch.setenv('VAULT_TOKEN', 'abcd1234!')
    with pytest.raises(ValueError, match='invalid token'):
        client.client()

    # bad url
    monkeypatch.setenv('VAULT_URL', 'invalid_url')
    with pytest.raises(ValueError, match='invalid vault url'):
        client.client()
