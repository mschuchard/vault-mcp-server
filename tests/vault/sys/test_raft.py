"""test vault raft mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
@pytest.mark.skip(reason='requires Vault to be running with the Raft integrated storage backend')
async def test_raft_read_config() -> None:
    async with dev.client as client:
        result = await client.call_tool(name='raft-config-read')
        assert isinstance(result.data, dict)
        # read_raft_config returns data with 'config' (containing 'servers') and 'index'
        assert 'config' in result.data
        assert 'servers' in result.data['config']
        assert 'index' in result.data


@pytest.mark.asyncio
@pytest.mark.skip(reason='requires a multi-node Raft cluster - not available in single-node test environment')
async def test_raft_cluster_join() -> None:
    async with dev.client as client:
        result = await client.call_tool(
            name='raft-cluster-join',
            arguments={'leader_api_addr': 'https://vault-leader:8200'},
        )
        assert isinstance(result.data, dict)


@pytest.mark.asyncio
@pytest.mark.skip(reason='requires a multi-node Raft cluster - not available in single-node test environment')
async def test_raft_node_remove() -> None:
    async with dev.client as client:
        result = await client.call_tool(name='raft-config-read')
        servers: list[dict] = result.data['config']['servers']
        # only attempt removal when there is more than one peer
        assert len(servers) > 1, 'need at least two nodes to test peer removal'
        non_leader = next(s for s in servers if not s.get('leader'))
        result = await client.call_tool(name='raft-node-remove', arguments={'server_id': non_leader['node_id']})
        assert result.data.get('success') is True


@pytest.mark.asyncio
@pytest.mark.skip(reason='snapshot API requires Vault Enterprise')
async def test_raft_snapshot_roundtrip() -> None:
    async with dev.client as client:
        result = await client.call_tool(name='raft-snapshot-take')
        assert result.is_error is False
        assert isinstance(result.data.get('snapshot'), str)
        assert len(result.data['snapshot']) > 0

        snapshot_b64 = result.data['snapshot']
        result = await client.call_tool(name='raft-snapshot-restore', arguments={'snapshot': snapshot_b64})
        assert result.data.get('success') is True


@pytest.mark.asyncio
@pytest.mark.skip(reason='auto-snapshot API requires Vault Enterprise')
async def test_raft_auto_snapshot_config_lifecycle() -> None:
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
