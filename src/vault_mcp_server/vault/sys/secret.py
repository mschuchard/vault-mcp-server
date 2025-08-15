"""vault secret engine"""

from fastmcp import Context


def enable(
    ctx: Context, engine: str, mount: str | None = None, config: dict | None = None, options: dict | None = None, local: bool = False, seal_wrap: bool = False
) -> dict[str, bool | None]:
    """enable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_secrets_engine(
        backend_type=engine, path=mount, config=config, options=options, local=local, seal_wrap=seal_wrap
    )
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(ctx: Context, mount: str) -> dict[str, bool | None]:
    """disable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list(ctx: Context) -> dict:
    """list enabled vault secret engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_mounted_secrets_engines()['data']
    return engines if engines else {}
