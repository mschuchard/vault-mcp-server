"""vault acl policy"""

from fastmcp import Context


def create_update(ctx: Context, name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> dict[str, bool]:
    """create or update a vault acl policy"""
    return {'success': ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy).ok}


def delete(ctx: Context, name: str) -> dict[str, bool]:
    """delete a vault acl policy"""
    return {'success': ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name).ok}


async def read(ctx: Context, name: str) -> dict[str, str | dict]:
    """read a vault acl policy"""
    return ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name)['data']


async def list(ctx: Context) -> list[str]:
    """list existing vault acl policies"""
    policies: list[str] = ctx.request_context.lifespan_context['sys'].list_acl_policies()['data']['keys']
    return policies if len(policies) > 0 else []
