"""fastmcp dev run issues workarounds"""

from fastmcp import FastMCP

from mcp_bindings import provider, server

mcp = FastMCP(name='Vault', lifespan=server.server_lifespan)
provider.provider(mcp)
