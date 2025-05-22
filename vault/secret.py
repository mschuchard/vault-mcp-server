"""vault secret engine"""

import json

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None) -> str:
    """enable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].enable_secrets_engine(backend_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> str:
    """disable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount).text


async def list(ctx: Context) -> str:
    """list enabled secret engines in vault"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_mounted_secrets_engines()['data']
    return json.dumps(engines if len(engines) > 0 else [])  # type: ignore (guaranteed list)
