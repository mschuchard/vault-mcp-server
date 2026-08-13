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
            description='List the currently enabled Vault audit devices (also known as: audit backends, audit log backends).',
            mime_type='application/json',
            tags={'audit', 'audit-device', 'audit-backend'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=auth.list_,
            uri='auth://engines',
            name='enabled-authentication-engines',
            description='List the currently enabled Vault authentication engines (also known as: auth methods, auth backends, login methods).',
            mime_type='application/json',
            tags={'authentication', 'auth-engine', 'auth-method'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=policy.list_,
            uri='sys://policies',
            name='configured-acl-policies',
            description='List the existing Vault ACL policies (also known as: access policies, permissions policies).',
            mime_type='application/json',
            tags={'acl-policy', 'policy', 'permissions'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=raft.read_config,
            uri='raft://config',
            name='raft-cluster-configuration',
            description='Read the Raft integrated storage configuration and peer list (also known as: raft storage cluster, cluster nodes, storage backend config).',
            mime_type='application/json',
            tags={'raft', 'storage', 'cluster'},
            annotations=Annotations(audience=['assistant']),
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=secret.list_,
            uri='secret://engines',
            name='enabled-secret-engines',
            description='List the currently enabled Vault secret engines (also known as: mounts, secrets engines, mount points, backends, sys/mounts).',
            mime_type='application/json',
            tags={'secret-engine', 'mounts', 'backend'},
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

    # audit (also known as: audit devices, audit backends, audit log backends)
    mcp.tool(
        name_or_fn=audit.enable,
        name='audit-device-enable',
        description='Enable a Vault audit device (also known as: audit backend, audit log backend) to record requests and responses.',
        annotations=cu_annotations,
        tags={'audit', 'audit-device', 'audit-backend'},
    )
    mcp.tool(
        name_or_fn=audit.disable,
        name='audit-device-disable',
        description='Disable an enabled Vault audit device (also known as: audit backend, audit log backend) at a given path.',
        annotations=del_annotations,
        tags={'audit', 'audit-device', 'audit-backend'},
    )
    mcp.tool(
        name_or_fn=audit.list_,
        name='audit-devices-list',
        description='List the currently enabled Vault audit devices (also known as: audit backends, audit log backends).',
        annotations=rl_annotations,
        tags={'audit', 'audit-device', 'audit-backend'},
    )
    # auth (also known as: authentication engines, auth methods, auth backends, login methods)
    mcp.tool(
        name_or_fn=auth.enable,
        name='authentication-engine-enable',
        description='Enable a Vault authentication engine (also known as: auth method, auth backend, login method) such as userpass, github, approle, or kubernetes.',
        annotations=cu_annotations,
        tags={'authentication', 'auth-engine', 'auth-method'},
    )
    mcp.tool(
        name_or_fn=auth.disable,
        name='authentication-engine-disable',
        description='Disable an enabled Vault authentication engine (also known as: auth method, auth backend, login method) at a given path.',
        annotations=del_annotations,
        tags={'authentication', 'auth-engine', 'auth-method'},
    )
    mcp.tool(
        name_or_fn=auth.list_,
        name='authentication-engines-list',
        description='List the currently enabled Vault authentication engines (also known as: auth methods, auth backends, login methods).',
        annotations=rl_annotations,
        tags={'authentication', 'auth-engine', 'auth-method'},
    )
    mcp.tool(
        name_or_fn=auth.read,
        name='authentication-engine-read',
        description='Read the tuning configuration for a mounted Vault authentication engine (also known as: auth method, auth backend, auth mount tuning).',
        annotations=rl_annotations,
        tags={'authentication', 'auth-engine', 'auth-method'},
    )
    mcp.tool(
        name_or_fn=auth.tune,
        name='authentication-engine-tune',
        description='Tune configuration parameters (TTLs, description, listing visibility, audit HMAC keys) for a Vault authentication engine (also known as: auth method, auth backend, auth mount).',
        annotations=cu_annotations,
        tags={'authentication', 'auth-engine', 'auth-method'},
    )
    # database (also known as: database secrets engine, db secrets engine, dynamic/static database credentials)
    mcp.tool(
        name_or_fn=database.read_connection,
        name='database-connection-read',
        description='Read the configuration for a database connection in the Vault database secrets engine (also known as: db engine, database backend).',
        annotations=rl_annotations,
        tags={'database', 'db-connection'},
    )
    mcp.tool(
        name_or_fn=database.list_connections,
        name='database-connections-list',
        description='List configured database connections in the Vault database secrets engine (also known as: db engine, database backend).',
        annotations=rl_annotations,
        tags={'database', 'db-connection'},
    )
    mcp.tool(
        name_or_fn=database.delete_connection,
        name='database-connection-delete',
        description='Delete a database connection from the Vault database secrets engine (also known as: db engine, database backend).',
        annotations=del_annotations,
        tags={'database', 'db-connection'},
    )
    mcp.tool(
        name_or_fn=database.reset_connection,
        name='database-connection-reset',
        description='Close and restart a database connection plugin in the Vault database secrets engine using its stored configuration.',
        annotations=cu_annotations,
        tags={'database', 'db-connection'},
    )
    mcp.tool(
        name_or_fn=database.rotate_root_credentials,
        name='database-connection-rotate-root',
        description='Rotate the stored root/superuser credentials for a database connection in the Vault database secrets engine.',
        annotations=cu_annotations,
        tags={'database', 'db-connection', 'credentials'},
    )
    mcp.tool(
        name_or_fn=database.create_role,
        name='database-role-create',
        description='Create or update a dynamic database role (also known as: dynamic credentials role) in the Vault database secrets engine.',
        annotations=cu_annotations,
        tags={'database', 'db-role', 'dynamic-credentials'},
    )
    mcp.tool(
        name_or_fn=database.read_role,
        name='database-role-read',
        description='Read a dynamic database role definition in the Vault database secrets engine.',
        annotations=rl_annotations,
        tags={'database', 'db-role', 'dynamic-credentials'},
    )
    mcp.tool(
        name_or_fn=database.list_roles,
        name='database-roles-list',
        description='List dynamic database roles configured in the Vault database secrets engine.',
        annotations=rl_annotations,
        tags={'database', 'db-role', 'dynamic-credentials'},
    )
    mcp.tool(
        name_or_fn=database.delete_role,
        name='database-role-delete',
        description='Delete a dynamic database role definition from the Vault database secrets engine.',
        annotations=del_annotations,
        tags={'database', 'db-role', 'dynamic-credentials'},
    )
    mcp.tool(
        name_or_fn=database.generate_credentials,
        name='database-credentials-generate',
        description='Generate dynamic (short-lived) database credentials for a role in the Vault database secrets engine.',
        annotations=cu_annotations,
        tags={'database', 'db-role', 'dynamic-credentials', 'credentials'},
    )
    mcp.tool(
        name_or_fn=database.create_static_role,
        name='database-static-role-create',
        description='Create or update a static database role, which manages the rotating password for an existing database user, in the Vault database secrets engine.',
        annotations=cu_annotations,
        tags={'database', 'db-role', 'static-credentials'},
    )
    mcp.tool(
        name_or_fn=database.read_static_role,
        name='database-static-role-read',
        description='Read a static database role definition in the Vault database secrets engine.',
        annotations=rl_annotations,
        tags={'database', 'db-role', 'static-credentials'},
    )
    mcp.tool(
        name_or_fn=database.list_static_roles,
        name='database-static-roles-list',
        description='List static database roles configured in the Vault database secrets engine.',
        annotations=rl_annotations,
        tags={'database', 'db-role', 'static-credentials'},
    )
    mcp.tool(
        name_or_fn=database.delete_static_role,
        name='database-static-role-delete',
        description='Delete a static database role definition from the Vault database secrets engine.',
        annotations=del_annotations,
        tags={'database', 'db-role', 'static-credentials'},
    )
    mcp.tool(
        name_or_fn=database.get_static_credentials,
        name='database-static-credentials-get',
        description='Retrieve the current (rotating) credentials for a static database role in the Vault database secrets engine.',
        annotations=rl_annotations,
        tags={'database', 'db-role', 'static-credentials', 'credentials'},
    )
    mcp.tool(
        name_or_fn=database.rotate_static_role_credentials,
        name='database-static-credentials-rotate',
        description='Manually trigger rotation of the password for a static database role in the Vault database secrets engine.',
        annotations=cu_annotations,
        tags={'database', 'db-role', 'static-credentials', 'credentials'},
    )
    # identity - entity (also known as: identity engine, identity entities)
    mcp.tool(
        name_or_fn=identity.create_or_update_entity,
        name='identity-entity-create-or-update',
        description='Create or update an entity in the Vault identity engine (also known as: identity entity, identity secrets engine).',
        annotations=cu_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.read_entity,
        name='identity-entity-read',
        description='Read an entity by ID from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.read_entity_by_name,
        name='identity-entity-read-by-name',
        description='Read an entity by name from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.update_entity,
        name='identity-entity-update',
        description='Update an existing entity by ID in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.delete_entity,
        name='identity-entity-delete',
        description='Delete an entity by ID from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.delete_entity_by_name,
        name='identity-entity-delete-by-name',
        description='Delete an entity by name from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.list_entities,
        name='identity-entities-list',
        description='List all entity IDs in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.merge_entities,
        name='identity-entities-merge',
        description='Merge multiple entities into a single target entity in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-entity'},
    )
    # identity - entity alias
    mcp.tool(
        name_or_fn=identity.create_or_update_entity_alias,
        name='identity-entity-alias-create-or-update',
        description='Create or update an entity alias (the identifier of a client in an auth source, e.g. a userpass username) in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-entity', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.read_entity_alias,
        name='identity-entity-alias-read',
        description='Read an entity alias by ID from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.update_entity_alias,
        name='identity-entity-alias-update',
        description='Update an existing entity alias by ID in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-entity', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.list_entity_aliases,
        name='identity-entity-aliases-list',
        description='List all entity alias IDs in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.delete_entity_alias,
        name='identity-entity-alias-delete',
        description='Delete an entity alias by ID from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-entity', 'identity-alias'},
    )
    # identity - group
    mcp.tool(
        name_or_fn=identity.create_or_update_group,
        name='identity-group-create-or-update',
        description='Create or update a group (internal or external) in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.read_group,
        name='identity-group-read',
        description='Read a group by ID from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.read_group_by_name,
        name='identity-group-read-by-name',
        description='Read a group by name from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.update_group,
        name='identity-group-update',
        description='Update an existing group by ID in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.delete_group,
        name='identity-group-delete',
        description='Delete a group by ID from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.delete_group_by_name,
        name='identity-group-delete-by-name',
        description='Delete a group by name from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-group'},
    )
    mcp.tool(
        name_or_fn=identity.list_groups,
        name='identity-groups-list',
        description='List all group IDs in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group'},
    )
    # identity - group alias
    mcp.tool(
        name_or_fn=identity.create_or_update_group_alias,
        name='identity-group-alias-create-or-update',
        description='Create or update a group alias (the identifier of a group in an external auth provider) in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-group', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.read_group_alias,
        name='identity-group-alias-read',
        description='Read a group alias by ID from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.update_group_alias,
        name='identity-group-alias-update',
        description='Update an existing group alias by ID in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'identity-group', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.list_group_aliases,
        name='identity-group-aliases-list',
        description='List all group alias IDs in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group', 'identity-alias'},
    )
    mcp.tool(
        name_or_fn=identity.delete_group_alias,
        name='identity-group-alias-delete',
        description='Delete a group alias by ID from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'identity-group', 'identity-alias'},
    )
    # identity - lookup
    mcp.tool(
        name_or_fn=identity.lookup_entity,
        name='identity-entity-lookup',
        description='Look up an entity by name, ID, or alias attributes in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-entity'},
    )
    mcp.tool(
        name_or_fn=identity.lookup_group,
        name='identity-group-lookup',
        description='Look up a group by name, ID, or alias attributes in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'identity-group'},
    )
    # identity - oidc (also known as: OIDC identity tokens, OIDC provider)
    mcp.tool(
        name_or_fn=identity.configure_tokens_backend,
        name='identity-oidc-configure',
        description='Configure the OIDC identity token issuer for the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.read_token_backend_configuration,
        name='identity-oidc-configuration-read',
        description='Read the OIDC identity token backend configuration for the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.create_named_key,
        name='identity-oidc-key-create-or-update',
        description='Create or update a named OIDC signing key used for identity token generation in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    mcp.tool(
        name_or_fn=identity.read_named_key,
        name='identity-oidc-key-read',
        description='Read a named OIDC signing key from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    mcp.tool(
        name_or_fn=identity.delete_named_key,
        name='identity-oidc-key-delete',
        description='Delete a named OIDC signing key from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    mcp.tool(
        name_or_fn=identity.list_named_keys,
        name='identity-oidc-keys-list',
        description='List all named OIDC signing keys in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    mcp.tool(
        name_or_fn=identity.rotate_named_key,
        name='identity-oidc-key-rotate',
        description='Manually rotate a named OIDC signing key in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    mcp.tool(
        name_or_fn=identity.create_or_update_role,
        name='identity-oidc-role-create-or-update',
        description='Create or update an OIDC identity token role in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.read_role,
        name='identity-oidc-role-read',
        description='Read an OIDC identity token role from the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.delete_role,
        name='identity-oidc-role-delete',
        description='Delete an OIDC identity token role from the Vault identity engine.',
        annotations=del_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.list_roles,
        name='identity-oidc-roles-list',
        description='List all OIDC identity token roles in the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.generate_signed_id_token,
        name='identity-oidc-token-generate',
        description='Generate a signed OIDC identity token (JWT) for a role in the Vault identity engine.',
        annotations=cu_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.introspect_signed_id_token,
        name='identity-oidc-token-introspect',
        description='Introspect and validate a signed OIDC identity token (JWT) issued by the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.read_well_known_configurations,
        name='identity-oidc-well-known-read',
        description='Read the OIDC well-known discovery configuration published by the Vault identity engine.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token'},
    )
    mcp.tool(
        name_or_fn=identity.read_active_public_keys,
        name='identity-oidc-public-keys-read',
        description='Read the active OIDC public keys (JWKS) published by the Vault identity engine, used to verify identity tokens.',
        annotations=rl_annotations,
        tags={'identity', 'oidc', 'identity-token', 'signing-key'},
    )
    # kv2 (also known as: key-value version 2, KV v2, key-value secrets engine, secret store)
    mcp.tool(
        name_or_fn=kv2.create_update,
        name='kv2-create-or-update',
        description='Create or update a secret in the Vault key-value version 2 secrets engine (also known as: KV v2, key-value store).',
        annotations=cu_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.delete,
        name='kv2-delete',
        description='Delete a secret (metadata and all versions) from the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=del_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.undelete,
        name='kv2-undelete',
        description='Undelete specific versions of a soft-deleted secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=cu_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.read,
        name='kv2-read',
        description='Read a secret value from the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=rl_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.list_,
        name='kv2-list',
        description='List the secrets (keys) at a path in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=rl_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.read_secret_metadata,
        name='kv2-metadata-and-versions',
        description='Read the metadata and version history for a secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=rl_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value', 'metadata'},
    )
    mcp.tool(
        name_or_fn=kv2.patch,
        name='kv2-patch',
        description='Partially update a secret without overwriting existing data in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=cu_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.configure,
        name='kv2-configure-backend',
        description='Configure backend-level settings (max versions, CAS, delete-version-after) for the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=cu_annotations,
        tags={'key-value-v2', 'kv2', 'configuration'},
    )
    mcp.tool(
        name_or_fn=kv2.read_configuration,
        name='kv2-read-backend-configuration',
        description='Read the backend-level configuration of the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=rl_annotations,
        tags={'key-value-v2', 'kv2', 'configuration'},
    )
    mcp.tool(
        name_or_fn=kv2.delete_latest_version_of_secret,
        name='kv2-delete-latest-version',
        description='Soft-delete the latest version of a secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=del_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.delete_secret_versions,
        name='kv2-delete-specific-versions',
        description='Soft-delete specific versions of a secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=del_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.destroy,
        name='kv2-destroy-versions',
        description='Permanently destroy specific versions of a secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=del_annotations,
        tags={'key-value-v2', 'kv2', 'secret-value'},
    )
    mcp.tool(
        name_or_fn=kv2.update_metadata,
        name='kv2-update-metadata',
        description='Update metadata (max versions, CAS, custom metadata) for a secret in the Vault key-value version 2 secrets engine (also known as: KV v2).',
        annotations=cu_annotations,
        tags={'key-value-v2', 'kv2', 'metadata'},
    )
    # pki (also known as: PKI secrets engine, certificate authority, CA, certificates)
    mcp.tool(
        name_or_fn=pki.generate_root,
        name='pki-generate-root-ca',
        description='Generate a root CA certificate with the Vault PKI secrets engine (also known as: certificate authority, PKI backend).',
        annotations=cu_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.delete_root,
        name='pki-delete-root-ca',
        description='Delete the current root CA certificate from the Vault PKI secrets engine (also known as: certificate authority).',
        annotations=del_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.read_root_certificate,
        name='pki-read-root-ca',
        description='Read the current root CA certificate (raw DER-encoded) from the Vault PKI secrets engine (also known as: certificate authority).',
        annotations=rl_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.read_root_certificate_chain,
        name='pki-read-root-ca-chain',
        description='Read the current root CA certificate chain (PEM format) from the Vault PKI secrets engine (also known as: certificate authority).',
        annotations=rl_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.read_crl,
        name='pki-read-crl',
        description='Read the current certificate revocation list (CRL) from the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'certificate', 'crl'},
    )
    mcp.tool(
        name_or_fn=pki.rotate_crl,
        name='pki-rotate-crl',
        description='Force a rotation of the certificate revocation list (CRL) in the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate', 'crl'},
    )
    mcp.tool(
        name_or_fn=pki.generate_intermediate,
        name='pki-generate-intermediate',
        description='Generate an intermediate CA certificate with the Vault PKI secrets engine (also known as: certificate authority).',
        annotations=cu_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.set_signed_intermediate,
        name='pki-set-signed-intermediate',
        description='Set a signed intermediate CA certificate for the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.sign_intermediate_certificate,
        name='pki-sign-intermediate-certificate',
        description='Sign an intermediate CA certificate (CSR) with the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate-authority', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.sign_self_issued,
        name='pki-sign-self-issued',
        description='Sign a self-issued certificate with the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.generate_certificate,
        name='pki-generate-certificate',
        description='Generate a private key and leaf certificate against a role in the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.sign_certificate,
        name='pki-sign-certificate',
        description='Sign a CSR (Certificate Signing Request) against a role in the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.read_certificate,
        name='pki-read-certificate',
        description='Read a certificate by serial number from the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.list_certificates,
        name='pki-list-certificates',
        description='List certificates issued by the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.revoke_certificate,
        name='pki-revoke-certificate',
        description='Revoke a certificate by serial number in the Vault PKI secrets engine.',
        annotations=del_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.tidy_certificates,
        name='pki-tidy-certificates',
        description='Clean up expired certificates in the Vault PKI secrets engine.',
        annotations=del_annotations,
        tags={'pki', 'certificate'},
    )
    mcp.tool(
        name_or_fn=pki.read_crl_configuration,
        name='pki-read-crl-configuration',
        description='Read the certificate revocation list (CRL) configuration for the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'crl', 'configuration'},
    )
    mcp.tool(
        name_or_fn=pki.set_crl_configuration,
        name='pki-set-crl-configuration',
        description='Set the certificate revocation list (CRL) configuration for the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'crl', 'configuration'},
    )
    mcp.tool(
        name_or_fn=pki.read_urls,
        name='pki-read-urls',
        description='Read the URL configuration (issuing certificates, CRL distribution points, OCSP servers) for the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'configuration'},
    )
    mcp.tool(
        name_or_fn=pki.set_urls,
        name='pki-set-urls',
        description='Set the URL configuration (issuing certificates, CRL distribution points, OCSP servers) for the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'configuration'},
    )
    mcp.tool(
        name_or_fn=pki.submit_ca_information,
        name='pki-submit-ca-information',
        description='Submit CA certificate and private key information to the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'certificate-authority'},
    )
    mcp.tool(
        name_or_fn=pki.create_update_role,
        name='pki-create-update-role',
        description='Create or update a role that governs certificate issuance in the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'role'},
    )
    mcp.tool(
        name_or_fn=pki.list_roles,
        name='pki-list-roles',
        description='List roles configured in the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'role'},
    )
    mcp.tool(
        name_or_fn=pki.read_role,
        name='pki-read-role',
        description='Read a role configured in the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'role'},
    )
    mcp.tool(
        name_or_fn=pki.delete_role,
        name='pki-delete-role',
        description='Delete a role from the Vault PKI secrets engine.',
        annotations=del_annotations,
        tags={'pki', 'role'},
    )
    mcp.tool(
        name_or_fn=pki.read_issuer,
        name='pki-read-issuer',
        description='Read an issuer configuration by reference ID in the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'issuer', 'certificate-authority'},
    )
    mcp.tool(
        name_or_fn=pki.list_issuers,
        name='pki-list-issuers',
        description='List all issuers configured in the Vault PKI secrets engine.',
        annotations=rl_annotations,
        tags={'pki', 'issuer', 'certificate-authority'},
    )
    mcp.tool(
        name_or_fn=pki.update_issuer,
        name='pki-update-issuer',
        description='Update an issuer configuration in the Vault PKI secrets engine.',
        annotations=cu_annotations,
        tags={'pki', 'issuer', 'certificate-authority'},
    )
    mcp.tool(
        name_or_fn=pki.revoke_issuer,
        name='pki-revoke-issuer',
        description='Revoke an issuer in the Vault PKI secrets engine.',
        annotations=del_annotations,
        tags={'pki', 'issuer', 'certificate-authority'},
    )
    # policy (also known as: ACL policy, access policy, permissions policy)
    mcp.tool(
        name_or_fn=policy.create_update,
        name='policy-create-or-update',
        description='Create or update a Vault ACL policy (also known as: access policy, permissions policy).',
        annotations=cu_annotations,
        tags={'policy', 'acl-policy', 'permissions'},
    )
    mcp.tool(
        name_or_fn=policy.delete,
        name='policy-delete',
        description='Delete a Vault ACL policy (also known as: access policy, permissions policy).',
        annotations=del_annotations,
        tags={'acl-policy', 'policy', 'permissions'},
    )
    mcp.tool(
        name_or_fn=policy.read,
        name='policy-read',
        description='Read a Vault ACL policy (also known as: access policy, permissions policy) by name.',
        annotations=rl_annotations,
        tags={'acl-policy', 'policy', 'permissions'},
    )
    mcp.tool(
        name_or_fn=policy.list_,
        name='policies-list',
        description='List the existing Vault ACL policies (also known as: access policies, permissions policies).',
        annotations=rl_annotations,
        tags={'acl-policy', 'policy', 'permissions'},
    )
    # raft (also known as: Raft integrated storage, storage cluster, storage backend)
    mcp.tool(
        name_or_fn=raft.read_config,
        name='raft-config-read',
        description='Read the Raft integrated storage configuration and peer/node list (also known as: raft storage cluster, storage backend config).',
        annotations=rl_annotations,
        tags={'raft', 'storage', 'cluster'},
    )
    mcp.tool(
        name_or_fn=raft.join,
        name='raft-cluster-join',
        description='Join the current node to an existing Raft integrated storage cluster (also known as: raft storage cluster).',
        annotations=cu_annotations,
        tags={'raft', 'storage', 'cluster'},
    )
    mcp.tool(
        name_or_fn=raft.remove_node,
        name='raft-node-remove',
        description='Remove a node from the Raft integrated storage cluster (also known as: raft storage cluster).',
        annotations=del_annotations,
        tags={'raft', 'storage', 'cluster'},
    )
    mcp.tool(
        name_or_fn=raft.take_snapshot,
        name='raft-snapshot-take',
        description='Take a base64-encoded snapshot of the Raft integrated storage state (also known as: raft storage backup).',
        annotations=rl_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.restore_snapshot,
        name='raft-snapshot-restore',
        description='Restore Raft integrated storage state from a previously taken snapshot (also known as: raft storage restore).',
        annotations=cu_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.read_auto_snapshot_status,
        name='raft-auto-snapshot-status-read',
        description='Read the status of a named Raft auto-snapshot configuration (Vault Enterprise only; also known as: raft storage backup automation).',
        annotations=rl_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.read_auto_snapshot_config,
        name='raft-auto-snapshot-config-read',
        description='Read a named Raft auto-snapshot configuration (Vault Enterprise only; also known as: raft storage backup automation).',
        annotations=rl_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.list_auto_snapshot_configs,
        name='raft-auto-snapshot-configs-list',
        description='List all Raft auto-snapshot configurations (Vault Enterprise only; also known as: raft storage backup automation).',
        annotations=rl_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.create_update_auto_snapshot_config,
        name='raft-auto-snapshot-config-create-or-update',
        description='Create or update a named Raft auto-snapshot configuration (Vault Enterprise only; also known as: raft storage backup automation).',
        annotations=cu_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    mcp.tool(
        name_or_fn=raft.delete_auto_snapshot_config,
        name='raft-auto-snapshot-config-delete',
        description='Delete a named Raft auto-snapshot configuration (Vault Enterprise only; also known as: raft storage backup automation).',
        annotations=del_annotations,
        tags={'raft', 'storage', 'snapshot', 'backup'},
    )
    # secret (also known as: secret engines, mounts, secrets engines, backends, sys/mounts)
    mcp.tool(
        name_or_fn=secret.enable,
        name='secret-engine-enable',
        description='Enable a Vault secret engine (also known as: mount, secrets engine, backend) such as kv, database, pki, or transit.',
        annotations=cu_annotations,
        tags={'secret-engine', 'mounts', 'backend'},
    )
    mcp.tool(
        name_or_fn=secret.disable,
        name='secret-engine-disable',
        description='Disable an enabled Vault secret engine (also known as: mount, secrets engine, backend) at a given path.',
        annotations=del_annotations,
        tags={'secret-engine', 'mounts', 'backend'},
    )
    mcp.tool(
        name_or_fn=secret.list_,
        name='secret-engines-list',
        description='List the currently enabled Vault secret engines (also known as: mounts, secrets engines, mount points, backends, sys/mounts).',
        annotations=rl_annotations,
        tags={'secret-engine', 'mounts', 'backend'},
    )
    mcp.tool(
        name_or_fn=secret.move,
        name='secret-engine-move',
        description='Move an already-mounted Vault secret engine (also known as: mount, secrets engine, backend) to a new mount point/path.',
        annotations=cu_annotations,
        tags={'secret-engine', 'mounts', 'backend'},
    )
    mcp.tool(
        name_or_fn=secret.read_configuration,
        name='secret-engine-read-configuration',
        description='Read the configuration (TTLs and mount-specific settings) of a mounted Vault secret engine (also known as: mount, secrets engine, backend).',
        annotations=rl_annotations,
        tags={'secret-engine', 'mounts', 'backend', 'configuration'},
    )
    mcp.tool(
        name_or_fn=secret.tune_configuration,
        name='secret-engine-tune-configuration',
        description='Tune configuration parameters for a mounted Vault secret engine (also known as: mount, secrets engine, backend).',
        annotations=cu_annotations,
        tags={'secret-engine', 'mounts', 'backend', 'configuration'},
    )
    mcp.tool(
        name_or_fn=secret.retrieve_option,
        name='secret-engine-retrieve-option',
        description="Retrieve a specific option value from a mounted Vault secret engine's configuration (also known as: mount, secrets engine, backend).",
        annotations=rl_annotations,
        tags={'secret-engine', 'mounts', 'backend', 'configuration'},
    )
    # transit (also known as: transit secrets engine, encryption as a service, encryption engine)
    mcp.tool(
        name_or_fn=transit.create,
        name='transit-engine-encryption-key-create',
        description='Create an encryption key in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.update_config,
        name='transit-engine-encryption-key-update-config',
        description='Update the configuration of an encryption key in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.read,
        name='transit-engine-encryption-key-read',
        description='Read an encryption key from the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=rl_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.list_,
        name='transit-engine-encryption-keys-list',
        description='List encryption keys in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=rl_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.delete,
        name='transit-engine-encryption-key-delete',
        description='Delete an encryption key from the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=del_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.rotate,
        name='transit-engine-encryption-key-rotate',
        description='Rotate an encryption key in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service'},
    )
    mcp.tool(
        name_or_fn=transit.encrypt,
        name='transit-engine-encrypt-plaintext',
        description='Encrypt plaintext using a key in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service', 'encrypt'},
    )
    mcp.tool(
        name_or_fn=transit.decrypt,
        name='transit-engine-decrypt-ciphertext',
        description='Decrypt ciphertext using a key in the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-key', 'encryption-as-a-service', 'decrypt'},
    )
    mcp.tool(
        name_or_fn=transit.generate,
        name='transit-engine-generate-random-bytes',
        description='Generate cryptographically secure random bytes through the Vault transit secrets engine (also known as: encryption as a service, encryption engine).',
        annotations=cu_annotations,
        tags={'transit', 'encryption-as-a-service', 'random-bytes'},
    )


def prompt_provider(mcp: FastMCP) -> None:
    """define implemented prompt integrations"""
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.example_policy,
            name='example-acl-policy',
            description='Display an example Vault ACL policy (also known as: access policy, permissions policy) document.',
            tags={'acl-policy', 'policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.generate_policy,
            name='generate-acl-policy',
            description='Generate a Vault ACL policy (also known as: access policy, permissions policy) example from a list of input paths.',
            tags={'acl-policy', 'policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.generate_smart_policy,
            name='generate-smart-acl-policy',
            description='Generate a context-aware Vault ACL policy (also known as: access policy, permissions policy) using the current live Vault state (mounted secret engines, auth methods, existing policies).',
            tags={'acl-policy', 'policy'},
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=multi.diagnose_vault_state,
            name='diagnose-vault-state',
            description='Diagnose the overall current state of the Vault server across multiple subsystems.',
            tags={'multiple'},
        )
    )


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
    prompt_provider(mcp)
