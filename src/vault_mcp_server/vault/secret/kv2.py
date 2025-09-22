"""vault kv2"""

from typing import Annotated
from fastmcp import Context
import hvac.exceptions


def create_update(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secrets to create/update.'] = '',
    secret: Annotated[
        dict,
        'Specifies keys, paired with associated values, to be held at the given location. Multiple key/value pairs can be specified, and all will be returned on a read operation.',
    ] = {},
) -> dict:
    """create or update a key-value version 2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
    )['data']


def delete(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to delete.'] = '',
) -> dict[str, bool]:
    """delete a key-value version 2 secret from vault"""
    return {'success': ctx.request_context.lifespan_context['kv2'].delete_metadata_and_all_versions(mount_point=mount, path=path).ok}


def undelete(
    ctx: Context,
    versions: Annotated[list[int], 'The versions to undelete. The versions will be restored and their data will be returned on normal get requests.'],
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to undelete.'] = '',
) -> dict[str, bool]:
    """undelete a key-value version 2 secret in vault"""
    return {'success': ctx.request_context.lifespan_context['kv2'].undelete_secret_versions(mount_point=mount, path=path, versions=versions).ok}


async def read(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to read.'] = '',
) -> dict:
    """read a key-value version 2 secret from a vault"""
    return ctx.request_context.lifespan_context['kv2'].read_secret_version(mount_point=mount, path=path)['data']['data']


async def list(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secrets to list.'] = '',
) -> list[str]:
    """list the key-value version 2 secrets in vault"""
    try:
        return ctx.request_context.lifespan_context['kv2'].list_secrets(mount_point=mount, path=path)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


async def read_secret_metadata(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret metadata to read.'] = '',
) -> dict:
    """read the metadata and versions for a key-value version 2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].read_secret_metadata(mount_point=mount, path=path)['data']


def patch(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secrets to patch.'] = '',
    secret: Annotated[
        dict,
        'Specifies keys, paired with associated values, to be held at the given location. Multiple key/value pairs can be specified, and all will be returned on a read operation.',
    ] = {},
) -> dict:
    """update the data of a key-value version 2 secret in vault without overwriting the current secret data"""
    return ctx.request_context.lifespan_context['kv2'].patch(
        mount_point=mount,
        path=path,
        secret=secret,
    )['data']
