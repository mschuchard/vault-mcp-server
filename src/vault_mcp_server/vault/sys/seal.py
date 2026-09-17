"""vault seal"""

from fastmcp import Context


async def read_status(ctx: Context) -> dict:
    """read the seal status of the vault server

    Returns fields such as sealed, t (unseal threshold), n (number of key shares),
    progress, type, and version.
    """
    return ctx.request_context.lifespan_context['sys'].read_seal_status()
