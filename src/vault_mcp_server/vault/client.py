"""vault client"""

import os
import re
import urllib.parse

import hvac
import hvac.exceptions


def client() -> hvac.Client:
    """construct and validate authenticated vault client"""
    # assign url value
    url: str = os.getenv('VAULT_URL', 'http://127.0.0.1:8200')
    # validate url
    parsed = urllib.parse.urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError('invalid vault url')
    # construct client with url and namespace
    client: hvac.Client = hvac.Client(url=url, namespace=os.getenv('VAULT_NAMESPACE') or None)

    # authenticate with selected method
    match os.getenv('VAULT_AUTH_METHOD', 'token'):
        case 'token':
            # assign token value
            token: str = os.environ['VAULT_TOKEN']
            # validate token value
            if not re.match(r'^[a-zA-Z0-9.]+$', token):
                raise ValueError('invalid token format')
            # authenticate client
            client.token = token
        case 'approle':
            # push method approle login
            resp = client.auth.approle.login(
                role_id=os.environ['VAULT_ROLE_ID'],
                secret_id=os.environ['VAULT_SECRET_ID'],
            )
            # use response token to authenticate
            client.token = resp['auth']['client_token']
        case 'userpass':
            # userpass method login
            resp = client.auth.userpass.login(
                username=os.environ['VAULT_USERNAME'],
                password=os.environ['VAULT_PASSWORD'],
            )
            # use response token to authenticate
            client.token = resp['auth']['client_token']
        case other:
            # unknown auth method
            raise ValueError(f'Unknown auth method: {other}')

    # validate client
    if not client.is_authenticated:
        raise hvac.exceptions.Unauthorized('invalid authentication')
    if client.sys.is_sealed():
        raise hvac.exceptions.VaultNotInitialized('vault server is sealed')

    # return authenticated client
    return client
