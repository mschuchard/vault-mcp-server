"""unit test utilities"""

from fastmcp import FastMCP, Client
from fastmcp.client.transports import FastMCPTransport

from mcp_bindings import server, provider


def mcp_client() -> Client[FastMCPTransport]:
    """bootstrap mcp server and return client for tests"""
    mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)
    provider.provider(mcp)
    return Client(mcp)
