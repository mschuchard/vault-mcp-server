"""test vault raft mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_raft_read_config() -> None:
    async with dev.client as client:
        result = await client.call_tool(name='raft-config-read')
        assert isinstance(result.data, dict)
        # read_raft_config returns data with 'config' (containing 'servers') and 'index'
        assert 'config' in result.data
        assert 'servers' in result.data['config']
        assert 'index' in result.data


# @pytest.mark.asyncio
# async def test_raft_snapshot_roundtrip() -> None:
#    async with dev.client as client:
#        # take a snapshot
#        result = await client.call_tool(name='raft-snapshot-take')
#        assert result.is_error is False
#        assert isinstance(result.data.get('snapshot'), str)
#        assert len(result.data['snapshot']) > 0
#
#        # restore it (non-force)
#        snapshot_b64 = result.data['snapshot']
#        result = await client.call_tool(name='raft-snapshot-restore', arguments={'snapshot': snapshot_b64})
#        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_raft_auto_snapshot_config_lifecycle() -> None:
    """Test auto-snapshot config CRUD (Vault Enterprise only - skipped on OSS)."""
    async with dev.client as client:
        name = 'test-auto-snap'

        # create
        result = await client.call_tool(
            name='raft-auto-snapshot-config-create-or-update',
            arguments={
                'name': name,
                'interval': '24h',
                'storage_type': 'local',
                'retain': 3,
                'path_prefix': '/tmp/vault-snapshots',
                'file_prefix': 'vault-snap',
            },
        )
        assert result.data.get('success') is True

        # list
        result = await client.call_tool(name='raft-auto-snapshot-configs-list')
        assert name in result.data

        # read config
        result = await client.call_tool(name='raft-auto-snapshot-config-read', arguments={'name': name})
        assert result.data.get('storage_type') == 'local'
        assert result.data.get('retain') == 3

        # read status
        result = await client.call_tool(name='raft-auto-snapshot-status-read', arguments={'name': name})
        assert isinstance(result.data, dict)

        # delete
        result = await client.call_tool(name='raft-auto-snapshot-config-delete', arguments={'name': name})
        assert result.data.get('success') is True
