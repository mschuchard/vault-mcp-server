"""test mcp server support"""

from mcp_bindings import server


def test_server() -> None:
    server.run(transport='stdio')
