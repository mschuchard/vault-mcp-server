bootstrap:
	@rm -f nohup.out
	@nohup vault server -dev -dev-root-token-id="abcdefghijklmnopqrstuvwxyz09" &

shutdown:
	@killall vault

unit: shutdown bootstrap
	VAULT_TOKEN="abcdefghijklmnopqrstuvwxyz09" uv run pytest

accept:
	VAULT_TOKEN="abcdefghijklmnopqrstuvwxyz09" uv run fastmcp dev dev.py