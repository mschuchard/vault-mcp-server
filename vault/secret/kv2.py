"""vault kv2"""

from fastmcp import Context
import hvac.exceptions


def create_update(ctx: Context, mount: str = 'secret', path: str = '', secret: dict = {}) -> dict:
    """create or update a key-value version 2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
    )['data']


def delete(ctx: Context, mount: str = 'secret', path: str = '') -> dict[str, bool]:
    """delete a key-value version 2 secret from vault"""
    return {'success': ctx.request_context.lifespan_context['kv2'].delete_metadata_and_all_versions(mount_point=mount, path=path).ok}


async def read(ctx: Context, mount: str = 'secret', path: str = '') -> dict:
    """read a key-value version 2 secret from a vault"""
    return ctx.request_context.lifespan_context['kv2'].read_secret_version(mount_point=mount, path=path)['data']['data']


async def list(ctx: Context, mount: str = 'secret', path: str = '') -> list[str]:
    """list the key-value version 2 secrets in vault"""
    try:
        return ctx.request_context.lifespan_context['kv2'].list_secrets(mount_point=mount, path=path)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


async def metadata(ctx: Context, mount: str = 'secret', path: str = '') -> dict:
    """read the metadata and versions for a key-value version 2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].read_secret_metadata(mount_point=mount, path=path)['data']


async def patch(ctx: Context, mount: str = 'secret', path: str = '', secret: dict = {}) -> dict:
    """update the data of a key-value version 2 secret in vault without overwriting the current secret data"""
    return ctx.request_context.lifespan_context['kv2'].patch(
        mount_point=mount,
        path=path,
        secret=secret,
    )['data']
