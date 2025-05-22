"""mcp server for vault"""

from mcp_bindings import provider, server

if __name__ == '__main__':
    # load integrations
    provider.provider(server.mcp)
    # run mcp server
    server.mcp.run(transport='stdio')
