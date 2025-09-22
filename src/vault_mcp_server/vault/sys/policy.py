"""vault acl policy"""

from typing import Annotated
from fastmcp import Context


def create_update(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the policy to create.'],
    policy: Annotated[dict[str, dict[str, dict[str, list[str]]]], 'Specifies the policy to create or update.'],
) -> dict[str, bool | None]:
    """create or update a vault acl policy"""
    result = ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def delete(ctx: Context, name: Annotated[str, 'Specifies the name of the policy to delete.']) -> dict[str, bool | None]:
    """delete a vault acl policy"""
    result = ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def read(ctx: Context, name: Annotated[str, 'The name of the acl policy to retrieve.']) -> dict[str, str | dict]:
    """read a vault acl policy"""
    return ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name)['data']


async def list(ctx: Context) -> list[str]:
    """list existing vault acl policies"""
    policies: list[str] = ctx.request_context.lifespan_context['sys'].list_acl_policies()['data']['keys']
    return policies if policies else []
