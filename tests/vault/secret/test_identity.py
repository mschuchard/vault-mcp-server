"""test vault identity mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_identity_entity() -> None:
    async with dev.client as client:
        # create
        result = await client.call_tool(
            name='identity-entity-create-or-update',
            arguments={'name': 'test-entity', 'metadata': {'team': 'ops'}, 'policies': []},
        )
        assert isinstance(result.data, dict)
        assert result.data.get('id') is not None
        entity_id: str = result.data['id']

        # read by id
        result = await client.call_tool(name='identity-entity-read', arguments={'entity_id': entity_id})
        assert result.data.get('name') == 'test-entity'
        assert result.data.get('metadata') == {'team': 'ops'}

        # read by name
        result = await client.call_tool(name='identity-entity-read-by-name', arguments={'name': 'test-entity'})
        assert result.data.get('id') == entity_id

        # update
        result = await client.call_tool(
            name='identity-entity-update',
            arguments={'entity_id': entity_id, 'metadata': {'team': 'platform'}},
        )
        assert result.data.get('success') is True

        # verify update
        result = await client.call_tool(name='identity-entity-read', arguments={'entity_id': entity_id})
        assert result.data.get('metadata') == {'team': 'platform'}

        # list
        result = await client.call_tool(name='identity-entities-list')
        assert entity_id in result.data

        # lookup by id
        result = await client.call_tool(name='identity-entity-lookup', arguments={'entity_id': entity_id})
        assert result.data.get('id') == entity_id

        # lookup by name
        result = await client.call_tool(name='identity-entity-lookup', arguments={'name': 'test-entity'})
        assert result.data.get('id') == entity_id

        # delete
        result = await client.call_tool(name='identity-entity-delete', arguments={'entity_id': entity_id})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_entity_by_name_delete() -> None:
    async with dev.client as client:
        # create
        result = await client.call_tool(
            name='identity-entity-create-or-update',
            arguments={'name': 'test-entity-byname'},
        )
        assert result.data.get('id') is not None

        # delete by name
        result = await client.call_tool(name='identity-entity-delete-by-name', arguments={'name': 'test-entity-byname'})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_entity_merge() -> None:
    async with dev.client as client:
        # create two entities to merge
        result = await client.call_tool(name='identity-entity-create-or-update', arguments={'name': 'merge-source'})
        source_id: str = result.data['id']

        result = await client.call_tool(name='identity-entity-create-or-update', arguments={'name': 'merge-target'})
        target_id: str = result.data['id']

        # merge source into target
        result = await client.call_tool(
            name='identity-entities-merge',
            arguments={'from_entity_ids': [source_id], 'to_entity_id': target_id},
        )
        assert result.data.get('success') is True

        # verify target still exists; source should be gone
        result = await client.call_tool(name='identity-entity-read', arguments={'entity_id': target_id})
        assert result.data.get('id') == target_id

        # cleanup
        result = await client.call_tool(name='identity-entity-delete', arguments={'entity_id': target_id})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_entity_alias() -> None:
    async with dev.client as client:
        # create parent entity
        result = await client.call_tool(name='identity-entity-create-or-update', arguments={'name': 'alias-entity'})
        assert result.data.get('id') is not None
        entity_id: str = result.data['id']

        # retrieve the token auth accessor to use as mount_accessor
        result = await client.call_tool(name='authentication-engines-list')
        token_accessor: str = result.data['token/']['accessor']

        # create alias
        result = await client.call_tool(
            name='identity-entity-alias-create-or-update',
            arguments={'name': 'test-alias', 'canonical_id': entity_id, 'mount_accessor': token_accessor},
        )
        assert isinstance(result.data, dict)
        assert result.data.get('id') is not None
        alias_id: str = result.data['id']

        # read alias
        result = await client.call_tool(name='identity-entity-alias-read', arguments={'alias_id': alias_id})
        assert result.data.get('canonical_id') == entity_id
        assert result.data.get('name') == 'test-alias'

        # update alias
        result = await client.call_tool(
            name='identity-entity-alias-update',
            arguments={'alias_id': alias_id, 'name': 'test-alias-updated', 'canonical_id': entity_id, 'mount_accessor': token_accessor},
        )
        assert isinstance(result.data, dict)

        # list aliases
        result = await client.call_tool(name='identity-entity-aliases-list')
        assert alias_id in result.data

        # delete alias
        result = await client.call_tool(name='identity-entity-alias-delete', arguments={'alias_id': alias_id})
        assert result.data.get('success') is True

        # cleanup entity
        result = await client.call_tool(name='identity-entity-delete', arguments={'entity_id': entity_id})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_group() -> None:
    async with dev.client as client:
        # create entity to use as member
        result = await client.call_tool(name='identity-entity-create-or-update', arguments={'name': 'group-member-entity'})
        member_entity_id: str = result.data['id']

        # create group
        result = await client.call_tool(
            name='identity-group-create-or-update',
            arguments={'name': 'test-group', 'metadata': {'env': 'test'}, 'member_entity_ids': [member_entity_id]},
        )
        assert isinstance(result.data, dict)
        assert result.data.get('id') is not None
        group_id: str = result.data['id']

        # read by id
        result = await client.call_tool(name='identity-group-read', arguments={'group_id': group_id})
        assert result.data.get('name') == 'test-group'
        assert result.data.get('metadata') == {'env': 'test'}
        assert member_entity_id in result.data.get('member_entity_ids', [])

        # read by name
        result = await client.call_tool(name='identity-group-read-by-name', arguments={'name': 'test-group'})
        assert result.data.get('id') == group_id

        # update
        result = await client.call_tool(
            name='identity-group-update',
            arguments={'group_id': group_id, 'name': 'test-group', 'metadata': {'env': 'staging'}},
        )
        assert isinstance(result.data, dict)

        # verify update
        result = await client.call_tool(name='identity-group-read', arguments={'group_id': group_id})
        assert result.data.get('metadata') == {'env': 'staging'}

        # list
        result = await client.call_tool(name='identity-groups-list')
        assert group_id in result.data

        # lookup by id
        result = await client.call_tool(name='identity-group-lookup', arguments={'group_id': group_id})
        assert result.data.get('id') == group_id

        # lookup by name
        result = await client.call_tool(name='identity-group-lookup', arguments={'name': 'test-group'})
        assert result.data.get('id') == group_id

        # delete
        result = await client.call_tool(name='identity-group-delete', arguments={'group_id': group_id})
        assert result.data.get('success') is True

        # cleanup entity
        result = await client.call_tool(name='identity-entity-delete', arguments={'entity_id': member_entity_id})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_group_by_name_delete() -> None:
    async with dev.client as client:
        # create
        result = await client.call_tool(name='identity-group-create-or-update', arguments={'name': 'test-group-byname'})
        assert result.data.get('id') is not None

        # delete by name
        result = await client.call_tool(name='identity-group-delete-by-name', arguments={'name': 'test-group-byname'})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_group_alias() -> None:
    async with dev.client as client:
        # create parent group (external type required for group aliases)
        result = await client.call_tool(
            name='identity-group-create-or-update',
            arguments={'name': 'external-group', 'group_type': 'external'},
        )
        assert result.data.get('id') is not None
        group_id: str = result.data['id']

        # retrieve the token auth accessor
        result = await client.call_tool(name='authentication-engines-list')
        token_accessor: str = result.data['token/']['accessor']

        # create group alias
        result = await client.call_tool(
            name='identity-group-alias-create-or-update',
            arguments={'name': 'test-group-alias', 'canonical_id': group_id, 'mount_accessor': token_accessor},
        )
        assert isinstance(result.data, dict)
        assert result.data.get('id') is not None
        alias_id: str = result.data['id']

        # read group alias
        result = await client.call_tool(name='identity-group-alias-read', arguments={'alias_id': alias_id})
        assert result.data.get('canonical_id') == group_id
        assert result.data.get('name') == 'test-group-alias'

        # update group alias
        result = await client.call_tool(
            name='identity-group-alias-update',
            arguments={'alias_id': alias_id, 'name': 'test-group-alias-updated', 'canonical_id': group_id, 'mount_accessor': token_accessor},
        )
        assert isinstance(result.data, dict)

        # list group aliases
        result = await client.call_tool(name='identity-group-aliases-list')
        assert alias_id in result.data

        # delete group alias
        result = await client.call_tool(name='identity-group-alias-delete', arguments={'alias_id': alias_id})
        assert result.data.get('success') is True

        # cleanup group
        result = await client.call_tool(name='identity-group-delete', arguments={'group_id': group_id})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_identity_oidc() -> None:
    async with dev.client as client:
        # configure issuer
        result = await client.call_tool(
            name='identity-oidc-configure',
            arguments={'issuer': 'http://127.0.0.1:8200'},
        )
        assert result.data is not None

        # read configuration
        result = await client.call_tool(name='identity-oidc-configuration-read')
        assert result.data.get('issuer') == 'http://127.0.0.1:8200'

        # create named key
        result = await client.call_tool(
            name='identity-oidc-key-create-or-update',
            arguments={'name': 'test-key', 'rotation_period': '24h', 'verification_ttl': '24h', 'algorithm': 'RS256'},
        )
        assert result.data is not None

        # read named key
        result = await client.call_tool(name='identity-oidc-key-read', arguments={'name': 'test-key'})
        assert result.data.get('algorithm') == 'RS256'
        assert result.data.get('rotation_period') is not None

        # list named keys
        result = await client.call_tool(name='identity-oidc-keys-list')
        assert 'test-key' in result.data

        # rotate named key
        result = await client.call_tool(name='identity-oidc-key-rotate', arguments={'name': 'test-key'})
        assert result.data.get('success') is True

        # create role (key must allow this role's client_id; use wildcard)
        result = await client.call_tool(
            name='identity-oidc-key-create-or-update',
            arguments={'name': 'test-key', 'allowed_client_ids': ['*']},
        )
        assert result.data is not None

        result = await client.call_tool(
            name='identity-oidc-role-create-or-update',
            arguments={'name': 'test-role', 'key': 'test-key', 'ttl': '1h'},
        )
        assert result.data is not None

        # read role
        result = await client.call_tool(name='identity-oidc-role-read', arguments={'name': 'test-role'})
        assert result.data.get('key') == 'test-key'
        assert result.data.get('ttl') is not None

        # list roles
        result = await client.call_tool(name='identity-oidc-roles-list')
        assert 'test-role' in result.data

        # generate signed id token
        result = await client.call_tool(name='identity-oidc-token-generate', arguments={'name': 'test-role'})
        assert isinstance(result.data, str)
        assert len(result.data) > 0
        token: str = result.data

        # introspect token
        result = await client.call_tool(name='identity-oidc-token-introspect', arguments={'token': token})
        assert isinstance(result.data, dict)

        # well-known discovery
        result = await client.call_tool(name='identity-oidc-well-known-read')
        assert result.data.get('issuer') is not None
        assert result.data.get('jwks_uri') is not None

        # public keys (jwks)
        result = await client.call_tool(name='identity-oidc-public-keys-read')
        assert result.data.get('keys') is not None

        # cleanup role then key (key cannot be deleted while in use by a role)
        result = await client.call_tool(name='identity-oidc-role-delete', arguments={'name': 'test-role'})
        assert result.data.get('success') is True

        result = await client.call_tool(name='identity-oidc-key-delete', arguments={'name': 'test-key'})
        assert result.data.get('success') is True
