"""vault audit device"""

from typing import Annotated
from fastmcp import Context


def enable(
    ctx: Context,
    type: Annotated[str, 'Specifies the type of the audit device.'],
    path: Annotated[str | None, 'Specifies the path in which to enable the audit device.'] = None,
    options: Annotated[dict | None, 'Configuration options to pass to the audit device itself. This is dependent on the audit device type.'] = None,
    local: Annotated[bool | None, 'Specifies if the audit device is a local only.'] = None,
) -> dict[str, bool | None]:
    """enable a vault audit device"""
    result = ctx.request_context.lifespan_context['sys'].enable_audit_device(device_type=type, path=path, options=options, local=local)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(ctx: Context, path: Annotated[str, 'Specifies the path of the audit device to delete.']) -> dict[str, bool | None]:
    """disable a vault audit device"""
    result = ctx.request_context.lifespan_context['sys'].disable_audit_device(path=path)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list(ctx: Context) -> dict:
    """list enabled vault audit devices"""
    devices: dict = ctx.request_context.lifespan_context['sys'].list_enabled_audit_devices()['data']
    return devices if devices else {}
