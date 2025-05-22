"""mcp server support"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import json

from mcp.server.fastmcp import FastMCP
import hvac

from vault import client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """manage mcp server lifecycle with type-safe context"""
    # construct vault client
    vault_client: hvac.Client = client.client()
    # initialize resources on startup
    yield {'client': vault_client, 'kv2': vault_client.secrets.kv.v2, 'sys': vault_client.sys, 'transit': vault_client.secrets.transit}


# TODO: local to run function once resources migrated to vault module
mcp: FastMCP = FastMCP(name='Vault', lifespan=server_lifespan)


# resources: TODO refactor once mcp sdk supports fastmcp add_resource updated usage
## auth engines
@mcp.resource(
    uri='auth://engines',
    name='Enabled Authentication Engines',
    description='List the available enabled Vault authentication engines',
    mime_type='application/json',
)
async def auth_engines() -> str:
    """list the vault authentication engines"""
    return json.dumps(client.client().sys.list_auth_methods())


## secret engines
@mcp.resource(
    uri='secret://engines', name='Enabled Secret Engines', description='List the available enabled Vault secret engines', mime_type='application/json'
)
async def secret_engines() -> str:
    """list the vault secret engines"""
    return json.dumps(client.client().sys.list_mounted_secrets_engines())


## policies
@mcp.resource(
    uri='sys://policies', name='Configured ACL Policies', description='List the available configured Vault ACL policies', mime_type='application/json'
)
async def acl_policies() -> str:
    """list the vault acl policies"""
    return json.dumps(client.client().sys.list_acl_policies())


## audit
@mcp.resource(uri='audit://devices', name='Enabled Audit Devices', description='List the available enabled Vault audit devices', mime_type='application/json')
async def audit_devices() -> str:
    """list the vault audit devices"""
    return json.dumps(client.client().sys.list_enabled_audit_devices())
