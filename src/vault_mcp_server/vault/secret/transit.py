"""vault transit"""

import base64
from typing import Annotated

from fastmcp import Context
import hvac.exceptions


def create(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to create.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
    type: Annotated[str | None, 'Specifies the type of encryption key to create.'] = None,
    convergent_encryption: Annotated[
        bool | None,
        'If enabled, the key will support convergent encryption, where the same plaintext creates the same ciphertext. This requires derived to be set to true. When enabled, each encryption(/decryption/rewrap/datakey) operation will derive a nonce value rather than randomly generate it.',
    ] = None,
    derived: Annotated[
        bool | None,
        'Specifies if key derivation is to be used. If enabled, all encrypt/decrypt requests to this named key must provide a context which is used for key derivation.',
    ] = None,
    exportable: Annotated[
        bool | None,
        'Enables keys to be exportable. This allows for all the valid keys in the key ring to be exported. Once set, this cannot be disabled.',
    ] = None,
    allow_plaintext_backup: Annotated[
        bool | None,
        'If set, enables taking backup of named key in the plaintext format. Once set, this cannot be disabled.',
    ] = None,
    auto_rotate_period: Annotated[str | None, 'The period at which this key should be rotated automatically.'] = None,
) -> dict:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(
        name=name,
        mount_point=mount,
        key_type=type,
        convergent_encryption=convergent_encryption,
        derived=derived,
        exportable=exportable,
        allow_plaintext_backup=allow_plaintext_backup,
        auto_rotate_period=auto_rotate_period,
    )['data']


def update_config(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to update configuration for.'],
    min_decryption_version: Annotated[
        int | None,
        'Specifies the minimum version of ciphertext allowed to be decrypted. Adjusting this as part of a key rotation policy can prevent old copies of ciphertext from being decrypted, should they fall into the wrong hands. For signatures, this value controls the minimum version of signature that can be verified against. For HMACs, this controls the minimum version of a key allowed to be used as the key for verification.',
    ] = None,
    min_encryption_version: Annotated[
        int | None,
        'Specifies the minimum version of the key that can be used to encrypt plaintext, sign payloads, or generate HMACs. Must be 0 (which will use the latest version) or a value greater than or equal to the min_decryption_version.',
    ] = None,
    deletion_allowed: Annotated[bool | None, 'Specifies if the key is allowed to be deleted.'] = None,
    exportable: Annotated[
        bool | None, 'Enables keys to be exportable. This allows for all the valid keys in the key ring to be exported. Once set, this cannot be disabled.'
    ] = None,
    allow_plaintext_backup: Annotated[
        bool | None,
        'If set, enables taking backup of named key in the plaintext format. Once set, this cannot be disabled.',
    ] = None,
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
    auto_rotate_period: Annotated[str | None, 'The period at which this key should be rotated automatically.'] = None,
) -> dict:
    """update the configuration of a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].update_key_configuration(
        name=name,
        min_decryption_version=min_decryption_version,
        min_encryption_version=min_encryption_version,
        deletion_allowed=deletion_allowed,
        exportable=exportable,
        allow_plaintext_backup=allow_plaintext_backup,
        mount_point=mount,
        auto_rotate_period=auto_rotate_period,
    )['data']


async def read(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to read.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
) -> dict:
    """read a transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount)['data']


async def list_(ctx: Context, mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit') -> list:
    """list the transit encryption keys in vault"""
    try:
        return ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to delete.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
) -> dict[str, bool]:
    """delete a transit encryption key from vault"""
    return {'success': ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount).ok}


def rotate(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to rotate.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
) -> dict:
    """rotate a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].rotate_key(name=name, mount_point=mount)['data']


def encrypt(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to encrypt against.'],
    text: Annotated[str, 'Specifies plaintext to be encoded.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
    context: Annotated[
        str | None, 'Specifies the base64 encoded context for key derivation. This is required if key derivation is enabled for this key.'
    ] = None,
    key_version: Annotated[
        int | None,
        "Specifies the version of the key to use for encryption. If not set, uses the latest version. Must be greater than or equal to the key's min_encryption_version, if set.",
    ] = None,
    nonce: Annotated[
        str | None,
        'Specifies the base64 encoded nonce value. This must be provided if convergent encryption is enabled for this key and the key was generated with Vault 0.6.1. Not required for keys created in 0.6.2+. The value must be exactly 96 bits (12 bytes) long and the user must ensure that for any given context (and thus, any given encryption key) this nonce value is never reused.',
    ] = None,
    associated_data: Annotated[
        str | None,
        'Specifies base64 encoded associated data (also known as additional data or AAD) to also be authenticated with AEAD ciphers (aes128-gcm96, aes256-gcm, and chacha20-poly1305).',
    ] = None,
    type: Annotated[
        str | None,
        'This parameter is required when encryption key is expected to be created. Specifies the type of key to create.',
    ] = None,
    convergent_encryption: Annotated[
        bool | None,
        'This parameter will only be used when a key is expected to be created. Whether to support convergent encryption. This is only supported when using a key with key derivation enabled and will require all requests to carry both a context and 96-bit (12-byte) nonce. The given nonce will be used in place of a randomly generated nonce. As a result, when the same context and nonce are supplied, the same ciphertext is generated. It is very important when using this mode that you ensure that all nonces are unique for a given context. Failing to do so will severely impact the ciphertext security.',
    ] = None,
) -> str:
    """encrypt plaintext with a vault transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].encrypt_data(
        name=name,
        plaintext=base64.urlsafe_b64encode(text.encode()).decode(),
        mount_point=mount,
        context=context,
        key_version=key_version,
        nonce=nonce,
        associated_data=associated_data,
        type=type,
        convergent_encryption=convergent_encryption,
    )['data']['ciphertext']


def decrypt(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the encryption key to decrypt against.'],
    text: Annotated[str, 'The ciphertext to decrypt.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
    context: Annotated[str | None, 'Specifies the base64 encoded context for key derivation. This is required if key derivation is enabled.'] = None,
    nonce: Annotated[
        str | None,
        'Specifies a base64 encoded nonce value used during encryption. Must be provided if convergent encryption is enabled for this key and the key was generated with Vault 0.6.1. Not required for keys created in 0.6.2+.',
    ] = None,
    associated_data: Annotated[
        str | None,
        'Specifies base64 encoded associated data (also known as additional data or AAD) to also be authenticated with AEAD ciphers (aes128-gcm96, aes256-gcm, and chacha20-poly1305).',
    ] = None,
) -> str:
    """decrypt ciphertext with a vault transit encryption key"""
    return base64.b64decode(
        ctx.request_context.lifespan_context['transit']
        .decrypt_data(name=name, ciphertext=text, mount_point=mount, context=context, nonce=nonce, associated_data=associated_data)['data']['plaintext']
        .encode()
    ).decode()


def generate(
    ctx: Context,
    num_bytes: Annotated[int, 'Specifies the number of bytes to return.'],
    mount: Annotated[str, 'The "path" the transit engine was mounted on.'] = 'transit',
) -> str:
    """generate random bytes through the vault transit engine"""
    return ctx.request_context.lifespan_context['transit'].generate_random_bytes(n_bytes=num_bytes, mount_point=mount)['data']['random_bytes']
