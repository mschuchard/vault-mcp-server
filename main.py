from mcp.server.fastmcp import FastMCP
from vault import client

mcp = FastMCP('Vault')

@mcp.tool()
def kv2_write(mount: str = 'secret', path: str = '', secret: dict = {}) -> dict:
    '''write a kv2 secret to vault'''
    return client.client().secrets.kv.v2.create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
    )

@mcp.tool()
def kv2_delete(mount: str = 'secret', path: str = '') -> bool:
    '''delete a kv2 secret from vault'''
    try:
        client.client().secrets.kv.delete_metadata_and_all_versions(mount_point=mount, path=path)

        return True
    except Exception:
        return False

@mcp.tool()
def kv2_read(mount: str = 'secret', path: str = '') -> dict:
    '''read a kv2 secret from a vault'''
    return client.client().secrets.kv.read_secret_version(mount_point=mount, path=path)['data']

@mcp.tool()
def kv2_list(mount: str = 'secret', path: str = '') -> list:
    '''list the kv2 secrets in vault'''
    return client.client().secrets.kv.v2.list_secrets(mount_point=mount, path=path)['data']['keys']
