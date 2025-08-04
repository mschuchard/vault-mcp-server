"""test mcp server support"""

import pytest

from mcp_bindings import server


@pytest.mark.xfail(reason='This test is expected to fail because it prematurely terminates the server before it can be read.')
def test_server() -> None:
    server.run(transport='stdio')
