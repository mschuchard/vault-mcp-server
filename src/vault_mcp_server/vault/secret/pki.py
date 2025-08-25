"""vault pki"""

from fastmcp import Context


def generate_root(ctx: Context, type: str, common_name: str, mount: str = 'pki') -> dict:
    """generate a root certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_root(type=type, common_name=common_name, mount_point=mount)['data']
