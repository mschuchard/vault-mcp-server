"""mcp vault integration provider"""

from fastmcp import FastMCP
from fastmcp.resources import Resource
from fastmcp.prompts import Prompt

from vault_mcp_server.vault.secret import database, kv2, pki, transit
from vault_mcp_server.vault.sys import audit, auth, policy, secret


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
            tags=['audit'],
            annotations={'readOnlyHint': True, 'idempotentHint': True},
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=auth.list_,
            uri='auth://engines',
            name='enabled-authentication-engines',
            description='List the available enabled Vault authentication engines',
            mime_type='application/json',
            tags=['authentication'],
            annotations={'readOnlyHint': True, 'idempotentHint': True},
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=policy.list_,
            uri='sys://policies',
            name='configured-acl-policies',
            description='List the available configured Vault ACL policies',
            mime_type='application/json',
            tags=['acl-policy'],
            annotations={'readOnlyHint': True, 'idempotentHint': True},
        )
    )
    mcp.add_resource(
        Resource.from_function(
            fn=secret.list_,
            uri='secret://engines',
            name='enabled-secret-engines',
            description='List the available enabled Vault secret engines',
            mime_type='application/json',
            tags=['secret-engine'],
            annotations={'readOnlyHint': True, 'idempotentHint': True},
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
    mcp.tool(name_or_fn=audit.enable, name='audit-device-enable', annotations=cu_annotations, tags=['audit'])
    mcp.tool(name_or_fn=audit.disable, name='audit-device-disable', annotations=del_annotations, tags=['audit'])
    mcp.tool(name_or_fn=audit.list_, name='audit-devices-list', annotations=rl_annotations, tags=['audit'])
    # auth
    mcp.tool(name_or_fn=auth.enable, name='authentication-engine-enable', annotations=cu_annotations, tags=['authentication'])
    mcp.tool(name_or_fn=auth.disable, name='authentication-engine-disable', annotations=del_annotations, tags=['authentication'])
    mcp.tool(name_or_fn=auth.list_, name='authentication-engines-list', annotations=rl_annotations, tags=['authentication'])
    mcp.tool(name_or_fn=auth.read, name='authentication-engine-read', annotations=rl_annotations, tags=['authentication'])
    mcp.tool(name_or_fn=auth.tune, name='authentication-engine-tune', annotations=cu_annotations, tags=['authentication'])
    # database
    mcp.tool(name_or_fn=database.read_connection, name='database-connection-read', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.list_connections, name='database-connections-list', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.delete_connection, name='database-connection-delete', annotations=del_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.reset_connection, name='database-connection-reset', annotations=cu_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.rotate_root_credentials, name='database-connection-rotate-root', annotations=cu_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.create_role, name='database-role-create', annotations=cu_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.read_role, name='database-role-read', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.list_roles, name='database-roles-list', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.delete_role, name='database-role-delete', annotations=del_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.generate_credentials, name='database-credentials-generate', annotations=cu_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.create_static_role, name='database-static-role-create', annotations=cu_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.read_static_role, name='database-static-role-read', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.list_static_roles, name='database-static-roles-list', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.delete_static_role, name='database-static-role-delete', annotations=del_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.get_static_credentials, name='database-static-credentials-get', annotations=rl_annotations, tags=['database'])
    mcp.tool(name_or_fn=database.rotate_static_role_credentials, name='database-static-credentials-rotate', annotations=cu_annotations, tags=['database'])
    # kv2
    mcp.tool(name_or_fn=kv2.create_update, name='kv2-create-or-update', annotations=cu_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.delete, name='kv2-delete', annotations=del_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.undelete, name='kv2-undelete', annotations=cu_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.read, name='kv2-read', annotations=rl_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.list_, name='kv2-list', annotations=rl_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.read_secret_metadata, name='kv2-metadata-and-versions', annotations=rl_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.patch, name='kv2-patch', annotations=cu_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.configure, name='kv2-configure-backend', annotations=cu_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.read_configuration, name='kv2-read-backend-configuration', annotations=rl_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.delete_latest_version_of_secret, name='kv2-delete-latest-version', annotations=del_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.delete_secret_versions, name='kv2-delete-specific-versions', annotations=del_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.destroy, name='kv2-destroy-versions', annotations=del_annotations, tags=['key-value-v2'])
    mcp.tool(name_or_fn=kv2.update_metadata, name='kv2-update-metadata', annotations=cu_annotations, tags=['key-value-v2'])
    # pki
    mcp.tool(name_or_fn=pki.generate_root, name='pki-generate-root-ca', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.delete_root, name='pki-delete-root-ca', annotations=del_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_root_certificate, name='pki-read-root-ca', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_root_certificate_chain, name='pki-read-root-ca-chain', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_crl, name='pki-read-crl', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.rotate_crl, name='pki-rotate-crl', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.generate_intermediate, name='pki-generate-intermediate', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.set_signed_intermediate, name='pki-set-signed-intermediate', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.sign_intermediate_certificate, name='pki-sign-intermediate-certificate', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.sign_self_issued, name='pki-sign-self-issued', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.generate_certificate, name='pki-generate-certificate', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.sign_certificate, name='pki-sign-certificate', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_certificate, name='pki-read-certificate', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.list_certificates, name='pki-list-certificates', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.revoke_certificate, name='pki-revoke-certificate', annotations=del_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.tidy_certificates, name='pki-tidy-certificates', annotations=del_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_crl_configuration, name='pki-read-crl-configuration', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.set_crl_configuration, name='pki-set-crl-configuration', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_urls, name='pki-read-urls', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.set_urls, name='pki-set-urls', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.submit_ca_information, name='pki-submit-ca-information', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.create_update_role, name='pki-create-update-role', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.list_roles, name='pki-list-roles', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_role, name='pki-read-role', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.delete_role, name='pki-delete-role', annotations=del_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.read_issuer, name='pki-read-issuer', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.list_issuers, name='pki-list-issuers', annotations=rl_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.update_issuer, name='pki-update-issuer', annotations=cu_annotations, tags=['pki'])
    mcp.tool(name_or_fn=pki.revoke_issuer, name='pki-revoke-issuer', annotations=del_annotations, tags=['pki'])
    # policy
    mcp.tool(name_or_fn=policy.create_update, name='policy-create-or-update', annotations=cu_annotations, tags=['policy'])
    mcp.tool(name_or_fn=policy.delete, name='policy-delete', annotations=del_annotations, tags=['acl-policy'])
    mcp.tool(name_or_fn=policy.read, name='policy-read', annotations=rl_annotations, tags=['acl-policy'])
    mcp.tool(name_or_fn=policy.list_, name='policies-list', annotations=rl_annotations, tags=['acl-policy'])
    # secret
    mcp.tool(name_or_fn=secret.enable, name='secret-engine-enable', annotations=cu_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.disable, name='secret-engine-disable', annotations=del_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.list_, name='secret-engines-list', annotations=rl_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.move, name='secret-engine-move', annotations=cu_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.read_configuration, name='secret-engine-read-configuration', annotations=rl_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.tune_configuration, name='secret-engine-tune-configuration', annotations=cu_annotations, tags=['secret-engine'])
    mcp.tool(name_or_fn=secret.retrieve_option, name='secret-engine-retrieve-option', annotations=rl_annotations, tags=['secret-engine'])
    # transit
    mcp.tool(name_or_fn=transit.create, name='transit-engine-encryption-key-create', annotations=cu_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.update_config, name='transit-engine-encryption-key-update-config', annotations=cu_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.read, name='transit-engine-encryption-key-read', annotations=rl_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.list_, name='transit-engine-encryption-keys-list', annotations=rl_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.delete, name='transit-engine-encryption-key-delete', annotations=del_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.rotate, name='transit-engine-encryption-key-rotate', annotations=cu_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.encrypt, name='transit-engine-encrypt-plaintext', annotations=cu_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.decrypt, name='transit-engine-decrypt-ciphertext', annotations=cu_annotations, tags=['transit'])
    mcp.tool(name_or_fn=transit.generate, name='transit-engine-generate-random-bytes', annotations=cu_annotations, tags=['transit'])


def prompt_provider(mcp: FastMCP) -> None:
    """define implemented prompt integrations"""
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.example_policy,
            name='example-acl-policy',
            tags=['acl-policy'],
        )
    )
    mcp.add_prompt(
        Prompt.from_function(
            fn=policy.generate_policy,
            name='generate-acl-policy',
            tags=['acl-policy'],
        )
    )


def provider(mcp: FastMCP) -> None:
    """define implemented integrations"""
    resource_provider(mcp)
    tool_provider(mcp)
    prompt_provider(mcp)
