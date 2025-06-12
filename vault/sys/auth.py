"""vault authentication engine"""

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None) -> dict[str, bool]:
    """enable a vault authentication engine"""
    return {'success': ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, path=mount).ok}


def disable(ctx: Context, mount: str) -> dict[str, bool]:
    """disable a vault authentication engine"""
    return {'success': ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount).ok}


async def list(ctx: Context) -> dict:
    """list enabled vault authentication engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_auth_methods()['data']
    return engines if len(engines) > 0 else {}
