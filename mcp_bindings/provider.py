"""mcp vault integration provider"""

from mcp.server.fastmcp import FastMCP

from vault import audit, auth, kv2, policy, secret


def resource_provider(mcp: FastMCP) -> None:
    """define implemented resource integrations"""
    pass


def tool_provider(mcp: FastMCP) -> None:
    """define implemented tool integrations"""
    # audit
    mcp.add_tool(fn=audit.enable, name='Enable Audit Device')
    mcp.add_tool(fn=audit.disable, name='Disable Audit Device')
    mcp.add_tool(fn=audit.list, name='List Audit Devices')
    # auth
    mcp.add_tool(fn=auth.enable, name='Enable Authentication Engine')
    mcp.add_tool(fn=auth.disable, name='Disable Authentication Engine')
    mcp.add_tool(fn=auth.list, name='List Authentication Engines')
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
    mcp.add_tool(fn=secret.enable, name='Enable Secret Engine')
    mcp.add_tool(fn=secret.disable, name='Disable Secret Engine')
    mcp.add_tool(fn=secret.list, name='List Secret Engines')


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
