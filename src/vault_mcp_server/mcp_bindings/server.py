"""mcp server support"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Literal

from fastmcp import FastMCP
import hvac

from vault_mcp_server.mcp_bindings import provider
from vault_mcp_server.vault import client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """manage mcp server lifecycle with type-safe context"""
    # construct vault client
    vault_client: hvac.Client = client.client()
    # initialize resources on startup
    yield {
        'client': vault_client,
        'database': vault_client.secrets.database,
        'kv2': vault_client.secrets.kv.v2,
        'pki': vault_client.secrets.pki,
        'sys': vault_client.sys,
        'transit': vault_client.secrets.transit,
    }


def run(transport: Literal['stdio', 'streamable-http', 'sse']) -> None:
    """load and execute fastmcp server"""
    # initialize fastmcp object
    mcp: FastMCP = FastMCP(
        name='Vault',
        instructions='This server facilitates interfacing and interactions with a Vault server. It provides tools for interacting with the secrets engines, and the system backends for authentication and authorization.',
        lifespan=server_lifespan,
    )
    # load integrations
    provider.provider(mcp)
    # run mcp server
    mcp.run(transport=transport)
