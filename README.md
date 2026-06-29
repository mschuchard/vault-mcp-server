# Vault MCP Server

There is now an official Vault MCP Server from Hashicorp. Therefore, the alternative third-party Vault MCP Server will continue to exist and be updated with features and fixes, but no attempt will be made to compete with the official product. The third-party Vault MCP Server can be executed locally instead of only remotely (although in many situations remote is preferable), and will continue to be available as a container image.

Due to this policy enacted because of the official product release, there will be no formal release process, versioning, or changelog. This product is also not recommended for enterprise production usage.

The MCP Server container image is hosted at [Dockerhub](https://hub.docker.com/r/matthewschuchard/vault-mcp-server), and it represents the code hosted here at `HEAD`.

## Desktop Configs

These can hopefully be extrapolated and modified to fit other clients if you want to play with this server for whatever reason.

### Claude
```json
{
  "mcpServers": {
    "vault": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "ENV_VAR",
        "-e",
        "ENV_VAR_TWO",
        "matthewschuchard/vault-mcp-server"
      ],
      "env": {
        "ENV_VAR": "<ENV VAR VALUE>",
        "ENV_VAR_TWO": "<ENV VAR TWO VALUE>",
      }
    }
  }
}
```

### VSCode

The `MCP: Add Server --> Docker Image` command can also streamline this configuration. The values below can be entered into the input prompts, and then the `mcp.json` file is automically opened within a pane afterward for further updates if necessary.

```json
{
  "servers": {
    "vault": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "ENV_VAR",
        "-e",
        "ENV_VAR_TWO",
        "matthewschuchard/vault-mcp-server"
      ],
      "env": {
        "ENV_VAR": "<ENV VAR VALUE>",
        "ENV_VAR_TWO": "<ENV VAR TWO VALUE>",
      }
    }
  }
}
```

### Environment Variables

These environment variables can all be defined and passed to the Vault MCP Server utilizing the pattern shown above for `ENV_VAR`.

- **CACHE_TTL**: 60

Establishes the cache time for all read and list operations before new value(s) are retrieved instead of using the cached value.

- **VAULT_AUTH_METHOD**: 'token'

Selects the Vault authentication method from among `approle` (beta), `token`, and `userpass` (beta).

- **VAULT_NAMESPACE**: ''

Establishes the Vault namespace (enterprise only).

- **VAULT_PASSWORD**: None

Password for user with the `userpass` authentication method.

- **VAULT_ROLE_ID**: None

Role ID for entity with the `approle` authentication method.

- **VAULT_SECRET_ID**: None

Secret ID for entity with the `approle` authentication method.

- **VAULT_TOKEN**: None

Token for entity with the `token` authentication method.

- **VAULT_URL**: http://127.0.0.1:8200

Vault server URL.

- **VAULT_USERNAME**: None

Username for user with the `userpass` authentication method.

## Features

### Resources (5)
- Current Enabled ACL Policies
- Current Enabled Audit Devices
- Current Enabled Authentication Engines
- Current Enabled Secret Engines
- Current Raft Cluster Configuration

### Tools (138)
- System Backend
  - ACL Policies
  - Audit Devices
  - Authentication Engines
  - Raft (Clustering and Storage Snapshots)
  - Secrets Engines
- Secrets Backend
  - Database (Beta)
  - Identity/Alias
  - KV Version 2
  - PKI
  - Transit

### Prompts (4)
- mcp.vault.example-acl-policy: This displays an example Vault ACL Policy in JSON string format. The displayed policy can be modified and entered as-is to the LLM (verified with agentic Claude), and it will understand that you want to create an ACL Policy through the Vault MCP Server with your modified content (with an auto-generated name). However, it is probably more prudent to use it as an input to the tool instead.
- mcp.vault.generate-acl-policy: This displays a pseudo-example Vault ACL Policy in JSON string format similar to the above prompt. The primary difference is that this prompt accepts a `paths` argument in `list[str]` type format, and the returned policy will contain the input paths. However, the `capabilities` will still be boilerplate, and need to be modified for your usage.
- mcp.vault.generate-smart-acl-policy: This is an interactive workflow with an agentic LLM to create and optimize a Vault ACL policy based on user requirements and prompts. It will also return the policy in JSON string format.
- mcp.vault.diagnose-vault-state: This is a diagnostic scanner to target your Vault server cluster with the resources available in this MCP server and report on any perceived deficiencies with respect to the server configuration.