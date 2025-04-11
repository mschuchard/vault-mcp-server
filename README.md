# Vault MCP Server

This is a toy. Python was selected as the language since the MCP Go SDK does not exist at the time of this writing, and HVAC is a very functional Vault SDK. Practically anything featured in this tool is also available and almost as easy to use in the Vault UI.

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

Please note that the container image does not yet exist at the time of this writing, but you can also build it yourself using the `Dockerfile` in this repository.