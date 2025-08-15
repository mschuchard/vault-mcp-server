"""vault audit device"""

from fastmcp import Context


def enable(ctx: Context, type: str, path: str | None = None, options: dict | None = None, local: bool | None = None) -> dict[str, bool | None]:
    """enable a vault audit device"""
    result = ctx.request_context.lifespan_context['sys'].enable_audit_device(device_type=type, path=path, options=options, local=local)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(ctx: Context, path: str) -> dict[str, bool | None]:
    """disable a vault audit device"""
    result = ctx.request_context.lifespan_context['sys'].disable_audit_device(path=path)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list(ctx: Context) -> dict:
    """list enabled vault audit devices"""
    devices: dict = ctx.request_context.lifespan_context['sys'].list_enabled_audit_devices()['data']
    return devices if devices else {}
