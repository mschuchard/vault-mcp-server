# vault and server bootstrap for unit testing
rm -f nohup.out && nohup vault server -dev -dev-root-token-id="abcdefghijklmnopqrstuvwxyz09" &
VAULT_TOKEN="abcdefghijklmnopqrstuvwxyz09" uv run pytest
killall vault
