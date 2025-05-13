"""vault secret engine"""

import json

from mcp.server.fastmcp import Context


def enable(ctx: Context, engine: str, mount: str = None) -> json:
    """enable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].enable_secrets_engine(backend_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> json:
    """disable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount).text


async def list(ctx: Context) -> json:
    """list enabled secret engines in vault"""
    engines: json = await ctx.read_resource('secret://engines')
    return json.dumps(engines[0].content)
