"""fastmcp dev run issues workarounds"""

from mcp_bindings import provider, server

mcp = server.mcp
provider.provider(mcp)
