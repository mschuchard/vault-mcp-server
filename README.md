# Vault MCP Server

There is now an official Vault MCP Server from Hashicorp. Therefore, the alternative third-party Vault MCP Server will continue to exist and be updated with features and fixes, but no attempt will be made to compete with the official product. The third-party Vault MCP Server can be executed locally instead of only remotely (although in many situations remote is preferable), and will continue to be available as a container image.

Due to this policy enacted because of the official product release, there will be no formal release process, versioning, or changelog. This product is also not recommended for enterprise production usage.

The MCP Server container image is hosted at [Dockerhub](https://hub.docker.com/r/matthewschuchard/vault-mcp-server), and it represents the code hosted here at `HEAD`.

## Desktop Configs

These can hopefully be extrapolated and modified to fit other clients if you want to play with this server for whatever reason.

**Claude**
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
        "VAULT_URL",
        "-e",
        "VAULT_TOKEN",
        "matthewschuchard/vault-mcp-server"
      ],
      "env": {
        "VAULT_URL": "<VAULT SERVER CLUSTER URL>",
        "VAULT_TOKEN": "<VAULT AUTHENTICATION TOKEN>"
      }
    }
  }
}
```

**VSCode**

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
        "VAULT_URL",
        "-e",
        "VAULT_TOKEN",
        "matthewschuchard/vault-mcp-server"
      ],
      "env": {
        "VAULT_URL": "<VAULT SERVER CLUSTER URL>",
        "VAULT_TOKEN": "<VAULT AUTHENTICATION TOKEN>"
      }
    }
  }
}
```

## Features
- ACL Policies
- Audit Devices
- Authentication Engine: Enable/Disable/List
- Secrets Engines
  - Enable/Disable/List
  - KV Version 2
  - PKI
  - Transit
