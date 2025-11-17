"""test vault kv2 mcp integrations"""

import pytest

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_kv2() -> None:
    async with dev.client as client:
        # 1. Configure Backend: Set max_versions to 2 globally
        result = await client.call_tool(name='kv2-configure-backend', arguments={'max_versions': 2})
        assert result.data.get('success') is True

        # 2. Read Backend Configuration: Verify max_versions is 2
        result = await client.call_tool(name='kv2-read-backend-configuration')
        assert result.data.get('max_versions') == 2

        # 3. Create/Update (Version 1)
        result = await client.call_tool(name='kv2-create-or-update', arguments={'path': 'mysecret', 'secret': {'foo': 'bar', 'baz': 'bat'}})
        assert result.data.get('version') == 1

        # 4. List
        result = await client.call_tool(name='kv2-list')
        assert result.data == ['mysecret']

        # 5. Read (Version 1)
        result = await client.call_tool(name='kv2-read', arguments={'path': 'mysecret'})
        assert result.data == {'foo': 'bar', 'baz': 'bat'}

        # 6. Patch/Update (Version 2)
        result = await client.call_tool(name='kv2-patch', arguments={'path': 'mysecret', 'secret': {'foobar': 'bazbat'}})
        assert result.data.get('version') == 2

        # 7. Update Metadata: Set max_versions to 5 for this specific secret
        result = await client.call_tool(name='kv2-update-metadata', arguments={'path': 'mysecret', 'max_versions': 5})
        assert result.data.get('success') is True

        # 8. Read Metadata (Check current version and max_versions override)
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result.data.get('current_version') == 2
        assert result.data.get('max_versions') == 5

        # 9. Soft Delete Latest Version (Version 2)
        result = await client.call_tool(name='kv2-delete-latest-version', arguments={'path': 'mysecret'})
        assert result.data.get('success') is True

        # 10. Read Metadata (Check V2 soft delete: deletion_time is a timestamp, V1 is active: deletion_time is "")
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result.data.get('versions').get('2').get('deletion_time') != ''
        assert result.data.get('versions').get('1').get('deletion_time') == ''

        # 11. Undelete Version 2
        result = await client.call_tool(name='kv2-undelete', arguments={'versions': [2], 'path': 'mysecret'})
        assert result.data.get('success') is True

        # 12. Soft Delete Specific Versions (Version 1)
        result = await client.call_tool(name='kv2-delete-specific-versions', arguments={'versions': [1], 'path': 'mysecret'})
        assert result.data.get('success') is True

        # 13. Read Metadata (Check V1 soft delete: deletion_time is a timestamp, V2 is active: deletion_time is "")
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        assert result.data.get('versions').get('1').get('deletion_time') != ''
        assert result.data.get('versions').get('2').get('deletion_time') == ''

        # 14. Destroy Version 1 (It must be soft-deleted first)
        result = await client.call_tool(name='kv2-destroy-versions', arguments={'versions': [1], 'path': 'mysecret'})
        assert result.data.get('success') is True

        # 15. Read Metadata (Check destroy: Version 1 should have 'destroyed': True)
        result = await client.call_tool(name='kv2-metadata-and-versions', arguments={'path': 'mysecret'})
        # The key remains, but the 'destroyed' flag is set to True
        assert result.data.get('versions').get('1').get('destroyed') is True

        # 16. Cleanup (Delete metadata and all remaining versions)
        result = await client.call_tool(name='kv2-delete', arguments={'path': 'mysecret'})
        assert result.data.get('success') is True
