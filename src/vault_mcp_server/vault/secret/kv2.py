"""vault kv2"""

from typing import Annotated, Optional

from fastmcp import Context
import hvac.exceptions


def configure(
    ctx: Context,
    max_versions: Annotated[int, 'The number of versions to keep per key.'] = 10,
    cas_required: Annotated[Optional[bool], 'If true, all keys will require the cas parameter to be set on all write requests.'] = None,
    delete_version_after: Annotated[str, 'Specifies the length of time before a version is deleted. Accepts Go duration format string.'] = '0s',
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
) -> dict[str, bool]:
    """configure backend level settings that are applied to every key in the key-value version 2 store in vault"""
    return {
        'success': ctx.request_context.lifespan_context['kv2']
        .configure(
            max_versions=max_versions,
            cas_required=cas_required,
            delete_version_after=delete_version_after,
            mount_point=mount,
        )
        .ok
    }


def read_configuration(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
) -> dict:
    """read the KV Version 2 configuration"""
    return ctx.request_context.lifespan_context['kv2'].read_configuration(
        mount_point=mount,
    )['data']


def create_update(
    ctx: Context,
    mount: Annotated[str, 'The "path" the key-value version 2 secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secrets to create/update.'] = '',
    secret: Annotated[
        dict,
        'Specifies keys, paired with associated values, to be held at the given location. Multiple key/value pairs can be specified, and all will be returned on a read operation.',
    ] = {},
    cas: Annotated[
        Optional[int],
        'Set the "cas" value to use a Check-And-Set operation. If not set the write will be allowed. If set to 0 a write will only be allowed if the key doesn\'t exist.',
    ] = None,
) -> dict:
    """create or update a key-value version 2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
        cas=cas,
    )['data']


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


async def read(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to read.'] = '',
    version: Annotated[Optional[int], 'Specifies the version to return. If not set the latest version is returned.'] = None,
    raise_on_deleted_version: Annotated[bool, 'If True, raise exception when the requested version has been deleted.'] = False,
) -> dict:
    """read a key-value version 2 secret from a vault"""
    response = ctx.request_context.lifespan_context['kv2'].read_secret_version(
        mount_point=mount,
        path=path,
        version=version,
        raise_on_deleted_version=raise_on_deleted_version,
    )
    return response['data']['data']


def delete_latest_version_of_secret(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to delete. This is specified as part of the URL.'] = '',
) -> dict[str, bool]:
    """issue a soft delete of the key value version 2 secret's latest version at the specified location in vault"""
    return {
        'success': ctx.request_context.lifespan_context['kv2']
        .delete_latest_version_of_secret(
            mount_point=mount,
            path=path,
        )
        .ok
    }


def delete_secret_versions(
    ctx: Context,
    versions: Annotated[
        list[int], 'The versions to be deleted. The versioned data will not be deleted, but it will no longer be returned in normal get requests.'
    ],
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to delete. This is specified as part of the URL.'] = '',
) -> dict[str, bool]:
    """issue a soft delete of the specified versions of the key value version 2 secret in vault"""
    return {
        'success': ctx.request_context.lifespan_context['kv2']
        .delete_secret_versions(
            mount_point=mount,
            path=path,
            versions=versions,
        )
        .ok
    }


def undelete(
    ctx: Context,
    versions: Annotated[list[int], 'The versions to undelete. The versions will be restored and their data will be returned on normal get requests.'],
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to undelete.'] = '',
) -> dict[str, bool]:
    """undelete a key-value version 2 secret in vault"""
    return {'success': ctx.request_context.lifespan_context['kv2'].undelete_secret_versions(mount_point=mount, path=path, versions=versions).ok}


def destroy(
    ctx: Context,
    versions: Annotated[list[int], 'The versions to destroy. Their data will be permanently deleted.'],
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to destroy. This is specified as part of the URL.'] = '',
) -> dict[str, bool]:
    """permanently remove the specified version data for the provided path and prevent the underlying data from being read in vault"""
    return {
        'success': ctx.request_context.lifespan_context['kv2']
        .destroy_secret_versions(
            mount_point=mount,
            path=path,
            versions=versions,
        )
        .ok
    }


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


def update_metadata(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret.'] = '',
    max_versions: Annotated[Optional[int], 'The number of versions to keep per key. If not set, the backend configured max version is used.'] = None,
    cas_required: Annotated[
        Optional[bool], "If true, the key will require the cas parameter to be set on all write requests. If false, the backend's configuration will be used."
    ] = None,
    delete_version_after: Annotated[
        Optional[str],
        'Set the delete_version_after value to a duration to specify when to delete a version after creation/update. Accepts Go duration format string.',
    ] = None,
    custom_metadata: Annotated[Optional[dict], 'A map of arbitrary string to string valued user-provided metadata meant to describe the secret.'] = None,
) -> dict[str, bool]:
    """update metadata for the secret at the specified path"""
    return {
        'success': ctx.request_context.lifespan_context['kv2']
        .update_metadata(
            mount_point=mount,
            path=path,
            max_versions=max_versions,
            cas_required=cas_required,
            delete_version_after=delete_version_after,
            custom_metadata=custom_metadata,
        )
        .ok
    }


def delete(
    ctx: Context,
    mount: Annotated[str, 'The "path" the secret engine was mounted on.'] = 'secret',
    path: Annotated[str, 'Specifies the path of the secret to delete.'] = '',
) -> dict[str, bool]:
    """delete a key-value version 2 secret from vault"""
    return {'success': ctx.request_context.lifespan_context['kv2'].delete_metadata_and_all_versions(mount_point=mount, path=path).ok}
