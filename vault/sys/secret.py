"""vault secret engine"""

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None) -> dict[str, bool]:
    """enable a vault secret engine"""
    return {'success': ctx.request_context.lifespan_context['sys'].enable_secrets_engine(backend_type=engine, path=mount).ok}


def disable(ctx: Context, mount: str) -> dict[str, bool]:
    """disable a vault secret engine"""
    return {'success': ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount).ok}


async def list(ctx: Context) -> dict:
    """list enabled vault secret engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_mounted_secrets_engines()['data']
    return engines if len(engines) > 0 else {}
