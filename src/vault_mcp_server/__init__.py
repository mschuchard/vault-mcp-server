"""mcp server for vault"""

from vault_mcp_server.mcp_bindings import server


def main() -> None:
    # execute server
    server.run(transport='stdio')


if __name__ == '__main__':
    main()
