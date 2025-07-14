"""test vault transit mcp integrations"""

import pytest

from fastmcp import FastMCP, Client, exceptions

from mcp_bindings import server, provider

mcp: FastMCP = FastMCP(name='Vault', lifespan=server.server_lifespan)


@pytest.mark.asyncio
async def test_run() -> None:
    async with Client(mcp) as client:
        provider.provider(mcp)

        # enable transit
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'transit'})
        except exceptions.ToolError:
            pass

        # create
        result = await client.call_tool(name='transit-engine-encryption-key-create', arguments={'name': 'mykey'})
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

        # delete: TODO when functionality expanded for `create` then configure key that is deletable, and re-add this test
        # result = await client.call_tool(name='transit-engine-encryption-key-delete', arguments={'name': 'mykey'})
        # assert result[0]
