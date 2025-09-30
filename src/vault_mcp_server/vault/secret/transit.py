"""vault transit"""

import base64
from typing import Annotated

from fastmcp import Context
import hvac.exceptions


def create(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to create.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
    type: Annotated[str | None, 'Specifies the type of encryption key to create.'] = None,
    convergent_encryption: Annotated[
        bool | None,
        'If enabled, the key will support convergent encryption, where the same plaintext creates the same ciphertext. This requires derived to be set to true. When enabled, each encryption(/decryption/rewrap/datakey) operation will derive a nonce value rather than randomly generate it.',
    ] = None,
    derived: Annotated[
        bool | None,
        'Specifies if key derivation is to be used. If enabled, all encrypt/decrypt requests to this named key must provide a context which is used for key derivation.',
    ] = None,
    auto_rotate_period: Annotated[str | None, 'The period at which this key should be rotated automatically.'] = None,
) -> dict:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(
        name=name, mount_point=mount, key_type=type, convergent_encryption=convergent_encryption, derived=derived, auto_rotate_period=auto_rotate_period
    )['data']


def update_config(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to update configuration for.'],
    deletion_allowed: Annotated[bool | None, 'Specifies if the key is allowed to be deleted.'] = None,
    exportable: Annotated[
        bool | None, 'Enables keys to be exportable. This allows for all the valid keys in the key ring to be exported. Once set, this cannot be disabled.'
    ] = None,
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
    auto_rotate_period: Annotated[str | None, 'The period at which this key should be rotated automatically.'] = None,
) -> dict:
    """update the configuration of a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].update_key_configuration(
        name=name, deletion_allowed=deletion_allowed, exportable=exportable, mount_point=mount, auto_rotate_period=auto_rotate_period
    )['data']


async def read(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to read.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
) -> dict:
    """read a transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount)['data']


async def list(ctx: Context, mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit') -> list:
    """list the transit encryption keys in vault"""
    try:
        return ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to delete.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
) -> dict[str, bool]:
    """delete a transit encryption key from vault"""
    return {'success': ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount).ok}


def rotate(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to rotate.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
) -> dict:
    """rotate a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].rotate_key(name=name, mount_point=mount)['data']


def encrypt(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to encrypt against.'],
    text: Annotated[str, 'Specifies plaintext to be encoded.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
    context: Annotated[
        str | None, 'Specifies the base64 encoded context for key derivation. This is required if key derivation is enabled for this key.'
    ] = None,
    convergent_encryption: Annotated[
        bool | None,
        'This parameter will only be used when a key is expected to be created. Whether to support convergent encryption. This is only supported when using a key with key derivation enabled and will require all requests to carry both a context and 96-bit (12-byte) nonce. The given nonce will be used in place of a randomly generated nonce. As a result, when the same context and nonce are supplied, the same ciphertext is generated. It is very important when using this mode that you ensure that all nonces are unique for a given context. Failing to do so will severely impact the ciphertext’s security.',
    ] = None,
) -> str:
    """encrypt plaintext with a vault transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].encrypt_data(
        name=name, plaintext=base64.urlsafe_b64encode(text.encode()).decode(), mount_point=mount, context=context, convergent_encryption=convergent_encryption
    )['data']['ciphertext']


def decrypt(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to decrypt against.'],
    text: Annotated[str, 'The ciphertext to decrypt.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
    context: Annotated[str | None, 'Specifies the base64 encoded context for key derivation. This is required if key derivation is enabled.'] = None,
) -> str:
    """decrypt ciphertext with a vault transit encryption key"""
    return base64.b64decode(
        ctx.request_context.lifespan_context['transit']
        .decrypt_data(name=name, ciphertext=text, mount_point=mount, context=context)['data']['plaintext']
        .encode()
    ).decode()


def generate(
    ctx: Context,
    num_bytes: Annotated[int, 'Specifies the number of bytes to return.'],
    mount: Annotated[str, 'The “path” the transit engine was mounted on.'] = 'transit',
) -> str:
    """generate random bytes through the vault transit engine"""
    return ctx.request_context.lifespan_context['transit'].generate_random_bytes(n_bytes=num_bytes, mount_point=mount)['data']['random_bytes']
