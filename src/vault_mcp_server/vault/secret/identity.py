"""vault identity"""

from typing import Annotated

from fastmcp import Context
import hvac.exceptions


# ---------------------------------------------------------------------------
# Entity
# ---------------------------------------------------------------------------


def create_or_update_entity(
    ctx: Context,
    name: Annotated[str, 'Name of the entity. Must be unique within the Vault namespace.'],
    entity_id: Annotated[str | None, 'ID of the entity. If set, updates the corresponding existing entity.'] = None,
    metadata: Annotated[dict | None, 'Arbitrary key-value metadata to associate with the entity.'] = None,
    policies: Annotated[list[str] | None, 'List of policies to be tied to the entity.'] = None,
    disabled: Annotated[bool, 'Whether the entity is disabled. Disabled entities cannot log in.'] = False,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """create or update an entity in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].create_or_update_entity(
        name=name,
        entity_id=entity_id,
        metadata=metadata,
        policies=policies,
        disabled=disabled,
        mount_point=mount_point,
    )['data']


async def read_entity(
    ctx: Context,
    entity_id: Annotated[str, 'The ID of the entity to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read an entity by ID from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_entity(
        entity_id=entity_id,
        mount_point=mount_point,
    )['data']


async def read_entity_by_name(
    ctx: Context,
    name: Annotated[str, 'The name of the entity to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read an entity by name from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_entity_by_name(
        name=name,
        mount_point=mount_point,
    )['data']


def update_entity(
    ctx: Context,
    entity_id: Annotated[str, 'The ID of the entity to update.'],
    name: Annotated[str | None, 'New name for the entity.'] = None,
    metadata: Annotated[dict | None, 'Arbitrary key-value metadata to associate with the entity.'] = None,
    policies: Annotated[list[str] | None, 'List of policies to be tied to the entity.'] = None,
    disabled: Annotated[bool | None, 'Whether the entity is disabled.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """update an existing entity by ID in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .update_entity(
            entity_id=entity_id,
            name=name,
            metadata=metadata,
            policies=policies,
            disabled=disabled,
            mount_point=mount_point,
        )
        .ok
    }


def delete_entity(
    ctx: Context,
    entity_id: Annotated[str, 'The ID of the entity to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete an entity by ID from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_entity(entity_id=entity_id, mount_point=mount_point).ok}


def delete_entity_by_name(
    ctx: Context,
    name: Annotated[str, 'The name of the entity to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete an entity by name from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_entity_by_name(name=name, mount_point=mount_point).ok}


async def list_entities(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all entity IDs in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_entities(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def merge_entities(
    ctx: Context,
    from_entity_ids: Annotated[list[str], 'List of entity IDs to be merged into the target entity.'],
    to_entity_id: Annotated[str, 'The ID of the target entity that the others will be merged into.'],
    force: Annotated[bool, 'Setting this to true will bypass merge restrictions resulting from conflicting identity aliases.'] = False,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """merge multiple entities into a single target entity in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .merge_entities(
            from_entity_ids=from_entity_ids,
            to_entity_id=to_entity_id,
            force=force,
            mount_point=mount_point,
        )
        .ok
    }


# ---------------------------------------------------------------------------
# Entity Alias
# ---------------------------------------------------------------------------


def create_or_update_entity_alias(
    ctx: Context,
    name: Annotated[
        str,
        'Name of the alias. Should be the identifier of the client in the authentication source (e.g. a username in userpass, or a GitHub username).',
    ],
    canonical_id: Annotated[str, 'Entity ID to which this alias belongs.'],
    mount_accessor: Annotated[str, 'Accessor of the auth mount to which this alias belongs.'],
    alias_id: Annotated[str | None, 'ID of the entity alias. If set, updates the corresponding existing alias.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """create or update an entity alias in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].create_or_update_entity_alias(
        name=name,
        canonical_id=canonical_id,
        mount_accessor=mount_accessor,
        alias_id=alias_id,
        mount_point=mount_point,
    )['data']


async def read_entity_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the entity alias to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read an entity alias by ID from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_entity_alias(alias_id=alias_id, mount_point=mount_point)['data']


def update_entity_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the entity alias to update.'],
    name: Annotated[str, 'New name for the alias.'],
    canonical_id: Annotated[str, 'Entity ID to which this alias belongs.'],
    mount_accessor: Annotated[str, 'Accessor of the auth mount to which this alias belongs.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """update an existing entity alias by ID in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].update_entity_alias(
        alias_id=alias_id,
        name=name,
        canonical_id=canonical_id,
        mount_accessor=mount_accessor,
        mount_point=mount_point,
    )['data']


async def list_entity_aliases(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all entity alias IDs in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_entity_aliases(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete_entity_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the entity alias to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete an entity alias by ID from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_entity_alias(alias_id=alias_id, mount_point=mount_point).ok}


# ---------------------------------------------------------------------------
# Group
# ---------------------------------------------------------------------------


def create_or_update_group(
    ctx: Context,
    name: Annotated[str, 'Name of the group. Must be unique within the Vault namespace.'],
    group_id: Annotated[str | None, 'ID of the group. If set, updates the corresponding existing group.'] = None,
    group_type: Annotated[
        str, 'Type of the group. Can be "internal" (managed inside Vault) or "external" (managed by an external auth provider).'
    ] = 'internal',
    metadata: Annotated[dict | None, 'Arbitrary key-value metadata to associate with the group.'] = None,
    policies: Annotated[list[str] | None, 'List of policies to be tied to the group.'] = None,
    member_group_ids: Annotated[list[str] | None, 'List of group IDs to be assigned as sub-groups of this group (internal groups only).'] = None,
    member_entity_ids: Annotated[list[str] | None, 'List of entity IDs to be assigned as members of this group (internal groups only).'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """create or update a group in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].create_or_update_group(
        name=name,
        group_id=group_id,
        group_type=group_type,
        metadata=metadata,
        policies=policies,
        member_group_ids=member_group_ids,
        member_entity_ids=member_entity_ids,
        mount_point=mount_point,
    )['data']


async def read_group(
    ctx: Context,
    group_id: Annotated[str, 'The ID of the group to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read a group by ID from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_group(group_id=group_id, mount_point=mount_point)['data']


async def read_group_by_name(
    ctx: Context,
    name: Annotated[str, 'The name of the group to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read a group by name from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_group_by_name(name=name, mount_point=mount_point)['data']


def update_group(
    ctx: Context,
    group_id: Annotated[str, 'The ID of the group to update.'],
    name: Annotated[str, 'Name for the group.'],
    group_type: Annotated[str, 'Type of the group ("internal" or "external").'] = 'internal',
    metadata: Annotated[dict | None, 'Arbitrary key-value metadata to associate with the group.'] = None,
    policies: Annotated[list[str] | None, 'List of policies to be tied to the group.'] = None,
    member_group_ids: Annotated[list[str] | None, 'List of group IDs to be assigned as sub-groups (internal groups only).'] = None,
    member_entity_ids: Annotated[list[str] | None, 'List of entity IDs to be assigned as members (internal groups only).'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """update an existing group by ID in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .update_group(
            group_id=group_id,
            name=name,
            group_type=group_type,
            metadata=metadata,
            policies=policies,
            member_group_ids=member_group_ids,
            member_entity_ids=member_entity_ids,
            mount_point=mount_point,
        )
        .ok
    }


def delete_group(
    ctx: Context,
    group_id: Annotated[str, 'The ID of the group to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete a group by ID from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_group(group_id=group_id, mount_point=mount_point).ok}


def delete_group_by_name(
    ctx: Context,
    name: Annotated[str, 'The name of the group to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete a group by name from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_group_by_name(name=name, mount_point=mount_point).ok}


async def list_groups(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all group IDs in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_groups(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


# ---------------------------------------------------------------------------
# Group Alias
# ---------------------------------------------------------------------------


def create_or_update_group_alias(
    ctx: Context,
    name: Annotated[str, 'Name of the group alias. This is the identifier of the group in the external auth provider.'],
    canonical_id: Annotated[str, 'Group ID to which this alias belongs.'],
    mount_accessor: Annotated[str, 'Accessor of the auth mount to which this alias belongs.'],
    alias_id: Annotated[str | None, 'ID of the group alias. If set, updates the corresponding existing alias.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """create or update a group alias in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].create_or_update_group_alias(
        name=name,
        canonical_id=canonical_id,
        mount_accessor=mount_accessor,
        alias_id=alias_id,
        mount_point=mount_point,
    )['data']


async def read_group_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the group alias to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read a group alias by ID from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_group_alias(alias_id=alias_id, mount_point=mount_point)['data']


def update_group_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the group alias to update.'],
    name: Annotated[str, 'New name for the group alias.'],
    canonical_id: Annotated[str | None, 'Group ID to which this alias belongs.'] = None,
    mount_accessor: Annotated[str | None, 'Accessor of the auth mount to which this alias belongs.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """update an existing group alias by ID in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].update_group_alias(
        entity_id=alias_id,
        name=name,
        canonical_id=canonical_id,
        mount_accessor=mount_accessor,
        mount_point=mount_point,
    )['data']


async def list_group_aliases(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all group alias IDs in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_group_aliases(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete_group_alias(
    ctx: Context,
    alias_id: Annotated[str, 'The ID of the group alias to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete a group alias by ID from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_group_alias(entity_id=alias_id, mount_point=mount_point).ok}


# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------


async def lookup_entity(
    ctx: Context,
    name: Annotated[str | None, 'Name of the entity to look up.'] = None,
    entity_id: Annotated[str | None, 'ID of the entity to look up.'] = None,
    alias_name: Annotated[str | None, 'Name of the alias associated with the entity. Must be used with alias_accessor.'] = None,
    alias_accessor: Annotated[str | None, 'Accessor of the auth mount the alias belongs to. Must be used with alias_name.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """look up an entity by name, ID, or alias attributes in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].lookup_entity(
        name=name,
        entity_id=entity_id,
        alias_name=alias_name,
        alias_mount_accessor=alias_accessor,
        mount_point=mount_point,
    )['data']


async def lookup_group(
    ctx: Context,
    name: Annotated[str | None, 'Name of the group to look up.'] = None,
    group_id: Annotated[str | None, 'ID of the group to look up.'] = None,
    alias_name: Annotated[str | None, 'Name of the alias associated with the group. Must be used with alias_accessor.'] = None,
    alias_accessor: Annotated[str | None, 'Accessor of the auth mount the alias belongs to. Must be used with alias_name.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """look up a group by name, ID, or alias attributes in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].lookup_group(
        name=name,
        group_id=group_id,
        alias_name=alias_name,
        alias_mount_accessor=alias_accessor,
        mount_point=mount_point,
    )['data']


# ---------------------------------------------------------------------------
# OIDC Tokens
# ---------------------------------------------------------------------------


def configure_tokens_backend(
    ctx: Context,
    issuer: Annotated[
        str | None,
        'Issuer URL to be used in the "iss" claim of generated tokens. Must be a case-sensitive HTTPS URL. If not set, Vault\'s api_addr is used.',
    ] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """update the OIDC token issuer configuration in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].configure_tokens_backend(issuer=issuer, mount_point=mount_point)


async def read_token_backend_configuration(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read the OIDC token backend configuration from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_tokens_backend_configuration(mount_point=mount_point)['data']


def create_named_key(
    ctx: Context,
    name: Annotated[str, 'Name of the named key to create or update.'],
    rotation_period: Annotated[str, 'How often to rotate the signing key. Uses Go duration format (e.g. "24h", "7d").'] = '24h',
    verification_ttl: Annotated[str, 'Controls how long the public key will be available to verify JWTs after rotation. Uses Go duration format.'] = '24h',
    allowed_client_ids: Annotated[list[str] | None, 'List of role client IDs allowed to use this key for token generation. Use ["*"] to allow all.'] = None,
    algorithm: Annotated[str, 'Signing algorithm. One of "RS256", "RS384", "RS512", "ES256", "ES384", "ES512", "EdDSA".'] = 'RS256',
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """create or update a named signing key for OIDC token generation in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .create_named_key(
            name=name,
            rotation_period=rotation_period,
            verification_ttl=verification_ttl,
            allowed_client_ids=allowed_client_ids,
            algorithm=algorithm,
            mount_point=mount_point,
        )
        .ok
    }


async def read_named_key(
    ctx: Context,
    name: Annotated[str, 'Name of the named key to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read a named OIDC signing key from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_named_key(name=name, mount_point=mount_point)['data']


def delete_named_key(
    ctx: Context,
    name: Annotated[str, 'Name of the named key to delete. Keys in use by a role cannot be deleted.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete a named OIDC signing key from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_named_key(name=name, mount_point=mount_point).ok}


async def list_named_keys(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all named OIDC signing keys in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_named_keys(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def rotate_named_key(
    ctx: Context,
    name: Annotated[str, 'Name of the named key to rotate.'],
    verification_ttl: Annotated[
        str | None,
        'Post-rotation verification TTL override. Controls how long the old key is available for verification after rotation. Uses Go duration format.',
    ] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """manually rotate a named OIDC signing key in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .rotate_named_key(
            name=name,
            verification_ttl=verification_ttl,
            mount_point=mount_point,
        )
        .ok
    }


def create_or_update_role(
    ctx: Context,
    name: Annotated[str, 'Name of the OIDC token role to create or update.'],
    key: Annotated[str, "The named key to use for signing tokens. The key must already exist and must allow this role's client ID."],
    template: Annotated[str | None, 'JSON string template for the identity token claims. Supports Vault identity template syntax.'] = None,
    client_id: Annotated[str | None, 'Optional client ID for the role. If not set, Vault generates one.'] = None,
    ttl: Annotated[str, 'TTL of the generated tokens. Uses Go duration format (e.g. "1h"). Defaults to the key\'s verification_ttl.'] = '24h',
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """create or update an OIDC token role in the vault identity engine"""
    return {
        'success': ctx.request_context.lifespan_context['identity']
        .create_or_update_role(
            name=name,
            key=key,
            template=template,
            client_id=client_id,
            ttl=ttl,
            mount_point=mount_point,
        )
        .ok
    }


async def read_role(
    ctx: Context,
    name: Annotated[str, 'Name of the OIDC token role to read.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read an OIDC token role from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_role(name=name, mount_point=mount_point)['data']


def delete_role(
    ctx: Context,
    name: Annotated[str, 'Name of the OIDC token role to delete.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict[str, bool]:
    """delete an OIDC token role from the vault identity engine"""
    return {'success': ctx.request_context.lifespan_context['identity'].delete_role(name=name, mount_point=mount_point).ok}


async def list_roles(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> list[str]:
    """list all OIDC token roles in the vault identity engine"""
    try:
        return ctx.request_context.lifespan_context['identity'].list_roles(mount_point=mount_point)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def generate_signed_id_token(
    ctx: Context,
    name: Annotated[str, 'Name of the OIDC token role to generate a signed token for.'],
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> str:
    """generate a signed OIDC identity token for the specified role in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].generate_signed_id_token(name=name, mount_point=mount_point)['data']['token']


async def introspect_signed_id_token(
    ctx: Context,
    token: Annotated[str, 'The signed OIDC identity token (JWT) to introspect.'],
    client_id: Annotated[str | None, 'Optional client ID to verify the "aud" claim of the token against.'] = None,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """introspect and validate a signed OIDC identity token in the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].introspect_signed_id_token(
        token=token,
        client_id=client_id,
        mount_point=mount_point,
    )['data']


async def read_well_known_configurations(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read the OIDC well-known discovery configuration from the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_well_known_configurations(mount_point=mount_point)


async def read_active_public_keys(
    ctx: Context,
    mount_point: Annotated[str, 'The "path" the identity engine was mounted on.'] = 'identity',
) -> dict:
    """read the active OIDC public keys (JWKS) published by the vault identity engine"""
    return ctx.request_context.lifespan_context['identity'].read_active_public_keys(mount_point=mount_point)
