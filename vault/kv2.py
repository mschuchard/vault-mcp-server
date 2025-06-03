"""vault kv2"""

from fastmcp import Context


def create_update(ctx: Context, mount: str = 'secret', path: str = '', secret: dict = {}) -> dict:
    """create or update a kv2 secret in vault"""
    return ctx.request_context.lifespan_context['kv2'].create_or_update_secret(
        mount_point=mount,
        path=path,
        secret=secret,
    )


def delete(ctx: Context, mount: str = 'secret', path: str = '') -> str:
    """delete a kv2 secret from vault"""
    return ctx.request_context.lifespan_context['kv2'].delete_metadata_and_all_versions(mount_point=mount, path=path).text


async def read(ctx: Context, mount: str = 'secret', path: str = '') -> dict:
    """read a kv2 secret from a vault"""
    return ctx.request_context.lifespan_context['kv2'].read_secret_version(mount_point=mount, path=path)['data']['data']


async def list(ctx: Context, mount: str = 'secret', path: str = '') -> list[str]:
    """list the kv2 secrets in vault"""
    secrets: dict = ctx.request_context.lifespan_context['kv2'].list_secrets(mount_point=mount, path=path)
    return secrets['data'].get('keys', []) if secrets else []
