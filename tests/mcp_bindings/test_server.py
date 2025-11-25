"""test mcp server support"""

from unittest.mock import patch

from vault_mcp_server.mcp_bindings import server


def test_server() -> None:
    with patch('vault_mcp_server.mcp_bindings.server.run') as mock_run:
        server.run(transport='stdio')
        mock_run.assert_called_once_with(transport='stdio')
