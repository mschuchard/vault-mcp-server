"""mcp server for vault"""

from mcp_bindings import server

if __name__ == '__main__':
    server.run(transport='stdio')
