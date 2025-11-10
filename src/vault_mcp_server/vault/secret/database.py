"""vault database"""

from typing import Annotated

from fastmcp import Context
import hvac.exceptions


async def read_connection(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the connection to read.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """read the configuration settings for a database connection in vault"""
    return ctx.request_context.lifespan_context['database'].read_connection(name=name, mount_point=mount)['data']


async def list_connections(
    ctx: Context,
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> list[str]:
    """list database connections in vault"""
    try:
        return ctx.request_context.lifespan_context['database'].list_connections(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete_connection(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the connection to delete.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """delete a database connection from vault"""
    return {'success': ctx.request_context.lifespan_context['database'].delete_connection(name=name, mount_point=mount).ok}


def reset_connection(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the connection to reset.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """close a database connection and its underlying plugin and restart it with the configuration stored in vault"""
    return {'success': ctx.request_context.lifespan_context['database'].reset_connection(name=name, mount_point=mount).ok}


def rotate_root_credentials(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the connection to rotate root credentials for.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """rotate the root superuser credentials stored for a database connection in vault"""
    return {'success': ctx.request_context.lifespan_context['database'].rotate_root_credentials(name=name, mount_point=mount).ok}


def create_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the role to create.'],
    db_name: Annotated[str, 'The name of the database connection to use for this role.'],
    creation_statements: Annotated[list[str], 'Specifies the database statements executed to create and configure a user.'],
    default_ttl: Annotated[
        str | None, 'Specifies the TTL for the leases associated with this role. Accepts time suffixed strings (1h) or an integer number of seconds.'
    ] = None,
    max_ttl: Annotated[
        str | None, 'Specifies the maximum TTL for the leases associated with this role. Accepts time suffixed strings (1h) or an integer number of seconds.'
    ] = None,
    revocation_statements: Annotated[list[str] | None, 'Specifies the database statements to be executed to revoke a user.'] = None,
    rollback_statements: Annotated[
        list[str] | None, 'Specifies the database statements to be executed to rollback a create operation in the event of an error.'
    ] = None,
    renew_statements: Annotated[list[str] | None, 'Specifies the database statements to be executed to renew a user.'] = None,
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """create or update a dynamic role definition with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].create_role(
        name=name,
        db_name=db_name,
        creation_statements=creation_statements,
        default_ttl=default_ttl,
        max_ttl=max_ttl,
        revocation_statements=revocation_statements,
        rollback_statements=rollback_statements,
        renew_statements=renew_statements,
        mount_point=mount,
    )


async def read_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the role to read.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """read a dynamic role definition with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].read_role(name=name, mount_point=mount)['data']


async def list_roles(
    ctx: Context,
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> list[str]:
    """list dynamic roles with the database engine in vault"""
    try:
        return ctx.request_context.lifespan_context['database'].list_roles(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the role to delete.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """delete a dynamic role definition with the database engine in vault"""
    return {'success': ctx.request_context.lifespan_context['database'].delete_role(name=name, mount_point=mount).ok}


def generate_credentials(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the role to create credentials against.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """generate dynamic database credentials based on a role with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].generate_credentials(name=name, mount_point=mount)['data']


def create_static_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the static role to create.'],
    db_name: Annotated[str, 'The name of the database connection to use for this role.'],
    username: Annotated[str, 'Specifies the database username that this Vault role corresponds to.'],
    rotation_statements: Annotated[list[str], 'Specifies the database statements to be executed to rotate the password for the configured database user.'],
    rotation_period: Annotated[
        int, 'Specifies the amount of time Vault should wait before rotating the password, in seconds. The minimum is 5 seconds.'
    ] = 86400,
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """create or update a static role definition with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].create_static_role(
        name=name,
        db_name=db_name,
        username=username,
        rotation_statements=rotation_statements,
        rotation_period=rotation_period,
        mount_point=mount,
    )


async def read_static_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the static role to read.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """read a static role definition with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].read_static_role(name=name, mount_point=mount)['data']


async def list_static_roles(
    ctx: Context,
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> list[str]:
    """list static roles with the database engine in vault"""
    try:
        return ctx.request_context.lifespan_context['database'].list_static_roles(mount_point=mount)['data'].get('keys', [])
    except hvac.exceptions.InvalidPath:
        return []


def delete_static_role(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the static role to delete.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """delete a static role definition with the database engine in vault"""
    return {'success': ctx.request_context.lifespan_context['database'].delete_static_role(name=name, mount_point=mount).ok}


def get_static_credentials(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the static role to get credentials for.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict:
    """retrieve the current credentials for a static role with the database engine in vault"""
    return ctx.request_context.lifespan_context['database'].get_static_credentials(name=name, mount_point=mount)['data']


def rotate_static_role_credentials(
    ctx: Context,
    name: Annotated[str, 'Specifies the name of the static role to rotate credentials for.'],
    mount: Annotated[str, 'The "path" the database engine was mounted on.'] = 'database',
) -> dict[str, bool]:
    """manually trigger rotation of credentials for a static role with the database engine in vault"""
    return {'success': ctx.request_context.lifespan_context['database'].rotate_static_role_credentials(name=name, mount_point=mount).ok}
