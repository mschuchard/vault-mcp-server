"""vault client"""

import os
import json

import hvac
import hvac.exceptions


def client() -> hvac.Client:
    """construct authenticated vault client"""
    # assign values from environment variables (standard input method for mcp clients)
    url: str = os.getenv('VAULT_URL', 'http://127.0.0.1:8200')
    token: str = os.getenv('VAULT_TOKEN', '')

    # construct and validate client
    client: hvac.Client = hvac.Client(url=url, token=token)

    if not client.is_authenticated:
        raise hvac.exceptions.Unauthorized('invalid authentication')

    if json.loads(client.seal_status)['sealed']:
        raise hvac.exceptions.VaultNotInitialized('vault server is sealed')

    # return authenticated client
    return client
