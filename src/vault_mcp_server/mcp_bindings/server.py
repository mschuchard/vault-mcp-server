"""mcp server support"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Literal
import os

from fastmcp import FastMCP
from fastmcp.server.transforms.search import BM25SearchTransform
from fastmcp.server.middleware.caching import ResponseCachingMiddleware, ListToolsSettings, ReadResourceSettings
import hvac

from vault_mcp_server.mcp_bindings import provider
from vault_mcp_server.vault import client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """manage mcp server lifecycle with type-safe context"""
    # construct vault client
    vault_client: hvac.Client = client.client()
    # initialize resources on startup
    try:
        yield {
            'client': vault_client,
            'database': vault_client.secrets.database,
            'kv2': vault_client.secrets.kv.v2,
            'identity': vault_client.secrets.identity,
            'pki': vault_client.secrets.pki,
            'sys': vault_client.sys,
            'transit': vault_client.secrets.transit,
        }
    finally:
        # cleanup resources on shutdown
        if hasattr(vault_client.adapter, 'close'):
            vault_client.adapter.close()


def run(transport: Literal['stdio', 'streamable-http', 'sse']) -> None:
    """load and execute fastmcp server"""
    # initialize fastmcp object
    mcp: FastMCP = FastMCP(
        name='Vault',
        instructions=(
            'This server provides live, authoritative access to a running HashiCorp Vault '
            'instance — secret engines, authentication methods, ACL policies, audit devices, '
            'PKI, transit, database secrets engines, identity, and raft storage. '
            'For ANY question about the current state or configuration of Vault (what is '
            'enabled, mounted, configured, or stored), use this server rather than local '
            'shell commands, the vault CLI, or prior knowledge — local tooling may not '
            'reflect the actual server state or have equivalent credentials. '
            'Start with the search_vault_tools tool to find the relevant operation, then '
            'invoke it via call_vault_tool.'
        ),
        lifespan=server_lifespan,
        transforms=[
            BM25SearchTransform(
                max_results=10,
                search_tool_name='search_vault_tools',
                call_tool_name='call_vault_tool',
            )
        ],
    )

    # add response caching middleware
    cache_ttl: int = int(os.getenv('CACHE_TTL', '60'))
    mcp.add_middleware(
        ResponseCachingMiddleware(
            # cache list operations
            list_tools_settings=ListToolsSettings(ttl=cache_ttl),
            list_resources_settings=ListToolsSettings(ttl=cache_ttl),
            # cache resource reads
            read_resource_settings=ReadResourceSettings(ttl=cache_ttl),
        )
    )

    # load integrations
    provider.provider(mcp)
    # run mcp server
    mcp.run(transport=transport)
