"""mcp server for vault"""

from mcp_bindings import server

if __name__ == '__main__':
    # execute server
    server.run(transport='stdio')
