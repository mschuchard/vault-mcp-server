"""vault acl policy"""

import json

from mcp.server.fastmcp import Context


def write(ctx: Context, name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> json:
    """write a acl policy to vault"""
    return ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy).text


def delete(ctx: Context, name: str) -> json:
    """delete a acl policy from vault"""
    return ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name).text


def read(ctx: Context, name: str) -> json:
    """read a acl policy from vault"""
    return json.dumps(ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name))


async def list(ctx: Context) -> json:
    """list acl policies in vault"""
    policies: json = await ctx.read_resource('sys://policies')
    return json.dumps(policies[0].content)
