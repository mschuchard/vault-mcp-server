"""mcp vault integration provider"""

from fastmcp import FastMCP

from vault.secret import kv2, transit
from vault.sys import audit, auth, policy, secret


def resource_provider(mcp: FastMCP) -> None:
    """define implemented resource integrations"""
    # lists of enabled and configured
    mcp.add_resource_fn(
        audit.list,
        uri='audit://devices',
        name='Enabled Audit Devices',
        description='List the available enabled Vault audit devices',
        mime_type='application/json',
    )
    mcp.add_resource_fn(
        auth.list,
        uri='auth://engines',
        name='Enabled Authentication Engines',
        description='List the available enabled Vault authentication engines',
        mime_type='application/json',
    )
    mcp.add_resource_fn(
        policy.list,
        uri='sys://policies',
        name='Configured ACL Policies',
        description='List the available configured Vault ACL policies',
        mime_type='application/json',
    )
    mcp.add_resource_fn(
        secret.list,
        uri='secret://engines',
        name='Enabled Secret Engines',
        description='List the available enabled Vault secret engines',
        mime_type='application/json',
    )


def tool_provider(mcp: FastMCP) -> None:
    """define implemented tool integrations"""
    # base annotations
    global_annotations: dict[str, bool] = {'openWorldHint': True}
    cu_annotations: dict[str, bool] = {} | global_annotations
    rl_annotations: dict[str, bool] = {'readOnlyHint': True, 'destructiveHint': False} | global_annotations
    del_annotations: dict[str, bool] = {'destructiveHint': True} | global_annotations
    # audit
    mcp.add_tool(fn=audit.enable, name='audit-device-enable', annotations=cu_annotations)
    mcp.add_tool(fn=audit.disable, name='audit-device-disable', annotations=del_annotations)
    mcp.add_tool(fn=audit.list, name='audit-devices-list', annotations=rl_annotations)
    # auth
    mcp.add_tool(fn=auth.enable, name='authentication-engine-enable', annotations=cu_annotations)
    mcp.add_tool(fn=auth.disable, name='authentication-engine-disable', annotations=del_annotations)
    mcp.add_tool(fn=auth.list, name='authentication-engines-list', annotations=rl_annotations)
    # kv2
    mcp.add_tool(fn=kv2.create_update, name='kv2-create-or-update', annotations=cu_annotations)
    mcp.add_tool(fn=kv2.delete, name='kv2-delete', annotations=del_annotations)
    mcp.add_tool(fn=kv2.read, name='kv2-read', annotations=rl_annotations)
    mcp.add_tool(fn=kv2.list, name='kv2-list', annotations=rl_annotations)
    mcp.add_tool(fn=kv2.metadata, name='kv2-metadata-and-versions', annotations=rl_annotations)
    mcp.add_tool(fn=kv2.patch, name='kv2-patch', annotations=cu_annotations)
    # policy
    mcp.add_tool(fn=policy.create, name='policy-write', annotations=cu_annotations)
    mcp.add_tool(fn=policy.delete, name='policy-delete', annotations=del_annotations)
    mcp.add_tool(fn=policy.read, name='policy-read', annotations=rl_annotations)
    mcp.add_tool(fn=policy.list, name='policy-list', annotations=rl_annotations)
    # secret
    mcp.add_tool(fn=secret.enable, name='secret-engine-enable', annotations=cu_annotations)
    mcp.add_tool(fn=secret.disable, name='secret-engine-disable', annotations=del_annotations)
    mcp.add_tool(fn=secret.list, name='secret-engine-list', annotations=rl_annotations)
    # transit
    mcp.add_tool(fn=transit.create, name='transit-engine-encryption-key-create', annotations=cu_annotations)
    mcp.add_tool(fn=transit.read, name='transit-engine-encryption-key-read', annotations=rl_annotations)
    mcp.add_tool(fn=transit.list, name='transit-engine-encryption-keys-list', annotations=rl_annotations)
    mcp.add_tool(fn=transit.delete, name='transit-engine-encryption-key-delete', annotations=del_annotations)
    mcp.add_tool(fn=transit.rotate, name='transit-engine-encryption-key-rotate', annotations=cu_annotations)
    mcp.add_tool(fn=transit.encrypt, name='transit-engine-encrypt-plaintext', annotations=cu_annotations)
    mcp.add_tool(fn=transit.decrypt, name='transit-engine-decrypt-ciphertext', annotations=cu_annotations)
    mcp.add_tool(fn=transit.generate, name='transit-engine-generate-random-bytes', annotations=cu_annotations)


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
