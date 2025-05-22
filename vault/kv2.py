"""vault kv2"""

import json

from mcp.server.fastmcp import Context


def write(ctx: Context, mount: str = 'secret', path: str = '', secret: dict = {}) -> str:
    """write a kv2 secret to vault"""
    return json.dumps(
        ctx.request_context.lifespan_context['kv2'].create_or_update_secret(
            mount_point=mount,
            path=path,
            secret=secret,
        )
    )


def delete(ctx: Context, mount: str = 'secret', path: str = '') -> str:
    """delete a kv2 secret from vault"""
    return ctx.request_context.lifespan_context['kv2'].delete_metadata_and_all_versions(mount_point=mount, path=path).text


async def read(ctx: Context, mount: str = 'secret', path: str = '') -> str:
    """read a kv2 secret from a vault"""
    return json.dumps(ctx.request_context.lifespan_context['kv2'].read_secret_version(mount_point=mount, path=path)['data'])


async def list(ctx: Context, mount: str = 'secret', path: str = '') -> str:
    """list the kv2 secrets in vault"""
    return json.dumps(ctx.request_context.lifespan_context['kv2'].list_secrets(mount_point=mount, path=path)['data']['keys'])
