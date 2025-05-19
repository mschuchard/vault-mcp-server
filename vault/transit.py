"""vault transit"""

import json

from mcp.server.fastmcp import Context


def create(ctx: Context, name: str, mount: str = 'transit') -> str:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(name=name, mount_point='transit').text


def read(ctx: Context, name: str, mount: str = 'transit') -> str:
    """read a transit encryption key from vault"""
    return json.dumps(ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount))


def list(ctx: Context, mount: str = 'transit') -> str:
    """list transit encryption keys in vault"""
    return json.dumps(ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data']['keys'])


def delete(ctx: Context, name: str, mount: str = 'transit') -> str:
    """delete transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount).text
