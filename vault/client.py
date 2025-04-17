"""vault client"""

import os
import hvac


def client() -> hvac.Client:
    """construct authenticated vault client"""
    # assign values from environment variables (standard input method for mcp clients)
    url: str = os.getenv('VAULT_URL', 'http://127.0.0.1:8200')
    token: str = os.getenv('VAULT_TOKEN', '')

    # return authenticated client
    return hvac.Client(url=url, token=token)
