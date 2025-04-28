from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import json

from mcp.server.fastmcp import Context, FastMCP
import hvac

from vault import client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage mcp server lifecycle with type-safe context"""
    # Initialize resources on startup
    vault_client: hvac.Client = client.client()
    yield {'client': vault_client}


mcp = FastMCP('Vault', lifespan=server_lifespan)
# ctx.request_context.lifespan_context['client']


# resources
## auth engines
@mcp.resource(
    uri='auth://engines',
    name='Enabled Authentication Engines',
    description='List the available enabled Vault authentication engines',
    mime_type='application/json',
)
def auth_engines() -> json:
    """list the vault authentication engines"""
    return json.dumps(client.client().sys.list_auth_methods())


## secret engines
@mcp.resource(
    uri='secret://engines', name='Enabled Secret Engines', description='List the available enabled Vault secret engines', mime_type='application/json'
)
def secret_engines() -> json:
    """list the vault secret engines"""
    return json.dumps(client.client().sys.list_mounted_secrets_engines())


## policies
@mcp.resource(
    uri='sys://policies', name='Configured ACL Policies', description='List the available configured Vault ACL policies', mime_type='application/json'
)
def acl_policies() -> json:
    """list the vault acl policies"""
    return json.dumps(client.client().sys.list_acl_policies())


# tools
## auth
### general
@mcp.tool(name='Enable Authentication Engine')
def auth_engine_enable(ctx: Context, engine: str, mount: str = None) -> bool:
    """enable a vault authentication engine"""
    try:
        ctx.request_context.lifespan_context['client'].sys.enable_auth_method(method_type=engine, path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='Disable Authentication Engine')
def auth_engine_disable(ctx: Context, mount: str) -> bool:
    """disable a vault auth engine"""
    try:
        ctx.request_context.lifespan_context['client'].sys.disable_auth_method(path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='List Authentication Engines')
async def auth_engine_list(ctx: Context) -> json:
    """list enabled authentication engines in vault: alpha"""
    engines: json = await ctx.read_resource('auth://engines')
    return json.dumps(engines['content'])


## secret engines
### general
@mcp.tool(name='Enable Secret Engine')
def secret_engine_enable(ctx: Context, engine: str, mount: str = None) -> bool:
    """enable a vault secret engine"""
    try:
        ctx.request_context.lifespan_context['client'].sys.enable_secrets_engine(backend_type=engine, path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='Disable Secret Engine')
def secret_engine_disable(ctx: Context, mount: str) -> bool:
    """disable a vault secret engine"""
    try:
        ctx.request_context.lifespan_context['client'].sys.disable_secrets_engine(path=mount)

        return True
    except Exception:
        return False


@mcp.tool(name='List Secret Engines')
async def secret_engine_list(ctx: Context) -> json:
    """list enabled secret engines in vault: alpha"""
    engines: json = await ctx.read_resource('secret://engines')
    return json.dumps(engines['content'])


### kv2
@mcp.tool(name='KV2 Write')
def kv2_write(ctx: Context, mount: str = 'secret', path: str = '', secret: dict = {}) -> json:
    """write a kv2 secret to vault"""
    return json.dumps(
        ctx.request_context.lifespan_context['client'].secrets.kv.v2.create_or_update_secret(
            mount_point=mount,
            path=path,
            secret=secret,
        )
    )


@mcp.tool(name='KV2 Delete')
def kv2_delete(ctx: Context, mount: str = 'secret', path: str = '') -> bool:
    """delete a kv2 secret from vault"""
    try:
        ctx.request_context.lifespan_context['client'].secrets.kv.delete_metadata_and_all_versions(mount_point=mount, path=path)

        return True
    except Exception:
        return False


@mcp.tool(name='KV2 Read')
def kv2_read(ctx: Context, mount: str = 'secret', path: str = '') -> json:
    """read a kv2 secret from a vault"""
    return json.dumps(ctx.request_context.lifespan_context['client'].secrets.kv.read_secret_version(mount_point=mount, path=path)['data'])


@mcp.tool(name='KV2 List')
def kv2_list(ctx: Context, mount: str = 'secret', path: str = '') -> json:
    """list the kv2 secrets in vault"""
    return json.dumps(ctx.request_context.lifespan_context['client'].secrets.kv.v2.list_secrets(mount_point=mount, path=path)['data']['keys'])


## policies
### general
@mcp.tool(name='Policy Write')
def policy_write(ctx: Context, name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> bool:
    """write a acl policy to vault"""
    try:
        ctx.request_context.lifespan_context['client'].sys.create_or_update_acl_policy(name=name, policy=policy)

        return True
    except Exception:
        return False


@mcp.tool(name='Policy Delete')
def policy_delete(ctx: Context, name: str) -> bool:
    """delete a acl policy from vault"""
    try:
        ctx.request_context.lifespan_context['client'].sys.delete_acl_policy(name=name)

        return True
    except Exception:
        return False


@mcp.tool(name='Policy Read')
def policy_read(ctx: Context, name: str) -> json:
    """read a acl policy from vault"""
    return json.dumps(ctx.request_context.lifespan_context['client'].sys.read_acl_policy(name=name))


@mcp.tool(name='Policy List')
async def policy_list(ctx: Context) -> json:
    """list acl policies in vault: alpha"""
    policies: json = await ctx.read_resource('sys://policies')
    return json.dumps(policies['content'])


if __name__ == '__main__':
    mcp.run(transport='stdio')
