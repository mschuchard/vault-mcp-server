"""vault acl policy"""

from typing import Annotated, List
from fastmcp import Context


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


# In src/vault_mcp_server/vault/sys/policy.py


async def generate_smart_policy(
    description: Annotated[str, 'Natural language description of what this policy should allow'],
) -> str:
    """Generate a context-aware Vault ACL policy prompt with current Vault state"""

    return f"""Generate a Vault ACL policy for: {description}

To create an appropriate policy, first check the current Vault configuration:
1. Read the 'enabled-secret-engines' resource to see what's mounted
2. Read the 'configured-acl-policies' resource to see existing policy patterns
3. Consider the 'enabled-authentication-engines' resource for auth context

Then generate a JSON policy object following this structure:
{{
    "path": {{
        "secret/data/example/*": {{"capabilities": ["read", "list"]}},
        "database/creds/myapp": {{"capabilities": ["read"]}}
    }}
}}

Security rules:
1. Use minimal necessary capabilities: read, list, create, update, delete, sudo
2. Be specific with paths - avoid wildcards unless truly needed
3. For KV v2: use secret/data/* for data, secret/metadata/* for metadata
4. Follow least-privilege principle

Return ONLY the JSON policy object, no markdown code blocks, no explanations.
"""
