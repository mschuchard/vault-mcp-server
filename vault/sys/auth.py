"""vault authentication engine"""

from fastmcp import Context


def enable(ctx: Context, engine: str, mount: str | None = None) -> str:
    """enable a vault authentication engine"""
    return ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, path=mount).text


def disable(ctx: Context, mount: str) -> str:
    """disable a vault authentication engine"""
    return ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount).text


async def list(ctx: Context) -> dict:
    """list enabled vault authentication engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_auth_methods()['data']
    return engines if len(engines) > 0 else {}
