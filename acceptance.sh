# vault and mcp servers bootstrap for acceptance testing
rm -f nohup.out && nohup vault server -dev -dev-root-token-id="abcdefghijklmnopqrstuvwxyz09" &
VAULT_TOKEN="abcdefghijklmnopqrstuvwxyz09" uv run fastmcp dev dev.py
killall vault
