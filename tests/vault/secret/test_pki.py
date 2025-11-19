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
        intermediate_csr = result.data.get('csr')

        result = await client.call_tool(name='pki-sign-intermediate-certificate', arguments={'csr': intermediate_csr, 'common_name': 'www.example.com'})
        assert result.data.get('certificate') is not None
        intermediate_cert = result.data.get('certificate')

        # test set_signed_intermediate
        result = await client.call_tool(name='pki-set-signed-intermediate', arguments={'certificate': intermediate_cert})
        assert result.data is not None

        result = await client.call_tool(name='pki-generate-certificate', arguments={'role': role, 'common_name': 'www.example.com'})
        assert result.data.get('certificate') is not None

        # TODO: need csr
        # result = await client.call_tool(name='pki-sign-certificate', arguments={'role': role, 'common_name': 'www.example.com', 'csr': result.data.get('csr')})
        # assert result.data.get('certificate') is not None

        # test CRL operations
        result = await client.call_tool(name='pki-read-crl')
        assert result.data is not None

        result = await client.call_tool(name='pki-rotate-crl')
        assert result.data is not None

        result = await client.call_tool(name='pki-read-crl-configuration')
        assert result.data is not None

        result = await client.call_tool(name='pki-set-crl-configuration', arguments={'expiry': '72h'})
        assert result.data is not None

        # test URL configuration
        result = await client.call_tool(name='pki-read-urls')
        assert result.data is not None

        result = await client.call_tool(
            name='pki-set-urls',
            arguments={
                'params': {
                    'issuing_certificates': ['http://127.0.0.1:8200/v1/pki/ca'],
                    'crl_distribution_points': ['http://127.0.0.1:8200/v1/pki/crl'],
                }
            },
        )
        assert result.data is not None

        # verify URL configuration was set
        result = await client.call_tool(name='pki-read-urls')
        assert 'http://127.0.0.1:8200/v1/pki/ca' in result.data.get('issuing_certificates', [])
        assert 'http://127.0.0.1:8200/v1/pki/crl' in result.data.get('crl_distribution_points', [])

        # test issuer operations (Vault 1.11+)
        result = await client.call_tool(name='pki-list-issuers')
        assert result.data is not None
        if len(result.data) > 0:
            issuer_ref = result.data[0]

            result = await client.call_tool(name='pki-read-issuer', arguments={'issuer_ref': issuer_ref})
            assert result.data is not None

            result = await client.call_tool(
                name='pki-update-issuer',
                arguments={'issuer_ref': issuer_ref, 'extra_params': {'issuer_name': 'example-issuer'}},
            )
            assert result.data is not None

        # list
        result = await client.call_tool(name='pki-list-certificates')
        assert len(result.data) > 0
        last_cert: str = result.data[-1]

        # read
        result = await client.call_tool(name='pki-read-root-ca')
        assert 'BEGIN CERTIFICATE' in result.data

        result = await client.call_tool(name='pki-read-certificate', arguments={'serial': 'ca'})
        assert result.data.get('certificate') is not None

        result = await client.call_tool(name='pki-read-root-ca-chain')
        assert 'BEGIN CERTIFICATE' in result.data

        result = await client.call_tool(name='pki-read-role', arguments={'name': role})
        assert result.data.get('use_pss') is not None

        # delete
        result = await client.call_tool(name='pki-delete-root-ca', arguments={})
        assert result.data['data'] is None
        assert result.data.get('mount_type') == 'pki'

        result = await client.call_tool(name='pki-revoke-certificate', arguments={'serial_number': last_cert})
        assert result.data.get('revocation_time') is not None

        result = await client.call_tool(name='pki-tidy-certificates', arguments={})
        assert result.data.get('success') is True

        result = await client.call_tool(name='pki-delete-role', arguments={'name': role})
        assert result.data.get('success') is True


@pytest.mark.asyncio
async def test_pki_submit_ca_information() -> None:
    """Test submitting CA information (certificate + private key bundle)"""
    async with dev.client as client:
        # enable pki at default mount
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'pki'})
        except exceptions.ToolError:
            pass

        # generate a root CA to get credentials
        result = await client.call_tool(
            name='pki-generate-root-ca',
            arguments={'type': 'exported', 'common_name': 'test.example.com'},
        )
        assert result.data.get('certificate') is not None
        assert result.data.get('private_key') is not None

        # create PEM bundle
        pem_bundle = result.data['certificate'] + '\n' + result.data['private_key']

        # test submit_ca_information (overwrites existing CA)
        result = await client.call_tool(name='pki-submit-ca-information', arguments={'pem_bundle': pem_bundle})
        assert result.data is not None

        # verify it was imported by reading the certificate
        result = await client.call_tool(name='pki-read-root-ca')
        assert 'BEGIN CERTIFICATE' in result.data

        # cleanup
        await client.call_tool(name='pki-delete-root-ca', arguments={})


@pytest.mark.asyncio
async def test_pki_sign_self_issued() -> None:
    """Test signing self-issued certificates"""
    async with dev.client as client:
        # enable pki
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'pki'})
        except exceptions.ToolError:
            pass

        # generate a root CA
        result = await client.call_tool(
            name='pki-generate-root-ca',
            arguments={'type': 'exported', 'common_name': 'root.example.com'},
        )
        assert result.data.get('certificate') is not None
        self_issued_cert = result.data['certificate']

        # test sign_self_issued
        result = await client.call_tool(name='pki-sign-self-issued', arguments={'certificate': self_issued_cert})
        assert result.data is not None

        # cleanup
        await client.call_tool(name='pki-delete-root-ca', arguments={})


@pytest.mark.asyncio
async def test_pki_issuer_revocation() -> None:
    """Test issuer revocation"""
    async with dev.client as client:
        # enable pki
        try:
            await client.call_tool(name='secret-engine-enable', arguments={'engine': 'pki'})
        except exceptions.ToolError:
            pass

        # generate a root CA
        result = await client.call_tool(
            name='pki-generate-root-ca',
            arguments={'type': 'internal', 'common_name': 'issuer-test.example.com'},
        )
        assert result.data is not None

        # list issuers
        result = await client.call_tool(name='pki-list-issuers')
        assert len(result.data) > 0
        issuer_ref = result.data[0]

        # revoke the issuer
        result = await client.call_tool(name='pki-revoke-issuer', arguments={'issuer_ref': issuer_ref})
        assert result.data is not None

        # cleanup
        await client.call_tool(name='pki-delete-root-ca', arguments={})
