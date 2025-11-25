"""vault authentication engine"""

from typing import Annotated
from fastmcp import Context


def enable(
    ctx: Context,
    method_type: Annotated[str, 'The name of the authentication method type, such as "github" or "userpass".'],
    path: Annotated[str | None, 'The path to mount the method on. If not provided, defaults to the value of the "method_type" argument.'] = None,
    description: Annotated[str | None, 'Human-friendly description of the auth method.'] = None,
    config: Annotated[dict | None, 'Configuration options for this auth method.'] = None,
    plugin_name: Annotated[str | None, 'The name of the auth plugin to use based from the name in the plugin catalog. Applies only to plugin methods.'] = None,
    local: Annotated[
        bool,
        '(Vault enterprise only) Specifies if the auth method is a local only. Local auth methods are not replicated nor (if a secondary) removed by replication.',
    ] = False,
) -> dict[str, bool | str | None]:
    """enable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_auth_method(
        method_type=method_type, description=description, config=config, plugin_name=plugin_name, local=local, path=path
    )
    return {'success': result.ok, 'error': str(result.text) if not result.ok else None}


def disable(ctx: Context, path: Annotated[str, 'The path the method was mounted on.']) -> dict[str, bool | str | None]:
    """disable a vault authentication engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_auth_method(path=path)
    return {'success': result.ok, 'error': str(result.text) if not result.ok else None}


async def list_(ctx: Context) -> dict:
    """list enabled vault authentication engines"""
    result = ctx.request_context.lifespan_context['sys'].list_auth_methods()
    return result.get('data', {}) if isinstance(result, dict) else {}


async def read(ctx: Context, path: Annotated[str, 'The path the method was mounted on.']) -> dict:
    """read the given auth path's configuration (tuning parameters)

    This endpoint requires sudo capability on the final path, but the same
    functionality can be achieved without sudo via sys/mounts/auth/[auth-path]/tune.
    """
    result = ctx.request_context.lifespan_context['sys'].read_auth_method_tuning(path=path)
    return result if isinstance(result, dict) else {}


def tune(
    ctx: Context,
    path: Annotated[str, 'The path the method was mounted on.'],
    default_lease_ttl: Annotated[int | None, 'Specifies the default time-to-live. If set on a specific auth path, this overrides the global default.'] = None,
    max_lease_ttl: Annotated[int | None, 'The maximum time-to-live. If set on a specific auth path, this overrides the global default.'] = None,
    description: Annotated[str | None, 'Specifies the description of the mount. This overrides the current stored value, if any.'] = None,
    audit_non_hmac_request_keys: Annotated[
        list | None, "Specifies the list of keys that will not be HMAC'd by audit devices in the request data object."
    ] = None,
    audit_non_hmac_response_keys: Annotated[
        list | None, "Specifies the list of keys that will not be HMAC'd by audit devices in the response data object."
    ] = None,
    listing_visibility: Annotated[str | None, 'Specifies whether to show this mount in the UI-specific listing endpoint.'] = None,
    passthrough_request_headers: Annotated[list | None, 'List of headers to whitelist and pass from the request to the backend.'] = None,
) -> dict[str, bool | str | None]:
    """tune configuration parameters for a given auth path

    This endpoint requires sudo capability on the final path, but the same
    functionality can be achieved without sudo via sys/mounts/auth/[auth-path]/tune.
    """
    result = ctx.request_context.lifespan_context['sys'].tune_auth_method(
        path=path,
        default_lease_ttl=default_lease_ttl,
        max_lease_ttl=max_lease_ttl,
        description=description,
        audit_non_hmac_request_keys=audit_non_hmac_request_keys,
        audit_non_hmac_response_keys=audit_non_hmac_response_keys,
        listing_visibility=listing_visibility,
        passthrough_request_headers=passthrough_request_headers,
    )
    return {'success': result.ok if hasattr(result, 'ok') else True, 'error': str(result.text) if hasattr(result, 'text') and not result.ok else None}
