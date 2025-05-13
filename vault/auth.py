"""vault authentication engine"""

import json

from mcp.server.fastmcp import Context


def enable(ctx: Context, engine: str, mount: str = None) -> json:
    """enable a vault authentication engine"""
    return ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> json:
    """disable a vault auth engine"""
    return ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount).text


async def list(ctx: Context) -> json:
    """list enabled authentication engines in vault"""
    engines: json = await ctx.read_resource('auth://engines')
    return json.dumps(engines[0].content)
