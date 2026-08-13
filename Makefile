VAULT_RAFT_DIR  := /tmp/vault-raft-data
VAULT_CONFIG    := /tmp/vault-dev.hcl
VAULT_INIT_JSON := /tmp/vault-init.json
VAULT_ADDR      := http://127.0.0.1:8200

# fixtures consumed by tests/vault/test_client.py
VAULT_TEST_ROLE_ID   := test-role-id
VAULT_TEST_SECRET_ID := test-secret-id
VAULT_TEST_USERNAME  := test-user
VAULT_TEST_PASSWORD  := test-password123

bootstrap:
	@rm -f nohup.out $(VAULT_INIT_JSON)
	@rm -rf $(VAULT_RAFT_DIR) && mkdir -p $(VAULT_RAFT_DIR)
	@printf 'storage "raft" {\n  path    = "$(VAULT_RAFT_DIR)"\n  node_id = "dev-node"\n}\nlistener "tcp" {\n  address     = "127.0.0.1:8200"\n  tls_disable = 1\n}\napi_addr     = "$(VAULT_ADDR)"\ncluster_addr = "https://127.0.0.1:8201"\ndisable_mlock = true\n' > $(VAULT_CONFIG)
	@nohup vault server -config=$(VAULT_CONFIG) &
	@sleep 2
	@VAULT_ADDR=$(VAULT_ADDR) vault operator init -key-shares=1 -key-threshold=1 -format=json > $(VAULT_INIT_JSON)
	@VAULT_ADDR=$(VAULT_ADDR) vault operator unseal $$(jq -r '.unseal_keys_b64[0]' $(VAULT_INIT_JSON))
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault secrets enable -path=secret -version=2 kv
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault auth enable approle
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault write auth/approle/role/test-role token_policies=default
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault write auth/approle/role/test-role/role-id role_id=$(VAULT_TEST_ROLE_ID)
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault write auth/approle/role/test-role/custom-secret-id secret_id=$(VAULT_TEST_SECRET_ID)
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault auth enable userpass
	@VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) vault write auth/userpass/users/$(VAULT_TEST_USERNAME) password=$(VAULT_TEST_PASSWORD) policies=default
	@echo "VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON))"

shutdown:
	@killall vault || true

# make ARGS='-k EXPRESSION' unit
unit:
	VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) uv run pytest $(ARGS)

accept:
	VAULT_ADDR=$(VAULT_ADDR) VAULT_TOKEN=$$(jq -r '.root_token' $(VAULT_INIT_JSON)) uv run fastmcp dev src/vault_mcp_server/dev.py

full:
	@echo 'make bootstrap'
	@echo 'docker buildx build . -t matthewschuchard/vault-mcp-server'
	@echo 'servers.vault.env.VAULT_TOKEN in mcp.json'
	@echo 'extensions mcp servers vault start server'
	@echo 'extensions mcp servers vault enable server'
	@echo 'begin chat with agent llm'