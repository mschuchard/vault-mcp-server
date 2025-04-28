# Vault MCP Server

This is a toy. Python was selected as the language since this is my first MCP server and the Python SDK is super easy to use, and HVAC is a very functional Vault SDK. Practically anything featured in this tool is also available and almost as easy to use in the Vault UI.

## Claude Desktop Config

This can hopefully be extrapolated and modified to fit other clients if you want to play with this server for whatever reason.

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

## Features
- Enable/Disable Authentication Engine
- Enable/Disable Secrets Engine
- KV Version 2 Secrets Engine
- ACL Policies
- Audit Devices