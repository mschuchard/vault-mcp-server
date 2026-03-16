"""vault raft"""

import base64
from typing import Annotated

from fastmcp import Context
import hvac.exceptions


async def read_config(ctx: Context) -> dict:
    """read the Raft integrated storage configuration, including the list of cluster peers"""
    return ctx.request_context.lifespan_context['sys'].read_raft_config()['data']


def join(
    ctx: Context,
    leader_api_addr: Annotated[str, 'The API address (including scheme and port) of the leader node to join (e.g. "https://vault-leader:8200").'],
    retry: Annotated[bool, 'If true, keep retrying the join until it succeeds or the node is stopped.'] = False,
    leader_ca_cert: Annotated[str | None, 'PEM-encoded CA certificate used to verify the leader TLS certificate.'] = None,
    leader_client_cert: Annotated[str | None, 'PEM-encoded client certificate for mutual TLS with the leader.'] = None,
    leader_client_key: Annotated[str | None, 'PEM-encoded private key that corresponds to leader_client_cert.'] = None,
) -> dict:
    """join the current node to an existing Raft integrated storage cluster"""
    result = ctx.request_context.lifespan_context['sys'].join_raft_cluster(
        leader_api_addr=leader_api_addr,
        retry=retry,
        leader_ca_cert=leader_ca_cert,
        leader_client_cert=leader_client_cert,
        leader_client_key=leader_client_key,
    )
    if isinstance(result, dict):
        return result.get('data', result)
    return {'joined': result.ok if hasattr(result, 'ok') else True}


def remove_node(
    ctx: Context,
    server_id: Annotated[str, 'The node ID of the Raft peer to remove from the cluster.'],
) -> dict[str, bool]:
    """remove a node from the Raft integrated storage cluster"""
    return {'success': ctx.request_context.lifespan_context['sys'].remove_raft_node(server_id=server_id).ok}


def take_snapshot(ctx: Context) -> dict[str, str]:
    """take a snapshot of the Raft integrated storage state and return it as a base64-encoded string"""
    # take_raft_snapshot uses a RawAdapter and returns a streaming requests.Response of raw binary data
    response = ctx.request_context.lifespan_context['sys'].take_raft_snapshot()
    return {'snapshot': base64.b64encode(response.content).decode()}


def restore_snapshot(
    ctx: Context,
    snapshot: Annotated[str, 'Base64-encoded snapshot data previously obtained from the raft-snapshot-take tool.'],
    force: Annotated[
        bool,
        'If true, bypass safety checks and force-restore even when the snapshot was taken from a different cluster (use with caution).',
    ] = False,
) -> dict[str, bool]:
    """restore the Raft integrated storage state from a previously taken snapshot"""
    raw: bytes = base64.b64decode(snapshot)
    if force:
        result = ctx.request_context.lifespan_context['sys'].force_restore_raft_snapshot(snapshot=raw)
    else:
        result = ctx.request_context.lifespan_context['sys'].restore_raft_snapshot(snapshot=raw)
    return {'success': result.ok}


# vault enterprise only from this point onward
async def read_auto_snapshot_status(
    ctx: Context,
    name: Annotated[str, 'The name of the auto-snapshot configuration to read status for.'],
) -> dict:
    """read the status of a named Raft auto-snapshot configuration (Vault Enterprise only)"""
    return ctx.request_context.lifespan_context['sys'].read_raft_auto_snapshot_status(name=name)['data']


async def read_auto_snapshot_config(
    ctx: Context,
    name: Annotated[str, 'The name of the auto-snapshot configuration to read.'],
) -> dict:
    """read a named Raft auto-snapshot configuration (Vault Enterprise only)"""
    return ctx.request_context.lifespan_context['sys'].read_raft_auto_snapshot_config(name=name)['data']


async def list_auto_snapshot_configs(ctx: Context) -> list[str]:
    """list all Raft auto-snapshot configurations (Vault Enterprise only)"""
    try:
        return ctx.request_context.lifespan_context['sys'].list_raft_auto_snapshot_configs()['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def create_update_auto_snapshot_config(
    ctx: Context,
    name: Annotated[str, 'The name of the auto-snapshot configuration to create or update.'],
    interval: Annotated[str, 'How often to take snapshots, as a Go duration string (e.g. "24h") or integer seconds.'],
    storage_type: Annotated[str, 'Snapshot storage backend. One of: "local", "aws-s3", "azure-blob", "google-gcs".'],
    retain: Annotated[int, 'Number of snapshots to keep. Older snapshots beyond this count are deleted.'] = 1,
    path_prefix: Annotated[str | None, 'Directory (local) or bucket prefix (cloud) where snapshots are written.'] = None,
    file_prefix: Annotated[str | None, 'Filename prefix for snapshot files. Defaults to "vault-snapshot".'] = None,
    local_max_space: Annotated[int | None, 'For storage_type=local, maximum bytes to use for snapshots on disk.'] = None,
) -> dict[str, bool]:
    """create or update a named Raft auto-snapshot configuration (Vault Enterprise only)"""
    kwargs = {k: v for k, v in {'path_prefix': path_prefix, 'file_prefix': file_prefix, 'local_max_space': local_max_space}.items() if v is not None}
    result = ctx.request_context.lifespan_context['sys'].create_or_update_raft_auto_snapshot_config(
        name=name,
        interval=interval,
        storage_type=storage_type,
        retain=retain,
        **kwargs,
    )
    return {'success': result.ok}


def delete_auto_snapshot_config(
    ctx: Context,
    name: Annotated[str, 'The name of the auto-snapshot configuration to delete.'],
) -> dict[str, bool]:
    """delete a named Raft auto-snapshot configuration (Vault Enterprise only)"""
    return {'success': ctx.request_context.lifespan_context['sys'].delete_raft_auto_snapshot_config(name=name).ok}
