# Vault MCP Server

This is a toy. Python was selected as the language since this is my first MCP server and the Python SDK is super easy to use, and HVAC is a very functional Vault SDK.

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

Until this tool matures beyond an arbitrary point the above hosted Docker Hub registry container image will match the code hosted here at `HEAD`.

## Features
- ACL Policies
- Audit Devices
- Authentication Engine: Enable/Disable/List
- Secrets Engines
  - Enable/Disable/List
  - KV Version 2
  - Transit (Encrypt/Decrypt currently experiencing HVAC body serialization issues)
