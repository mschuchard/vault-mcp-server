"""vault acl policy"""

import json
from typing import Iterable

from fastmcp import Context
from mcp.server.lowlevel.helper_types import ReadResourceContents


def write(ctx: Context, name: str, policy: dict[str, dict[str, dict[str, list[str]]]]) -> str:
    """write a acl policy to vault"""
    return ctx.request_context.lifespan_context['sys'].create_or_update_acl_policy(name=name, policy=policy).text


def delete(ctx: Context, name: str) -> str:
    """delete a acl policy from vault"""
    return ctx.request_context.lifespan_context['sys'].delete_acl_policy(name=name).text


async def read(ctx: Context, name: str) -> str:
    """read a acl policy from vault"""
    return json.dumps(ctx.request_context.lifespan_context['sys'].read_acl_policy(name=name))


async def list(ctx: Context) -> str:
    """list acl policies in vault"""
    policies: Iterable[ReadResourceContents] = await ctx.read_resource('sys://policies')
    return json.dumps(policies[0].content if len(policies) > 0 else [])  # type: ignore (guaranteed list)
