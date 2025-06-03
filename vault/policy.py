"""vault acl policy"""

from fastmcp import Context


def create(ctx: Context, name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> str:
    """create a acl policy in vault"""
    return ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy).text


def delete(ctx: Context, name: str) -> str:
    """delete a acl policy from vault"""
    return ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name).text


async def read(ctx: Context, name: str) -> str:
    """read a acl policy from vault"""
    return ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name)['data']


async def list(ctx: Context) -> list[str]:
    """list acl policies in vault"""
    policies: list[str] = ctx.request_context.lifespan_context['sys'].list_acl_policies()['data']['keys']
    return policies if len(policies) > 0 else []
