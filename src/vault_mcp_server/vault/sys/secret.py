"""vault secret engine"""

from typing import Annotated
from fastmcp import Context


def enable(
    ctx: Context,
    engine: Annotated[str, 'The name of the backend type, such as "kv", "aws", "github", or "token".'],
    mount: Annotated[str | None, 'The path to mount the secrets engine on. If not provided, defaults to the value of the "engine" argument.'] = None,
    description: Annotated[str | None, 'A human-friendly description of the mount.'] = None,
    config: Annotated[
        dict | None,
        'Configuration options for this mount. Possible values include: default_lease_ttl (str: "5s" or "30m"), max_lease_ttl (str), audit_non_hmac_request_keys (list), audit_non_hmac_response_keys (list), listing_visibility (str: "unauth" or "hidden"), passthrough_request_headers (list).',
    ] = None,
    plugin_name: Annotated[str | None, 'The name of the plugin to use based from the name in the plugin catalog. Required for plugin backends.'] = None,
    options: Annotated[dict | None, 'Specifies mount type specific options that are passed to the backend. For KV: version (str: "2" for KV v2).'] = None,
    local: Annotated[
        bool,
        '(Vault enterprise only) Specifies if the secrets engine is local only. Local secrets engines are not replicated nor (if a secondary) removed by replication.',
    ] = False,
    seal_wrap: Annotated[bool, '(Vault enterprise only) Enable seal wrapping for the mount.'] = False,
) -> dict[str, bool | None]:
    """enable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].enable_secrets_engine(
        backend_type=engine, path=mount, description=description, config=config, plugin_name=plugin_name, options=options, local=local, seal_wrap=seal_wrap
    )
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def disable(
    ctx: Context, mount: Annotated[str, 'The path where the secrets engine is mounted. This is specified as part of the URL.']
) -> dict[str, bool | None]:
    """disable a vault secret engine"""
    result = ctx.request_context.lifespan_context['sys'].disable_secrets_engine(path=mount)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


async def list_(ctx: Context) -> dict:
    """list enabled vault secret engines"""
    engines: dict = ctx.request_context.lifespan_context['sys'].list_mounted_secrets_engines()['data']
    return engines if engines else {}


def move(
    ctx: Context,
    from_path: Annotated[str, 'Specifies the previous mount point of the secrets engine.'],
    to_path: Annotated[str, 'Specifies the new destination mount point for the secrets engine.'],
) -> dict[str, bool | None]:
    """move an already-mounted secrets engine to a new mount point"""
    result = ctx.request_context.lifespan_context['sys'].move_backend(from_path=from_path, to_path=to_path)
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def read_configuration(ctx: Context, mount: Annotated[str, 'The path where the secrets engine is mounted. This is specified as part of the URL.']) -> dict:
    """read the configuration of a mounted secrets engine. Returns the current time in seconds for each TTL, which may be the system default or a mount-specific value."""
    response = ctx.request_context.lifespan_context['sys'].read_mount_configuration(path=mount)
    return response.get('data', {}) if hasattr(response, 'get') else response


def tune_configuration(
    ctx: Context,
    mount: Annotated[str, 'The path where the secrets engine is mounted. This is specified as part of the URL.'],
    default_lease_ttl: Annotated[
        str | None,
        'Default time-to-live for secrets (e.g., "3600s", "1h"). Overrides the global default. A value of 0 is equivalent to the system default TTL.',
    ] = None,
    max_lease_ttl: Annotated[str | None, 'Maximum time-to-live for secrets (e.g., "8600s", "24h"). Overrides the global default.'] = None,
    description: Annotated[str | None, 'Human-friendly description of the mount. This overrides the current stored value.'] = None,
    audit_non_hmac_request_keys: Annotated[list | None, "List of keys that will not be HMAC'd by audit devices in the request data object."] = None,
    audit_non_hmac_response_keys: Annotated[list | None, "List of keys that will not be HMAC'd by audit devices in the response data object."] = None,
    listing_visibility: Annotated[
        str | None, 'Specifies whether to show this mount in the UI-specific listing endpoint. Valid values: "unauth" or "hidden".'
    ] = None,
    passthrough_request_headers: Annotated[list | None, 'List of headers to whitelist and pass from the request to the backend.'] = None,
    options: Annotated[dict | None, 'Specifies mount type specific options. For KV: version (str: "2" for KV v2).'] = None,
    force_no_cache: Annotated[bool | None, 'Disable caching for this mount.'] = None,
) -> dict[str, bool | None]:
    """tune configuration parameters for a mounted secrets engine"""
    result = ctx.request_context.lifespan_context['sys'].tune_mount_configuration(
        path=mount,
        default_lease_ttl=default_lease_ttl,
        max_lease_ttl=max_lease_ttl,
        description=description,
        audit_non_hmac_request_keys=audit_non_hmac_request_keys,
        audit_non_hmac_response_keys=audit_non_hmac_response_keys,
        listing_visibility=listing_visibility,
        passthrough_request_headers=passthrough_request_headers,
        options=options,
        force_no_cache=force_no_cache,
    )
    return {'success': result.ok, 'error': result.error if not result.ok else None}


def retrieve_option(
    ctx: Context,
    mount: Annotated[str, 'The mount point of the secrets engine (without trailing slash).'],
    option_name: Annotated[str, "The name of the option to retrieve from the mount's options."],
    default_value: Annotated[str | None, 'Default value to return if the option is not found.'] = None,
) -> str | None:
    """retrieve a specific option value from a mounted secrets engine's configuration"""
    return ctx.request_context.lifespan_context['sys'].retrieve_mount_option(mount_point=mount, option_name=option_name, default_value=default_value)
