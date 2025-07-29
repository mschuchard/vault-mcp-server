"""mcp vault integration provider"""

from fastmcp import FastMCP
from fastmcp.resources import Resource

from vault.secret import kv2, transit
from vault.sys import audit, auth, policy, secret


def resource_provider(mcp: FastMCP) -> None:
    """define implemented resource integrations"""
    # lists of enabled and configured
    mcp.add_resource(
        Resource.from_function(
            fn=audit.list,
            uri='audit://devices',
            name='enabled-audit-devices',
            description='List the available enabled Vault audit devices',
            mime_type='application/json',
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=auth.list,
            uri='auth://engines',
            name='enabled-authentication-engines',
            description='List the available enabled Vault authentication engines',
            mime_type='application/json',
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=policy.list,
            uri='sys://policies',
            name='configured-acl-policies',
            description='List the available configured Vault ACL policies',
            mime_type='application/json',
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=secret.list,
            uri='secret://engines',
            name='enabled-secret-engines',
            description='List the available enabled Vault secret engines',
            mime_type='application/json',
        )
    )


def tool_provider(mcp: FastMCP) -> None:
    """define implemented tool integrations"""
    # base annotations
    global_annotations: dict[str, bool] = {'openWorldHint': True}
    cu_annotations: dict[str, bool] = {} | global_annotations
    rl_annotations: dict[str, bool] = {'readOnlyHint': True, 'destructiveHint': False} | global_annotations
    del_annotations: dict[str, bool] = {'destructiveHint': True} | global_annotations
    # audit
    mcp.tool(name_or_fn=audit.enable, name='audit-device-enable', annotations=cu_annotations)
    mcp.tool(name_or_fn=audit.disable, name='audit-device-disable', annotations=del_annotations)
    mcp.tool(name_or_fn=audit.list, name='audit-devices-list', annotations=rl_annotations)
    # auth
    mcp.tool(name_or_fn=auth.enable, name='authentication-engine-enable', annotations=cu_annotations)
    mcp.tool(name_or_fn=auth.disable, name='authentication-engine-disable', annotations=del_annotations)
    mcp.tool(name_or_fn=auth.list, name='authentication-engines-list', annotations=rl_annotations)
    # kv2
    mcp.tool(name_or_fn=kv2.create_update, name='kv2-create-or-update', annotations=cu_annotations)
    mcp.tool(name_or_fn=kv2.delete, name='kv2-delete', annotations=del_annotations)
    mcp.tool(name_or_fn=kv2.read, name='kv2-read', annotations=rl_annotations)
    mcp.tool(name_or_fn=kv2.list, name='kv2-list', annotations=rl_annotations)
    mcp.tool(name_or_fn=kv2.metadata, name='kv2-metadata-and-versions', annotations=rl_annotations)
    mcp.tool(name_or_fn=kv2.patch, name='kv2-patch', annotations=cu_annotations)
    # policy
    mcp.tool(name_or_fn=policy.create_update, name='policy-create-or-update', annotations=cu_annotations)
    mcp.tool(name_or_fn=policy.delete, name='policy-delete', annotations=del_annotations)
    mcp.tool(name_or_fn=policy.read, name='policy-read', annotations=rl_annotations)
    mcp.tool(name_or_fn=policy.list, name='policies-list', annotations=rl_annotations)
    # secret
    mcp.tool(name_or_fn=secret.enable, name='secret-engine-enable', annotations=cu_annotations)
    mcp.tool(name_or_fn=secret.disable, name='secret-engine-disable', annotations=del_annotations)
    mcp.tool(name_or_fn=secret.list, name='secret-engines-list', annotations=rl_annotations)
    # transit
    mcp.tool(name_or_fn=transit.create, name='transit-engine-encryption-key-create', annotations=cu_annotations)
    mcp.tool(name_or_fn=transit.update_config, name='transit-engine-encryption-key-update-config', annotations=cu_annotations)
    mcp.tool(name_or_fn=transit.read, name='transit-engine-encryption-key-read', annotations=rl_annotations)
    mcp.tool(name_or_fn=transit.list, name='transit-engine-encryption-keys-list', annotations=rl_annotations)
    mcp.tool(name_or_fn=transit.delete, name='transit-engine-encryption-key-delete', annotations=del_annotations)
    mcp.tool(name_or_fn=transit.rotate, name='transit-engine-encryption-key-rotate', annotations=cu_annotations)
    mcp.tool(name_or_fn=transit.encrypt, name='transit-engine-encrypt-plaintext', annotations=cu_annotations)
    mcp.tool(name_or_fn=transit.decrypt, name='transit-engine-decrypt-ciphertext', annotations=cu_annotations)
    mcp.tool(name_or_fn=transit.generate, name='transit-engine-generate-random-bytes', annotations=cu_annotations)


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
