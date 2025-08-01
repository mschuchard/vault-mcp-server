"""test vault transit mcp integrations"""

import pytest

from fastmcp import exceptions

from tests import utils


@pytest.mark.asyncio
async def test_transit() -> None:
    async with utils.mcp_client() as client:
        # enable transit
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'transit'})
        except exceptions.ToolError:
            pass

        # create
        result = await client.call_tool(name='transit-engine-encryption-key-create', arguments={'name': 'mykey'})
        assert result[0]

        # update config
        result = await client.call_tool(
            name='transit-engine-encryption-key-update-config', arguments={'name': 'mykey', 'deletion_allowed': True, 'exportable': True}
        )
        assert result[0]

        # read
        result = await client.call_tool(name='transit-engine-encryption-key-read', arguments={'name': 'mykey'})
        assert result[0]

        # list
        result = await client.call_tool(name='transit-engine-encryption-keys-list')
        assert result[0]

        # rotate
        result = await client.call_tool(name='transit-engine-encryption-key-rotate', arguments={'name': 'mykey'})
        assert result[0]

        # encrypt
        result = await client.call_tool(name='transit-engine-encrypt-plaintext', arguments={'name': 'mykey', 'text': 'helloworld'})
        assert result[0]

        # decrypt: TODO need to parse `result` to obtain ciphertext for decryption
        # result = await client.call_tool(name='transit-engine-decrypt-ciphertext', arguments={'name': 'mykey', 'text': ''})
        # assert result[0]

        # generate
        result = await client.call_tool(name='transit-engine-generate-random-bytes', arguments={'num_bytes': 16})
        assert result[0]

        # delete
        result = await client.call_tool(name='transit-engine-encryption-key-delete', arguments={'name': 'mykey'})
        assert result[0]
