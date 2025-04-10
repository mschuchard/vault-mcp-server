'''vault client'''
import os
import hvac


def client(url: str = '', token: str = '') -> hvac.Client:
    '''construct authenticated vault client'''
    # url backup to environment var
    if len(url) == 0:
        url = os.getenv('VAULT_URL', 'http://127.0.0.1:8200')

    # token backup to environment var
    if len(token) == 0:
        token = os.getenv('VAULT_TOKEN', '')

    # return authenticated client
    return hvac.Client(
        url=url,
        token=token
    )
