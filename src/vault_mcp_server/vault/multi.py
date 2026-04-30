"""vault multiple interfaces"""

from fastmcp import Context

from vault_mcp_server.vault.sys import audit, auth, policy, secret


async def diagnose_vault_state(ctx: Context) -> str:
    """Diagnose the current Vault cluster state and surface potential misconfigurations"""

    # gather resource information
    policies: list[str] = await policy.list_(ctx)
    secret_engines: dict = await secret.list_(ctx)
    auth_engines: dict = await auth.list_(ctx)
    audit_devices: dict = await audit.list_(ctx)

    # read policy contents for cross-referencing
    policy_contents: dict[str, dict] = {}
    for name in policies:
        if name not in ('root', 'default'):
            policy_contents[name] = await policy.read(ctx, name=name)

    # extract mounted paths for cross-referencing
    mounted_paths: list[str] = list(secret_engines.keys())

    return f"""Diagnose the following Vault cluster state and identify potential misconfigurations, security gaps, or missing components.

Current Vault state:
- Enabled audit devices: {audit_devices}
- Enabled authentication methods: {auth_engines}
- Mounted secret engines: {secret_engines}
- ACL policies: {policies}
- Policy contents: {policy_contents}

Check for the following issues and report findings grouped by severity (critical, warning, info):

1. AUDIT: Flag if no audit devices are enabled — this is a critical security gap
2. AUTH: Flag if only the token auth method is enabled — no external auth methods configured
3. POLICIES: Cross-reference mounted secret engine paths ({mounted_paths}) against policy contents — flag any mounted engine with no policy covering its paths
4. POLICIES: Flag any policy that exists but is not referenced by any auth method role (orphaned policies)
5. AUTH: Flag auth methods with no associated policies configured
6. ENGINES: Flag secret engines mounted but likely unused (no corresponding policy path coverage)

Be specific — reference the actual names and paths from the state above rather than giving generic advice."""
