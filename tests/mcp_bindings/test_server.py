"""test mcp server support"""

from mcp_bindings import server


def test_run() -> None:
    server.run(transport='stdio')
