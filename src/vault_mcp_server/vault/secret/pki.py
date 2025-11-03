"""vault pki"""

from typing import Annotated, Literal

from fastmcp import Context
import hvac.exceptions


def generate_root(
    ctx: Context,
    type: Annotated[Literal['exported', 'internal', 'kms'], 'The type of key to generate for the root CA.'],
    common_name: Annotated[str, 'The requested common name for the root CA certificate.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate a root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_root(type=type, common_name=common_name, mount_point=mount)['data']


def delete_root(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> dict:
    """delete the current root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].delete_root(mount_point=mount)


async def read_root_certificate(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> str:
    """read the current root ca certificate in raw DER-encoded format with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate(mount_point=mount)


async def read_root_certificate_chain(ctx: Context, mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki') -> str:
    """read the current root ca certificate chain in PEM format with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate_chain(mount_point=mount)


def generate_intermediate(
    ctx: Context,
    type: Annotated[Literal['exported', 'internal', 'kms'], 'The type of key to generate for the intermediate CA.'],
    common_name: Annotated[str, 'The requested common name for the intermediate CA certificate.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate an intermediate certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_intermediate(type=type, common_name=common_name, mount_point=mount)['data']


def sign_intermediate_certificate(
    ctx: Context,
    csr: Annotated[str, 'The PEM-encoded CSR (Certificate Signing Request) to sign.'],
    common_name: Annotated[str, 'The requested common name for the intermediate certificate.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """sign an intermediate ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_intermediate(csr=csr, common_name=common_name, mount_point=mount)['data']


def generate_certificate(
    ctx: Context,
    role: Annotated[str, 'The name of the role to create the certificate against.'],
    common_name: Annotated[str, 'The requested common name for the certificate.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """generate a private key and certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_certificate(name=role, common_name=common_name, mount_point=mount)['data']


def sign_certificate(
    ctx: Context,
    role: Annotated[str, 'The name of the role to sign the certificate.'],
    csr: Annotated[str, 'The PEM-encoded CSR (Certificate Signing Request) to sign.'],
    common_name: Annotated[str, 'The requested common name for the certificate.'],
    mount: Annotated[str, 'The "path" the method/backend was mounted on.'] = 'pki',
) -> dict:
    """sign a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_certificate(name=role, csr=csr, common_name=common_name, mount_point=mount)['data']


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


def create_update_role(
    ctx: Context,
    name: Annotated[str, 'The name of the role to create or update.'],
    extra_params: Annotated[dict, 'Extra parameters for the role.'] = {},
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
