"""vault health"""

from typing import Annotated
from fastmcp import Context


async def read_status(
    ctx: Context,
    standby_ok: Annotated[bool | None, 'If true, a standby node returns a 200 status instead of the typical 429 status.'] = None,
    active_code: Annotated[int, 'The status code returned when the node is active.'] = 200,
    standby_code: Annotated[int, 'The status code returned when the node is a standby.'] = 429,
    dr_secondary_code: Annotated[int, 'The status code returned when the node is a DR secondary.'] = 472,
    performance_standby_code: Annotated[int, 'The status code returned when the node is a performance standby.'] = 473,
    sealed_code: Annotated[int, 'The status code returned when the node is sealed.'] = 503,
    uninit_code: Annotated[int, 'The status code returned when the node is uninitialized.'] = 501,
) -> dict:
    """read the health status of the vault server

    Returns fields such as initialized, sealed, standby, performance_standby,
    replication_performance_mode, replication_dr_mode, server_time_utc, version,
    cluster_name, and cluster_id. The *_code parameters control which HTTP status
    is treated as a non-error response for each server state, rather than raising.
    """
    return ctx.request_context.lifespan_context['sys'].read_health_status(
        method='GET',
        standby_ok=standby_ok,
        active_code=active_code,
        standby_code=standby_code,
        dr_secondary_code=dr_secondary_code,
        performance_standby_code=performance_standby_code,
        sealed_code=sealed_code,
        uninit_code=uninit_code,
    )
