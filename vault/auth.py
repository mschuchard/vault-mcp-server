"""vault authentication engine"""

import json
from typing import Iterable

from mcp.server.fastmcp import Context
from mcp.server.lowlevel.helper_types import ReadResourceContents


def enable(ctx: Context, engine: str, mount: str | None = None) -> str:
    """enable a vault authentication engine"""
    return ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> str:
    """disable a vault auth engine"""
    return ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount).text


async def list(ctx: Context) -> str:
    """list enabled authentication engines in vault"""
    engines: Iterable[ReadResourceContents] = await ctx.read_resource('auth://engines')
    return json.dumps(engines[0].content if len(engines) > 0 else [])  # type: ignore (guaranteed list)
