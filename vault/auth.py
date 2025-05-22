"""vault authentication engine"""

import json

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None) -> str:
    """enable a vault authentication engine"""
    return ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> str:
    """disable a vault auth engine"""
    return ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount).text


async def list(ctx: Context) -> str:
    """list enabled authentication engines in vault"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_auth_methods()['data']
    return json.dumps(engines if len(engines) > 0 else [])  # type: ignore (guaranteed list)
