"""vault pki"""

from fastmcp import Context
import hvac.exceptions


def generate_root(ctx: Context, type: str, common_name: str, mount: str = 'pki') -> dict:
    """generate a root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_root(type=type, common_name=common_name, mount_point=mount)['data']


def delete_root(ctx: Context, mount: str = 'pki') -> dict:
    """delete the current root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].delete_root(mount_point=mount)


async def read_root_certificate(ctx: Context, mount: str = 'pki') -> str:
    """read the current root ca certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate(mount_point=mount)


async def read_root_certificate_chain(ctx: Context, mount: str = 'pki') -> str:
    """read the current root ca certificate chain with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_ca_certificate_chain(mount_point=mount)


def generate_intermediate(ctx: Context, type: str, common_name: str, mount: str = 'pki') -> dict:
    """generate an intermediate certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_intermediate(type=type, common_name=common_name, mount_point=mount)['data']


def sign_intermediate_certificate(ctx: Context, csr: str, common_name: str, mount: str = 'pki') -> dict:
    """sign an intermediate certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_intermediate(csr=csr, common_name=common_name, mount_point=mount)['data']


def generate_certificate(ctx: Context, role: str, common_name: str, mount: str = 'pki') -> dict:
    """generate a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].generate_certificate(name=role, common_name=common_name, mount_point=mount)['data']


def sign_certificate(ctx: Context, role: str, csr: str, common_name: str, mount: str = 'pki') -> dict:
    """sign a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].sign_certificate(name=role, csr=csr, common_name=common_name, mount_point=mount)['data']


async def read_certificate(ctx: Context, serial: str, mount: str = 'pki') -> dict:
    """read a certificate by serial number with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_certificate(serial=serial, mount_point=mount)


async def list_certificates(ctx: Context, mount: str = 'pki') -> list[str]:
    """list current certificates with the pki engine in vault"""
    try:
        return ctx.request_context.lifespan_context['pki'].list_certificates(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidRequest:
        return []


def revoke_certificate(ctx: Context, serial_number: str, mount: str = 'pki') -> dict:
    """revoke a certificate with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].revoke_certificate(serial_number=serial_number, mount_point=mount)['data']


def tidy_certificates(ctx: Context, mount: str = 'pki') -> dict:
    """cleanup expired certificates with the pki engine in vault"""
    return {'success': ctx.request_context.lifespan_context['pki'].tidy(mount_point=mount).ok}


def create_update_role(ctx: Context, name: str, extra_params: dict = {}, mount: str = 'pki') -> dict:
    """create or update a role with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].create_or_update_role(name=name, extra_params=extra_params, mount_point=mount)['data']


async def list_roles(ctx: Context, mount: str = 'pki') -> list[str]:
    """list current roles with the pki engine in vault"""
    try:
        return ctx.request_context.lifespan_context['pki'].list_roles(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


async def read_role(ctx: Context, name: str, mount: str = 'pki') -> dict:
    """read a role with the pki engine in vault"""
    return ctx.request_context.lifespan_context['pki'].read_role(name=name, mount_point=mount)['data']


def delete_role(ctx: Context, name: str, mount: str = 'pki') -> dict:
    """delete a role with the pki engine in vault"""
    return {'success': ctx.request_context.lifespan_context['pki'].delete_role(name=name, mount_point=mount).ok}
