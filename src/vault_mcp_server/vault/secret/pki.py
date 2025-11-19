"""vault pki"""

from typing import Annotated, Literal

from fastmcp import Context
import hvac.exceptions


def generate_root(
    ctx: Context,
    type: Annotated[Literal['exported', 'internal', 'kms'], 'The type of key to generate for the root CA.'],
    common_name: Annotated[str, 'The requested common name for the root CA certificate.'],
    extra_params: Annotated[dict, 'Extra parameters for root generation (ttl, alt_names, ip_sans, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate a root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_root(type=type, common_name=common_name, extra_params=extra_params, mount_point=mount)['data']


def delete_root(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """delete the current root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].delete_root(mount_point=mount)


async def read_root_certificate(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> str:
    """read the current root ca certificate in raw DER-encoded format with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate(mount_point=mount)


async def read_root_certificate_chain(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> str:
    """read the current root ca certificate chain in PEM format with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate_chain(mount_point=mount)


async def read_crl(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> str:
    """read the current certificate revocation list (CRL) in PEM format with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_crl(mount_point=mount)


def rotate_crl(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """force a rotation of the certificate revocation list (CRL) with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].rotate_crl(mount_point=mount)


def generate_intermediate(
    ctx: Context,
    type: Annotated[Literal['exported', 'internal', 'kms'], 'The type of key to generate for the intermediate CA.'],
    common_name: Annotated[str, 'The requested common name for the intermediate CA certificate.'],
    extra_params: Annotated[dict, 'Extra parameters for intermediate generation (ttl, alt_names, ip_sans, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate an intermediate certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_intermediate(type=type, common_name=common_name, extra_params=extra_params, mount_point=mount)[
        'data'
    ]


def set_signed_intermediate(
    ctx: Context,
    certificate: Annotated[str, 'The signed intermediate certificate in PEM format.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """set a signed intermediate certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].set_signed_intermediate(certificate=certificate, mount_point=mount)


def sign_intermediate_certificate(
    ctx: Context,
    csr: Annotated[str, 'The PEM-encoded CSR (Certificate Signing Request) to sign.'],
    common_name: Annotated[str, 'The requested common name for the intermediate certificate.'],
    extra_params: Annotated[dict, 'Extra parameters for signing (ttl, format, max_path_length, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """sign an intermediate ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_intermediate(csr=csr, common_name=common_name, extra_params=extra_params, mount_point=mount)['data']


def sign_self_issued(
    ctx: Context,
    certificate: Annotated[str, 'The PEM-encoded self-issued certificate to sign.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """sign a self-issued certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_self_issued(certificate=certificate, mount_point=mount)


def generate_certificate(
    ctx: Context,
    role: Annotated[str, 'The name of the role to create the certificate against.'],
    common_name: Annotated[str, 'The requested common name for the certificate.'],
    extra_params: Annotated[dict, 'Extra parameters for certificate generation (ttl, alt_names, ip_sans, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate a private key and certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_certificate(name=role, common_name=common_name, extra_params=extra_params, mount_point=mount)[
        'data'
    ]


def sign_certificate(
    ctx: Context,
    role: Annotated[str, 'The name of the role to sign the certificate.'],
    csr: Annotated[str, 'The PEM-encoded CSR (Certificate Signing Request) to sign.'],
    common_name: Annotated[str, 'The requested common name for the certificate.'],
    extra_params: Annotated[dict, 'Extra parameters for signing (ttl, alt_names, ip_sans, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """sign a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_certificate(
        name=role, csr=csr, common_name=common_name, extra_params=extra_params, mount_point=mount
    )['data']


async def read_certificate(
    ctx: Context,
    serial: Annotated[str, 'The serial number of the certificate to read.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """read a certificate by serial number with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_certificate(serial=serial, mount_point=mount)['data']


async def list_certificates(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> list[str]:
    """list current certificates with the pki engine in vault"""
    try:
        return ctx.request_context.lifespan_context['pki'].list_certificates(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidRequest:
        return []


def revoke_certificate(
    ctx: Context,
    serial_number: Annotated[str, 'The serial number of the certificate to revoke.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """revoke a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].revoke_certificate(serial_number=serial_number, mount_point=mount)['data']


def tidy_certificates(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """cleanup expired certificates with the pki engine in vault"""
    return {'success': ctx.request_context.lifespan_context['pki'].tidy(mount_point=mount).ok}


async def read_crl_configuration(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """read the CRL configuration with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_crl_configuration(mount_point=mount)['data']


def set_crl_configuration(
    ctx: Context,
    expiry: Annotated[str | None, 'The duration for which the generated CRL should be marked valid (e.g., "72h").'] = None,
    disable: Annotated[bool | None, 'If true, disables the CRL.'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """set the CRL configuration with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].set_crl_configuration(expiry=expiry, disable=disable, mount_point=mount)


async def read_urls(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """read the URL configuration (issuing_certificates, crl_distribution_points, ocsp_servers) with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_urls(mount_point=mount)['data']


def set_urls(
    ctx: Context,
    issuing_certificates: Annotated[list[str] | None, 'The URL values for the Issuing Certificate field.'] = None,
    crl_distribution_points: Annotated[list[str] | None, 'The URL values for the CRL Distribution Points field.'] = None,
    ocsp_servers: Annotated[list[str] | None, 'The URL values for the OCSP Servers field.'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """set the URL configuration with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].set_urls(
        issuing_certificates=issuing_certificates,
        crl_distribution_points=crl_distribution_points,
        ocsp_servers=ocsp_servers,
        mount_point=mount,
    )


def submit_ca_information(
    ctx: Context,
    pem_bundle: Annotated[str, 'The PEM bundle containing the CA certificate and private key.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """submit CA information (certificate and private key bundle) with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].submit_ca_information(pem_bundle=pem_bundle, mount_point=mount)


def create_update_role(
    ctx: Context,
    name: Annotated[str, 'The name of the role to create or update.'],
    extra_params: Annotated[dict, 'Extra parameters for the role.'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """create or update a role with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].create_or_update_role(name=name, extra_params=extra_params, mount_point=mount)['data']


async def list_roles(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> list[str]:
    """list current roles with the pki engine in vault"""
    try:
        return ctx.request_context.lifespan_context['pki'].list_roles(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


async def read_role(
    ctx: Context, name: Annotated[str, 'The name of the role to read.'], mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki'
) -> dict:
    """read a role with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_role(name=name, mount_point=mount)['data']


def delete_role(
    ctx: Context, name: Annotated[str, 'The name of the role to delete.'], mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki'
) -> dict:
    """delete a role with the pki engine in vault"""
    return {'success': ctx.request_context.lifespan_context['pki'].delete_role(name=name, mount_point=mount).ok}


async def read_issuer(
    ctx: Context,
    issuer_ref: Annotated[str, 'The reference ID of the issuer to read.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """read an issuer configuration by reference ID with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_issuer(issuer_ref=issuer_ref, mount_point=mount)


async def list_issuers(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> list[str]:
    """list all issuers in the pki mount with the pki engine in vault"""
    try:
        return ctx.request_context.lifespan_context['pki'].list_issuers(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def update_issuer(
    ctx: Context,
    issuer_ref: Annotated[str, 'The reference ID of the issuer to update.'],
    extra_params: Annotated[dict, 'Extra parameters for issuer update (issuer_name, leaf_not_after_behavior, etc.).'] = None,
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """update an issuer configuration with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].update_issuer(issuer_ref=issuer_ref, extra_params=extra_params, mount_point=mount)


def revoke_issuer(
    ctx: Context,
    issuer_ref: Annotated[str, 'The reference ID of the issuer to revoke.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """revoke an issuer with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].revoke_issuer(issuer_ref=issuer_ref, mount_point=mount)
