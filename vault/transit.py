"""vault transit"""

import json
import base64

from mcp.server.fastmcp import Context


def create(ctx: Context, name: str, mount: str = 'transit') -> str:
    """create a transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].create_key(name=name, mount_point='transit').text


async def read(ctx: Context, name: str, mount: str = 'transit') -> str:
    """read a transit encryption key from vault"""
    return json.dumps(ctx.request_context.lifespan_context['transit'].read_key(name=name, mount_point=mount))


async def list(ctx: Context, mount: str = 'transit') -> str:
    """list transit encryption keys in vault"""
    return json.dumps(ctx.request_context.lifespan_context['transit'].list_keys(mount_point=mount)['data']['keys'])


def delete(ctx: Context, name: str, mount: str = 'transit') -> str:
    """delete transit encryption key from vault"""
    return ctx.request_context.lifespan_context['transit'].delete_key(name=name, mount_point=mount).text


def rotate(ctx: Context, name: str, mount: str = 'transit') -> str:
    """rotate transit encryption key in vault"""
    return ctx.request_context.lifespan_context['transit'].rotate_key(name=name, mount_point=mount).text


def encrypt(ctx: Context, name: str, text: str, mount: str = 'transit') -> str:
    """encrypt plaintext with transit encryption key"""
    return ctx.request_context.lifespan_context['transit'].encrypt_data(name=name, plaintext=base64.b64encode(text.encode()), mount_point=mount)['data'][
        'ciphertext'
    ]


def decrypt(ctx: Context, name: str, text: str, mount: str = 'transit') -> str:
    """decrypt plaintext with transit encryption key"""
    return json.dumps(ctx.request_context.lifespan_context['transit'].decrypt_data(name=name, ciphertext=text, mount_point=mount)['data']['plaintext'])


def generate(ctx: Context, num_bytes: int, mount: str = 'transit') -> str:
    """generate random bytes"""
    return ctx.request_context.lifespan_context['transit'].generate_random_bytes(n_bytes=num_bytes, mount_point=mount)['data']['random_bytes']
