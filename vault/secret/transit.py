"""vault transit"""

import base64

from fastmcp import Context
import hvac.exceptions


def create(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(name=name, mount_point=mount)['data']


async def read(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """read a transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount)['data']


async def list(ctx: Context, mount: str = 'transit') -> list:
    """list the transit encryption keys in vault"""
    try:
        return ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """delete a transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount)


def rotate(ctx: Context, name: str, mount: str = 'transit') -> dict:
    """rotate a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].rotate_key(name=name, mount_point=mount)['data']


def encrypt(ctx: Context, name: str, text: str, mount: str = 'transit') -> str:
    """encrypt plaintext with a vault transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].encrypt_data(name=name, plaintext=base64.b64encode(text.encode()), mount_point=mount)['data'][
        'ciphertext'
    ]


def decrypt(ctx: Context, name: str, text: str, mount: str = 'transit') -> str:
    """decrypt ciphertext with a vault transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].decrypt_data(name=name, ciphertext=text, mount_point=mount)['data']['plaintext']


def generate(ctx: Context, num_bytes: int, mount: str = 'transit') -> str:
    """generate random bytes through the vault transit engine"""
    return ctx.request_context.lifespan_context['transit'].generate_random_bytes(n_bytes=num_bytes, mount_point=mount)['data']['random_bytes']
