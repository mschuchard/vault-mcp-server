"""vault secret engine"""

from typing import Annotated
from fastmcp import Context


def enable(
    ctx: Context,
    engine: Annotated[str, 'The name of the backend type, such as "github" or "token".'],
    mount: Annotated[str | None, 'The path to mount the method on. If not provided, defaults to the value of the "engine" argument.'] = None,
    config: Annotated[dict | None, 'Configuration options for this secrets engine.'] = None,
    options: Annotated[dict | None, 'Specifies mount type specific options that are passed to the backend.'] = None,
    local: Annotated[
        bool,
        '(Vault enterprise only) Specifies if the secrets engine is a local only. Local secrets engines are not replicated nor (if a secondary) removed by replication.',
    ] = False,
    seal_wrap: Annotated[bool, '(Vault enterprise only) Enable seal wrapping for the mount.'] = False,
) -> dict[str, bool | None]:
    """enable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_secrets_engine(
        backend_type=engine, path=mount, config=config, options=options, local=local, seal_wrap=seal_wrap
    )
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(
    ctx: Context, mount: Annotated[str, 'The path the secrets engine was mounted on. If not provided, defaults to the value of the "engine" argument.']
) -> dict[str, bool | None]:
    """disable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list_(ctx: Context) -> dict:
    """list enabled vault secret engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_mounted_secrets_engines()['data']
    return engines if engines else {}
