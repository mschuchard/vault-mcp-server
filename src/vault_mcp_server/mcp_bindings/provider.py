"""mcp vault integration provider"""

from fastmcp import FastMCP
from fastmcp.resources import Resource
from fastmcp.prompts import Prompt
from mcp.types import Annotations

from vault_mcp_server.vault.secret import database, identity, kv2, pki, transit
from vault_mcp_server.vault.sys import audit, auth, policy, raft, secret
from vault_mcp_server.vault import multi


def resource_provider(mcp: FastMCP) -> None:
    """define implemented resource integrations"""
    # lists of enabled and configured within vault
    mcp.add_resource(
        Resource.from_function(
            fn=audit.list_,
            uri='audit://devices',
            name='enabled-audit-devices',
            description='List the available enabled Vault audit devices',
            mime_type='application/json',
            tags={'audit'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=auth.list_,
            uri='auth://engines',
            name='enabled-authentication-engines',
            description='List the available enabled Vault authentication engines',
            mime_type='application/json',
            tags={'authentication'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=policy.list_,
            uri='sys://policies',
            name='configured-acl-policies',
            description='List the available configured Vault ACL policies',
            mime_type='application/json',
            tags={'acl-policy'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=raft.read_config,
            uri='raft://config',
            name='raft-cluster-configuration',
            description='Read the Raft integrated storage configuration and peer list',
            mime_type='application/json',
            tags={'raft'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=secret.list_,
            uri='secret://engines',
            name='enabled-secret-engines',
            description='List the available enabled Vault secret engines',
            mime_type='application/json',
            tags={'secret-engine'},
            annotations=Annotations(audience=['assistant']),
        )
    )


def tool_provider(mcp: FastMCP) -> None:
    """define implemented tool integrations"""
    # base annotations
    global_annotations: dict[str, bool] = {'openWorldHint': True}
    cu_annotations: dict[str, bool] = {} | global_annotations
    rl_annotations: dict[str, bool] = {'readOnlyHint': True, 'destructiveHint': False} | global_annotations
    del_annotations: dict[str, bool] = {'destructiveHint': True} | global_annotations
    # audit
    mcp.tool(name_or_fn=audit.enable, name='audit-device-enable', annotations=cu_annotations, tags={'audit'})
    mcp.tool(name_or_fn=audit.disable, name='audit-device-disable', annotations=del_annotations, tags={'audit'})
    mcp.tool(name_or_fn=audit.list_, name='audit-devices-list', annotations=rl_annotations, tags={'audit'})
    # auth
    mcp.tool(name_or_fn=auth.enable, name='authentication-engine-enable', annotations=cu_annotations, tags={'authentication'})
    mcp.tool(name_or_fn=auth.disable, name='authentication-engine-disable', annotations=del_annotations, tags={'authentication'})
    mcp.tool(name_or_fn=auth.list_, name='authentication-engines-list', annotations=rl_annotations, tags={'authentication'})
    mcp.tool(name_or_fn=auth.read, name='authentication-engine-read', annotations=rl_annotations, tags={'authentication'})
    mcp.tool(name_or_fn=auth.tune, name='authentication-engine-tune', annotations=cu_annotations, tags={'authentication'})
    # database
    mcp.tool(name_or_fn=database.read_connection, name='database-connection-read', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.list_connections, name='database-connections-list', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.delete_connection, name='database-connection-delete', annotations=del_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.reset_connection, name='database-connection-reset', annotations=cu_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.rotate_root_credentials, name='database-connection-rotate-root', annotations=cu_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.create_role, name='database-role-create', annotations=cu_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.read_role, name='database-role-read', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.list_roles, name='database-roles-list', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.delete_role, name='database-role-delete', annotations=del_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.generate_credentials, name='database-credentials-generate', annotations=cu_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.create_static_role, name='database-static-role-create', annotations=cu_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.read_static_role, name='database-static-role-read', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.list_static_roles, name='database-static-roles-list', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.delete_static_role, name='database-static-role-delete', annotations=del_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.get_static_credentials, name='database-static-credentials-get', annotations=rl_annotations, tags={'database'})
    mcp.tool(name_or_fn=database.rotate_static_role_credentials, name='database-static-credentials-rotate', annotations=cu_annotations, tags={'database'})
    # identity - entity
    mcp.tool(name_or_fn=identity.create_or_update_entity, name='identity-entity-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_entity, name='identity-entity-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_entity_by_name, name='identity-entity-read-by-name', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.update_entity, name='identity-entity-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_entity, name='identity-entity-delete', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_entity_by_name, name='identity-entity-delete-by-name', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_entities, name='identity-entities-list', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.merge_entities, name='identity-entities-merge', annotations=cu_annotations, tags={'identity'})
    # identity - entity alias
    mcp.tool(name_or_fn=identity.create_or_update_entity_alias, name='identity-entity-alias-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_entity_alias, name='identity-entity-alias-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.update_entity_alias, name='identity-entity-alias-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_entity_aliases, name='identity-entity-aliases-list', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_entity_alias, name='identity-entity-alias-delete', annotations=del_annotations, tags={'identity'})
    # identity - group
    mcp.tool(name_or_fn=identity.create_or_update_group, name='identity-group-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_group, name='identity-group-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_group_by_name, name='identity-group-read-by-name', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.update_group, name='identity-group-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_group, name='identity-group-delete', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_group_by_name, name='identity-group-delete-by-name', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_groups, name='identity-groups-list', annotations=rl_annotations, tags={'identity'})
    # identity - group alias
    mcp.tool(name_or_fn=identity.create_or_update_group_alias, name='identity-group-alias-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_group_alias, name='identity-group-alias-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.update_group_alias, name='identity-group-alias-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_group_aliases, name='identity-group-aliases-list', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_group_alias, name='identity-group-alias-delete', annotations=del_annotations, tags={'identity'})
    # identity - lookup
    mcp.tool(name_or_fn=identity.lookup_entity, name='identity-entity-lookup', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.lookup_group, name='identity-group-lookup', annotations=rl_annotations, tags={'identity'})
    # identity - oidc
    mcp.tool(name_or_fn=identity.configure_tokens_backend, name='identity-oidc-configure', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_token_backend_configuration, name='identity-oidc-configuration-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.create_named_key, name='identity-oidc-key-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_named_key, name='identity-oidc-key-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_named_key, name='identity-oidc-key-delete', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_named_keys, name='identity-oidc-keys-list', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.rotate_named_key, name='identity-oidc-key-rotate', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.create_or_update_role, name='identity-oidc-role-create-or-update', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_role, name='identity-oidc-role-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.delete_role, name='identity-oidc-role-delete', annotations=del_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.list_roles, name='identity-oidc-roles-list', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.generate_signed_id_token, name='identity-oidc-token-generate', annotations=cu_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.introspect_signed_id_token, name='identity-oidc-token-introspect', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_well_known_configurations, name='identity-oidc-well-known-read', annotations=rl_annotations, tags={'identity'})
    mcp.tool(name_or_fn=identity.read_active_public_keys, name='identity-oidc-public-keys-read', annotations=rl_annotations, tags={'identity'})
    # kv2
    mcp.tool(name_or_fn=kv2.create_update, name='kv2-create-or-update', annotations=cu_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.delete, name='kv2-delete', annotations=del_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.undelete, name='kv2-undelete', annotations=cu_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.read, name='kv2-read', annotations=rl_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.list_, name='kv2-list', annotations=rl_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.read_secret_metadata, name='kv2-metadata-and-versions', annotations=rl_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.patch, name='kv2-patch', annotations=cu_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.configure, name='kv2-configure-backend', annotations=cu_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.read_configuration, name='kv2-read-backend-configuration', annotations=rl_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.delete_latest_version_of_secret, name='kv2-delete-latest-version', annotations=del_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.delete_secret_versions, name='kv2-delete-specific-versions', annotations=del_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.destroy, name='kv2-destroy-versions', annotations=del_annotations, tags={'key-value-v2'})
    mcp.tool(name_or_fn=kv2.update_metadata, name='kv2-update-metadata', annotations=cu_annotations, tags={'key-value-v2'})
    # pki
    mcp.tool(name_or_fn=pki.generate_root, name='pki-generate-root-ca', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.delete_root, name='pki-delete-root-ca', annotations=del_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_root_certificate, name='pki-read-root-ca', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_root_certificate_chain, name='pki-read-root-ca-chain', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_crl, name='pki-read-crl', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.rotate_crl, name='pki-rotate-crl', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.generate_intermediate, name='pki-generate-intermediate', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.set_signed_intermediate, name='pki-set-signed-intermediate', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.sign_intermediate_certificate, name='pki-sign-intermediate-certificate', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.sign_self_issued, name='pki-sign-self-issued', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.generate_certificate, name='pki-generate-certificate', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.sign_certificate, name='pki-sign-certificate', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_certificate, name='pki-read-certificate', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.list_certificates, name='pki-list-certificates', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.revoke_certificate, name='pki-revoke-certificate', annotations=del_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.tidy_certificates, name='pki-tidy-certificates', annotations=del_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_crl_configuration, name='pki-read-crl-configuration', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.set_crl_configuration, name='pki-set-crl-configuration', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_urls, name='pki-read-urls', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.set_urls, name='pki-set-urls', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.submit_ca_information, name='pki-submit-ca-information', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.create_update_role, name='pki-create-update-role', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.list_roles, name='pki-list-roles', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_role, name='pki-read-role', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.delete_role, name='pki-delete-role', annotations=del_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.read_issuer, name='pki-read-issuer', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.list_issuers, name='pki-list-issuers', annotations=rl_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.update_issuer, name='pki-update-issuer', annotations=cu_annotations, tags={'pki'})
    mcp.tool(name_or_fn=pki.revoke_issuer, name='pki-revoke-issuer', annotations=del_annotations, tags={'pki'})
    # policy
    mcp.tool(name_or_fn=policy.create_update, name='policy-create-or-update', annotations=cu_annotations, tags={'policy'})
    mcp.tool(name_or_fn=policy.delete, name='policy-delete', annotations=del_annotations, tags={'acl-policy'})
    mcp.tool(name_or_fn=policy.read, name='policy-read', annotations=rl_annotations, tags={'acl-policy'})
    mcp.tool(name_or_fn=policy.list_, name='policies-list', annotations=rl_annotations, tags={'acl-policy'})
    # raft
    mcp.tool(name_or_fn=raft.read_config, name='raft-config-read', annotations=rl_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.join, name='raft-cluster-join', annotations=cu_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.remove_node, name='raft-node-remove', annotations=del_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.take_snapshot, name='raft-snapshot-take', annotations=rl_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.restore_snapshot, name='raft-snapshot-restore', annotations=cu_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.read_auto_snapshot_status, name='raft-auto-snapshot-status-read', annotations=rl_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.read_auto_snapshot_config, name='raft-auto-snapshot-config-read', annotations=rl_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.list_auto_snapshot_configs, name='raft-auto-snapshot-configs-list', annotations=rl_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.create_update_auto_snapshot_config, name='raft-auto-snapshot-config-create-or-update', annotations=cu_annotations, tags={'raft'})
    mcp.tool(name_or_fn=raft.delete_auto_snapshot_config, name='raft-auto-snapshot-config-delete', annotations=del_annotations, tags={'raft'})
    # secret
    mcp.tool(name_or_fn=secret.enable, name='secret-engine-enable', annotations=cu_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.disable, name='secret-engine-disable', annotations=del_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.list_, name='secret-engines-list', annotations=rl_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.move, name='secret-engine-move', annotations=cu_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.read_configuration, name='secret-engine-read-configuration', annotations=rl_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.tune_configuration, name='secret-engine-tune-configuration', annotations=cu_annotations, tags={'secret-engine'})
    mcp.tool(name_or_fn=secret.retrieve_option, name='secret-engine-retrieve-option', annotations=rl_annotations, tags={'secret-engine'})
    # transit
    mcp.tool(name_or_fn=transit.create, name='transit-engine-encryption-key-create', annotations=cu_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.update_config, name='transit-engine-encryption-key-update-config', annotations=cu_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.read, name='transit-engine-encryption-key-read', annotations=rl_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.list_, name='transit-engine-encryption-keys-list', annotations=rl_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.delete, name='transit-engine-encryption-key-delete', annotations=del_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.rotate, name='transit-engine-encryption-key-rotate', annotations=cu_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.encrypt, name='transit-engine-encrypt-plaintext', annotations=cu_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.decrypt, name='transit-engine-decrypt-ciphertext', annotations=cu_annotations, tags={'transit'})
    mcp.tool(name_or_fn=transit.generate, name='transit-engine-generate-random-bytes', annotations=cu_annotations, tags={'transit'})


def prompt_provider(mcp: FastMCP) -> None:
    """define implemented prompt integrations"""
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.example_policy,
            name='example-acl-policy',
            tags={'acl-policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.generate_policy,
            name='generate-acl-policy',
            tags={'acl-policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.generate_smart_policy,
            name='generate-smart-acl-policy',
            tags={'acl-policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=multi.diagnose_vault_state,
            name='diagnose-vault-state',
            tags={'multiple'},
        )
    )


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
    prompt_provider(mcp)
