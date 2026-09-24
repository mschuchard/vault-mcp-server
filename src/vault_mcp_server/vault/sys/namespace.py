"""vault namespace"""

from typing import Annotated

import hvac.exceptions
from fastmcp import Context


def create(ctx: Context, path: Annotated[str, 'Path of the namespace to create (Enterprise only).']) -> dict[str, bool]:
    """create a vault namespace"""
    return {'success': ctx.request_context.lifespan_context['sys'].create_namespace(path=path).ok}


async def list_(ctx: Context) -> list[str]:
    """list all vault namespaces (Enterprise only)"""
    try:
        return ctx.request_context.lifespan_context['sys'].list_namespaces()['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete(ctx: Context, path: Annotated[str, 'Path of the namespace to delete. Cannot delete a namespace with existing child namespaces.']) -> dict[str, bool]:
    """delete a vault namespace (Enterprise only)"""
    return {'success': ctx.request_context.lifespan_context['sys'].delete_namespace(path=path).ok}


def switch(
    ctx: Context,
    namespace: Annotated[str, 'Vault namespace path subsequent requests on this session should target. Empty string clears the active namespace.'],
) -> dict[str, str | None]:
    """switch the active vault namespace used by this server process for all subsequent requests

    This does not call the Vault API; it mutates the X-Vault-Namespace header on the shared
    client adapter in place, which every registered tool reads on its next request since they all hold a reference to the same adapter
    constructed in server_lifespan. Because this server runs over stdio (one process per client
    session), the mutation is scoped to the calling session and does not affect other sessions.
    """
    ctx.request_context.lifespan_context['client'].adapter.namespace = namespace or None
    return {'namespace': namespace or None}
