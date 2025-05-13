"""vault audit device"""

import json

from mcp.server.fastmcp import Context


def enable(ctx: Context, type: str, path: str) -> json:
    """enable a vault audit device"""
    return ctx.request_context.lifespan_context['sys'].enable_audit_device(device_type=type, path=path).text


def disable(ctx: Context, path: str) -> json:
    """disable a vault audit device"""
    return ctx.request_context.lifespan_context['sys'].disable_audit_device(path=path).text


async def list(ctx: Context) -> json:
    """list enabled audit devices in vault"""
    devices = await ctx.read_resource('audit://devices')
    return json.dumps(devices[0].content)
