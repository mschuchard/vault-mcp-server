"""mcp vault integration provider"""

from fastmcp import FastMCP

from vault import audit, auth, kv2, policy, secret, transit


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
    # audit
    mcp.add_tool(fn=audit.enable, name='Audit Device Enable')
    mcp.add_tool(fn=audit.disable, name='Audit Device Disable')
    mcp.add_tool(fn=audit.list, name='Audit Devices List')
    # auth
    mcp.add_tool(fn=auth.enable, name='Authentication Engine Enable')
    mcp.add_tool(fn=auth.disable, name='Authentication Engine Disable')
    mcp.add_tool(fn=auth.list, name='Authentication Engines List')
    # kv2
    mcp.add_tool(fn=kv2.write, name='KV2 Write')
    mcp.add_tool(fn=kv2.delete, name='KV2 Delete')
    mcp.add_tool(fn=kv2.read, name='KV2 Read')
    mcp.add_tool(fn=kv2.list, name='KV2 List')
    # policy
    mcp.add_tool(fn=policy.write, name='Policy Write')
    mcp.add_tool(fn=policy.delete, name='Policy Delete')
    mcp.add_tool(fn=policy.read, name='Policy Read')
    mcp.add_tool(fn=policy.list, name='Policy List')
    # secret
    mcp.add_tool(fn=secret.enable, name='Secret Engine Enable')
    mcp.add_tool(fn=secret.disable, name='Secret Engine Disable')
    mcp.add_tool(fn=secret.list, name='Secret Engine List')
    # transit
    mcp.add_tool(fn=transit.create, name='Transit Engine Encryption Key Create')
    mcp.add_tool(fn=transit.read, name='Transit Engine Encryption Key Read')
    mcp.add_tool(fn=transit.list, name='Transit Engine Encryption Keys List')
    mcp.add_tool(fn=transit.delete, name='Transit Engine Encryption Key Delete')
    mcp.add_tool(fn=transit.rotate, name='Transit Engine Encryption Key Rotate')
    mcp.add_tool(fn=transit.encrypt, name='Transit Engine Encrypt Plaintext')
    mcp.add_tool(fn=transit.decrypt, name='Transit Engine Decrypt Ciphertext')
    mcp.add_tool(fn=transit.generate, name='Transit Engine Generate Random Bytes')


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
