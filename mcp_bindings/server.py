"""mcp server support"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Literal

from fastmcp import FastMCP
import hvac

from mcp_bindings import provider
from vault import client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """manage mcp server lifecycle with type-safe context"""
    # construct vault client
    vault_client: hvac.Client = client.client()
    # initialize resources on startup
    yield {'client': vault_client, 'kv2': vault_client.secrets.kv.v2, 'sys': vault_client.sys, 'transit': vault_client.secrets.transit}


def run(transport: Literal['stdio', 'streamable-http', 'sse']) -> None:
    """initialize fastmcp object"""
    mcp: FastMCP = FastMCP(name='Vault', lifespan=server_lifespan)
    # load integrations
    provider.provider(mcp)
    # run mcp server
    mcp.run(transport=transport)
