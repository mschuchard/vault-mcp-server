"""fastmcp dev run issues workarounds"""

from fastmcp import FastMCP, Client
from fastmcp.client.transports import FastMCPTransport

from vault_mcp_server.mcp_bindings import provider, server

mcp = FastMCP(name='Vault', lifespan=server.server_lifespan)
provider.provider(mcp)


def mcp_client() -> Client[FastMCPTransport]:
    """bootstrap mcp server and return client for tests"""
    mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)
    provider.provider(mcp)
    return Client(mcp)
