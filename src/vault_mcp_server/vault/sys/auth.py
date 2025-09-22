"""vault authentication engine"""

from typing import Annotated
from fastmcp import Context


def enable(
    ctx: Context,
    engine: Annotated[str, 'The name of the authentication method type, such as "github" or "token".'],
    mount: Annotated[str | None, 'The path to mount the method on. If not provided, defaults to the value of the "engine" argument.'] = None,
    config: Annotated[dict | None, 'Configuration options for this auth method.'] = None,
    local: Annotated[
        bool | None,
        '(Vault enterprise only) Specifies if the auth method is a local only. Local auth methods are not replicated nor (if a secondary) removed by replication.',
    ] = None,
) -> dict[str, bool | None]:
    """enable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_auth_method(method_type=engine, config=config, path=mount, local=local)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(
    ctx: Context, mount: Annotated[str, 'The path the method was mounted on. If not provided, defaults to the value of the "engine" argument.']
) -> dict[str, bool | None]:
    """disable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_auth_method(path=mount)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list(ctx: Context) -> dict:
    """list enabled vault authentication engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_auth_methods()['data']
    return engines if engines else {}
