"""vault transit"""

import base64

from fastmcp import Context
import hvac.exceptions


def create(
    ctx: Context,
    name: str,
    mount: str = 'transit',
    type: str | None = None,
    convergent_encryption: bool | None = None,
    derived: bool | None = None,
    auto_rotate_period: str | None = None,
) -> dict:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(
        name=name, mount_point=mount, key_type=type, convergent_encryption=convergent_encryption, derived=derived, auto_rotate_period=auto_rotate_period
    )['data']


def update_config(
    ctx: Context, name: str, deletion_allowed: bool | None = None, exportable: bool | None = None, mount: str = 'transit', auto_rotate_period: str | None = None
) -> dict:
    """update the configuration of a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].update_key_configuration(
        name=name, deletion_allowed=deletion_allowed, exportable=exportable, mount_point=mount, auto_rotate_period=auto_rotate_period
    )['data']


async def read(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """read a transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount)['data']


async def list(ctx: Context, mount: str = 'transit') -> list:
    """list the transit encryption keys in vault"""
    try:
        return ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete(ctx: Context, name: str, mount: str = 'transit') -> dict[str, bool]:
    """delete a transit encryption key from vault"""
    return {'success': ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount).ok}


def rotate(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """rotate a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].rotate_key(name=name, mount_point=mount)['data']


def encrypt(ctx: Context, name: str, text: str, mount: str = 'transit', context: str | None = None, convergent_encryption: bool | None = None) -> str:
    """encrypt plaintext with a vault transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].encrypt_data(
        name=name, plaintext=base64.urlsafe_b64encode(text.encode()).decode(), mount_point=mount, context=context, convergent_encryption=convergent_encryption
    )['data']['ciphertext']


def decrypt(ctx: Context, name: str, text: str, mount: str = 'transit', context: str | None = None) -> str:
    """decrypt ciphertext with a vault transit encryption key"""
    return base64.b64decode(
        ctx.request_context.lifespan_context['transit']
        .decrypt_data(name=name, ciphertext=text, mount_point=mount, context=context)['data']['plaintext']
        .encode()
    ).decode()


def generate(ctx: Context, num_bytes: int, mount: str = 'transit') -> str:
    """generate random bytes through the vault transit engine"""
    return ctx.request_context.lifespan_context['transit'].generate_random_bytes(n_bytes=num_bytes, mount_point=mount)['data']['random_bytes']
