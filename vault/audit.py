"""vault audit device"""

import json
from typing import Iterable

from fastmcp import Context
from mcp.server.lowlevel.helper_types import ReadResourceContents


def enable(ctx: Context, type: str, path: str) -> str:
    """enable a vault audit device"""
    return ctx.request_context.lifespan_context['sys'].enable_audit_device(device_type=type, path=path).text


def disable(ctx: Context, path: str) -> str:
    """disable a vault audit device"""
    return ctx.request_context.lifespan_context['sys'].disable_audit_device(path=path).text


async def list(ctx: Context) -> str:
    """list enabled audit devices in vault"""
    devices: Iterable[ReadResourceContents] = await ctx.read_resource('audit://devices')
    return json.dumps(devices[0].content if len(devices) > 0 else [])  # type: ignore (guaranteed list)
