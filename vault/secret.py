"""vault secret engine"""

import json
from typing import Iterable

from mcp.server.fastmcp import Context
from mcp.server.lowlevel.helper_types import ReadResourceContents


def enable(ctx: Context, engine: str, mount: str | None = None) -> str:
    """enable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].enable_secrets_engine(backend_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> str:
    """disable a vault secret engine"""
    return ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount).text


async def list(ctx: Context) -> str:
    """list enabled secret engines in vault"""
    engines: Iterable[ReadResourceContents] = await ctx.read_resource('secret://engines')
    return json.dumps(engines[0].content if len(engines) > 0 else [])  # type: ignore (guaranteed list)
