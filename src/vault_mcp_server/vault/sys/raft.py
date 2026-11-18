"""vault raft"""

import datetime
import os
import pathlib
import tempfile
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


def _snapshot_dir() -> pathlib.Path:
    """resolve and create the server-side directory that raft snapshots are written to and read from"""
    # snapshots contain every secret in the cluster, so the directory is owner-only and is the only location these tools can access
    directory: pathlib.Path = pathlib.Path(os.getenv('RAFT_SNAPSHOT_DIR', os.path.join(tempfile.gettempdir(), 'vault-mcp-server-snapshots'))).resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory


def _snapshot_path(filename: str) -> pathlib.Path:
    """resolve a bare snapshot file name inside the snapshot directory, rejecting anything that could escape it"""
    if filename in ('', '.', '..') or filename != os.path.basename(filename):
        raise ValueError('filename must be a bare file name without directory components')
    return _snapshot_dir() / filename


def take_snapshot(
    ctx: Context,
    filename: Annotated[
        str | None,
        'Name of the file to write inside the server snapshot directory. Defaults to a timestamped name. An existing file is never overwritten.',
    ] = None,
) -> dict[str, str | int]:
    """take a snapshot of the Raft integrated storage state, write it to a file on the server, and return the file name, path, and size in bytes"""
    if filename is None:
        filename = datetime.datetime.now(datetime.UTC).strftime('vault-raft-%Y%m%dT%H%M%SZ.snap')
    snapshot_path: pathlib.Path = _snapshot_path(filename)
    # exclusive create with owner-only permissions fails on an existing file before vault is contacted, and never overwrites it
    descriptor: int = os.open(snapshot_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, 'wb') as snapshot_file:
            # take_raft_snapshot uses a RawAdapter and returns a streaming requests.Response of raw binary data
            response = ctx.request_context.lifespan_context['sys'].take_raft_snapshot()
            try:
                # write chunk by chunk so the full snapshot is never buffered in memory
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    snapshot_file.write(chunk)
            finally:
                response.close()
    except BaseException:
        # remove the incomplete file so a later restore cannot pick up a truncated snapshot
        snapshot_path.unlink(missing_ok=True)
        raise
    return {'filename': snapshot_path.name, 'path': str(snapshot_path), 'size': snapshot_path.stat().st_size}


def restore_snapshot(
    ctx: Context,
    filename: Annotated[str, 'Name of a snapshot file inside the server snapshot directory, as returned by the raft-snapshot-take tool.'],
    force: Annotated[
        bool,
        'If true, bypass safety checks and force-restore even when the snapshot was taken from a different cluster (use with caution).',
    ] = False,
) -> dict[str, bool]:
    """restore the Raft integrated storage state from a snapshot file previously written by the raft-snapshot-take tool"""
    snapshot_path: pathlib.Path = _snapshot_path(filename)
    # reject a symlink that points outside the snapshot directory
    if snapshot_path.resolve().parent != snapshot_path.parent:
        raise ValueError('filename must refer to a file inside the snapshot directory')
    # an open file object is streamed by requests as the request body instead of being read into memory
    with snapshot_path.open('rb') as snapshot_file:
        if force:
            result = ctx.request_context.lifespan_context['sys'].force_restore_raft_snapshot(snapshot=snapshot_file)
        else:
            result = ctx.request_context.lifespan_context['sys'].restore_raft_snapshot(snapshot=snapshot_file)
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
