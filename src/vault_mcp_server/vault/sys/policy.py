"""vault acl policy"""

from typing import Annotated, List
from fastmcp import Context

from vault_mcp_server.vault.sys import auth, secret
from vault_mcp_server.vault.secret import database, kv2, pki, transit


def create_update(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the policy to create.'],
    policy: Annotated[str | dict[str, dict[str, dict[str, list[str]]]], 'Specifies the policy document. Can be a string (HCL) or dict (JSON).'],
    pretty_print: Annotated[bool, 'If True and policy is a dict, send JSON with pretty formatting.'] = True,
) -> dict[str, bool | None]:
    """create or update a vault acl policy"""
    result = ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy, pretty_print=pretty_print)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def delete(ctx: Context, name: Annotated[str, 'Specifies the name of the policy to delete.']) -> dict[str, bool | None]:
    """delete a vault acl policy"""
    result = ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def read(ctx: Context, name: Annotated[str, 'The name of the acl policy to retrieve.']) -> dict[str, str | dict]:
    """read a vault acl policy"""
    return ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name)['data']


async def list_(ctx: Context) -> list[str]:
    """list existing vault acl policies"""
    policies: list[str] = ctx.request_context.lifespan_context['sys'].list_acl_policies()['data']['keys']
    return policies if policies else []


async def example_policy() -> dict[str, dict[str, dict[str, List[str]]]]:
    """display an example vault acl policy"""
    return {'path': {'secret/data/my-app/*': {'capabilities': ['read', 'list']}, 'secret/metadata/my-app/*': {'capabilities': ['list']}}}


async def generate_policy(
    paths: Annotated[List[str], 'The list of Vault access paths to include in the generated policy.'],
) -> dict[str, dict[str, dict[str, List[str]]]]:
    """generate a vault acl policy example with input paths"""
    # initialize policy dictionary
    policy: dict[str, dict[str, dict[str, list[str]]]] = {'path': {}}

    # iterate through paths and attach example capabilities
    for path in paths:
        policy['path'][path] = {'capabilities': ['read', 'list']}

    return policy


async def generate_smart_policy(
    ctx: Context,
    description: Annotated[str, 'Natural language description of what this policy should allow'],
) -> str:
    """Generate a context-aware Vault ACL policy prompt with current Vault state"""
    # validate description
    if not description.strip():
        raise ValueError('description must not be empty')

    # gather resource information
    policies: list[str] = await list_(ctx)
    secret_engines: dict = await secret.list_(ctx)
    auth_engines: dict = await auth.list_(ctx)

    # read policy contents for pattern reference
    policy_contents: dict[str, dict] = {}
    for name in policies:
        policy_contents[name] = await read(ctx, name=name)

    # gather per-engine role/key/path information based on what is actually mounted
    engine_roles: dict[str, dict] = {}
    mounted_paths: set = set(secret_engines.keys())

    for mount_path in mounted_paths:
        # strip trailing slash vault includes in listed paths
        clean_path = mount_path.rstrip('/')
        engine_type = secret_engines[mount_path].get('type', '')

        # gather the roles for each mounted secret engine
        try:
            match engine_type:
                case 'database':
                    dynamic = await database.list_roles(ctx, mount=clean_path)
                    static = await database.list_static_roles(ctx, mount=clean_path)
                    engine_roles[clean_path] = {'type': 'database', 'dynamic_roles': dynamic, 'static_roles': static}
                case 'pki':
                    roles = await pki.list_roles(ctx, mount=clean_path)
                    issuers = await pki.list_issuers(ctx, mount=clean_path)
                    engine_roles[clean_path] = {'type': 'pki', 'roles': roles, 'issuers': issuers}
                case 'transit':
                    keys = await transit.list_(ctx, mount=clean_path)
                    engine_roles[clean_path] = {'type': 'transit', 'keys': keys}
                case 'kv' if secret_engines[mount_path].get('options', {}).get('version') == '2':
                    paths = await kv2.list_(ctx, mount=clean_path)
                    engine_roles[clean_path] = {'type': 'kv2', 'top_level_paths': paths}
        except Exception:
            pass

    return f"""Generate a Vault ACL policy for: {description}

Current Vault state:
- Mounted secret engines: {secret_engines}
- Secret engine roles and keys: {engine_roles}
- Existing ACL policies: {policies}
- Enabled authentication methods: {auth_engines}
- Policy contents (for pattern reference): {policy_contents}

Return ONLY a JSON policy object. Use only the paths that exist above.
Follow least-privilege: prefer read/list over create/update/delete.

Path construction guidance based on engine_roles:
- database dynamic roles: <mount>/creds/<role-name>
- database static roles: <mount>/static-creds/<role-name>
- pki roles: <mount>/issue/<role-name> and <mount>/sign/<role-name>
- transit keys: <mount>/encrypt/<key-name> and <mount>/decrypt/<key-name>
- kv2 data: <mount>/data/<path> and <mount>/metadata/<path>

Avoid sudo unless absolutely required — it grants unrestricted access.

Example structure in addition to those enumerated above:
{{
    "path": {{
        "secret/data/myapp/*": {{"capabilities": ["read", "list"]}}
    }}
}}"""
