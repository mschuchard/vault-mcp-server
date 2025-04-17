from mcp.server.fastmcp import FastMCP
from vault import client
import json

mcp = FastMCP('Vault')


# resources
## auth engines
@mcp.resource(
    uri='auth://engines',
    name='Enabled Authentication Engines',
    description='List the available enabled Vault authentication engines',
    mime_type='application/json',
)
def auth_engines() -> str:
    """list the vault authentication engines"""
    return json.dumps(client.client().sys.list_auth_methods())


## secret engines
@mcp.resource(
    uri='secret://engines', name='Enabled Secret Engines', description='List the available enabled Vault secret engines', mime_type='application/json'
)
def secret_engines() -> str:
    """list the vault secret engines"""
    return json.dumps(client.client().sys.list_mounted_secrets_engines())


## policies
@mcp.resource(
    uri='sys://policies', name='Configured ACL Policies', description='List the available configured Vault ACL policies', mime_type='application/json'
)
def acl_policies() -> str:
    """list the vault acl policies"""
    return json.dumps(client.client().sys.list_acl_policies())


# tools
## auth
### general
@mcp.tool(name='Enable Authentication Engine')
def auth_engine_enable(engine: str, mount: str = None) -> bool:
    """enable a vault authentication engine"""
    try:
        client.client().sys.enable_auth_method(method_type=engine, path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='Disable Authentication Engine')
def auth_engine_disable(mount: str) -> bool:
    """disable a vault auth engine"""
    try:
        client.client().sys.disable_auth_method(path=mount)

        return True
    except Exception:
        return False


## secret engines
### general
@mcp.tool(name='Enable Secret Engine')
def secret_engine_enable(engine: str, mount: str = None) -> bool:
    """enable a vault secret engine"""
    try:
        client.client().sys.enable_secrets_engine(backend_type=engine, path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='Disable Secret Engine')
def secret_engine_disable(mount: str) -> bool:
    """disable a vault secret engine"""
    try:
        client.client().sys.disable_secrets_engine(path=mount)

        return True
    except Exception:
        return False


### kv2
@mcp.tool(name='KV2 Write')
def kv2_write(mount: str = 'secret', path: str = '', secret: dict = {}) -> dict:
    """write a kv2 secret to vault"""
    return client.client().secrets.kv.v2.create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
    )


@mcp.tool(name='KV2 Delete')
def kv2_delete(mount: str = 'secret', path: str = '') -> bool:
    """delete a kv2 secret from vault"""
    try:
        client.client().secrets.kv.delete_metadata_and_all_versions(mount_point=mount, path=path)

        return True
    except Exception:
        return False


@mcp.tool(name='KV2 Read')
def kv2_read(mount: str = 'secret', path: str = '') -> dict:
    """read a kv2 secret from a vault"""
    return client.client().secrets.kv.read_secret_version(mount_point=mount, path=path)['data']


@mcp.tool(name='KV2 List')
def kv2_list(mount: str = 'secret', path: str = '') -> list:
    """list the kv2 secrets in vault"""
    return client.client().secrets.kv.v2.list_secrets(mount_point=mount, path=path)['data']['keys']


## policies
### general
@mcp.tool(name='Policy Write')
def policy_write(name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> bool:
    """write a acl policy to vault"""
    try:
        client.client().sys.create_or_update_acl_policy(name=name, policy=policy)

        return True
    except Exception:
        return False


@mcp.tool(name='Policy Delete')
def policy_delete(name: str) -> bool:
    """delete a acl policy from vault"""
    try:
        client.client().sys.delete_acl_policy(name=name)

        return True
    except Exception:
        return False


@mcp.tool(name='Policy Read')
def policy_read(name: str) -> dict:
    """read a acl policy from vault"""
    return client.client().sys.read_acl_policy(name=name)


if __name__ == '__main__':
    mcp.run(transport='stdio')
