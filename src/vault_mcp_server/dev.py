"""fastmcp dev run issues workarounds"""

from fastmcp import FastMCP, Client
from fastmcp.client.transports import FastMCPTransport

from vault_mcp_server.mcp_bindings import provider, server, errors

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)
provider.provider(mcp)
mcp.add_middleware(errors.VaultErrorMiddleware())
client: Client[FastMCPTransport] = Client(mcp)
