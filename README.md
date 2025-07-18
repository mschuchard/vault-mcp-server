# Vault MCP Server

This is no longer a toy, and thus will soon begin a formal versioned release schedule. An initial version, updated documentation, and `CHANGELOG` are forthcoming.

Python was selected as the language since this is my first MCP server and the Python SDK is super easy to use, and HVAC is a very functional Vault SDK.

The MCP Server container image is hosted at [Dockerhub](https://hub.docker.com/r/matthewschuchard/vault-mcp-server).

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

Until this tool is formally released at version `1.0.0` the hosted Docker Hub registry container image will match the code hosted here at `HEAD`.

## Features
- ACL Policies
- Audit Devices
- Authentication Engine: Enable/Disable/List
- Secrets Engines
  - Enable/Disable/List
  - KV Version 2
  - Transit
