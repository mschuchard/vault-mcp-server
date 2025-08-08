"""vault audit device"""

from fastmcp import Context


def enable(ctx: Context, type: str, path: str | None = None, options: dict | None = None, local: bool | None = None) -> dict[str, bool]:
    """enable a vault audit device"""
    return {'success': ctx.request_context.lifespan_context['sys'].enable_audit_device(device_type=type, path=path, options=options, local=local).ok}


def disable(ctx: Context, path: str) -> dict[str, bool]:
    """disable a vault audit device"""
    return {'success': ctx.request_context.lifespan_context['sys'].disable_audit_device(path=path).ok}


async def list(ctx: Context) -> dict:
    """list enabled vault audit devices"""
    devices: dict = ctx.request_context.lifespan_context['sys'].list_enabled_audit_devices()['data']
    return devices if len(devices) > 0 else {}
