"""test vault pki mcp integrations"""

import pytest

from fastmcp import exceptions

from vault_mcp_server import dev


@pytest.mark.asyncio
async def test_pki() -> None:
    async with dev.client as client:
        # enable pki
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'pki'})
        except exceptions.ToolError:
            pass

        # roles create_update and list for later
        result = await client.call_tool(
            name='pki-create-update-role',
            arguments={'name': 'example', 'extra_params': {'allowed_domains': 'example.com', 'allow_subdomains': True, 'max_ttl': '72h'}},
        )
        assert result.data.get('use_pss') is not None

        result = await client.call_tool(name='pki-list-roles')
        assert result.data == ['example']
        role: str = result.data[0]

        # create_update
        result = await client.call_tool(name='pki-generate-root-ca', arguments={'type': 'exported', 'common_name': 'www.example.com'})
        assert result.data.get('certificate') is not None
        assert result.data.get('private_key') is not None

        result = await client.call_tool(name='pki-generate-intermediate', arguments={'type': 'exported', 'common_name': 'www.example.com'})
        assert result.data.get('csr') is not None

        result = await client.call_tool(name='pki-sign-intermediate-certificate', arguments={'csr': result.data.get('csr'), 'common_name': 'www.example.com'})
        assert result.data.get('certificate') is not None

        result = await client.call_tool(name='pki-generate-certificate', arguments={'role': role, 'common_name': 'www.example.com'})
        assert result.data.get('certificate') is not None

        # TODO: need csr
        # result = await client.call_tool(name='pki-sign-certificate', arguments={'role': role, 'common_name': 'www.example.com', 'csr': result.data.get('csr')})
        # assert result.data.get('certificate') is not None

        # list
        result = await client.call_tool(name='pki-list-certificates')
        assert len(result.data) > 0
        last_cert: str = result.data[-1]

        # read
        result = await client.call_tool(name='pki-read-root-ca')
        assert result.data is not None

        result = await client.call_tool(name='pki-read-certificate', arguments={'serial': 'ca'})
        assert result.data is not None

        result = await client.call_tool(name='pki-read-root-ca-chain')
        assert result.data is not None

        result = await client.call_tool(name='pki-read-role', arguments={'name': role})
        assert result.data.get('use_pss') is not None

        # delete
        result = await client.call_tool(name='pki-delete-root-ca', arguments={})
        assert result.data is not None

        result = await client.call_tool(name='pki-revoke-certificate', arguments={'serial_number': last_cert})
        assert result.data.get('revocation_time') is not None

        result = await client.call_tool(name='pki-tidy-certificates', arguments={})
        assert result.data.get('success') is True

        result = await client.call_tool(name='pki-delete-role', arguments={'name': role})
        assert result.data.get('success') is True
