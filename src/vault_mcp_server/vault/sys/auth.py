"""vault authentication engine"""

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None, config: dict | None = None, local: bool | None = None) -> dict[str, bool | None]:
    """enable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, config=config, path=mount, local=local)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(ctx: Context, mount: str) -> dict[str, bool | None]:
    """disable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list(ctx: Context) -> dict:
    """list enabled vault authentication engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_auth_methods()['data']
    return engines if len(engines) > 0 else {}
