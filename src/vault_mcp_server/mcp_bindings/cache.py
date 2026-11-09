"""namespace aware response caching middleware"""

from typing import Any

import mcp.types
from fastmcp.resources import ResourceResult
from fastmcp.server.middleware import CallNext, MiddlewareContext
from fastmcp.server.middleware.caching import ReadResourceSettings, ResponseCachingMiddleware
from fastmcp.tools import ToolResult


class VaultResponseCachingMiddleware(ResponseCachingMiddleware):
    """Response caching whose resource read cache is partitioned by active vault namespace and discarded after every tool call.

    The stock resource read cache key is derived from the resource uri alone. Consequently, a namespace switch would serve the
    previous namespace's data, and a tool call that mutates vault would serve pre-mutation data until the ttl expires. Only changes
    made outside of this server remain subject to the ttl. All other cached responses (e.g. tool and resource lists) behave as usual.
    """

    def __init__(self, read_resource_settings: ReadResourceSettings | None = None, **kwargs: Any) -> None:
        # the inherited resource read cache is disabled because resource reads are cached by the per namespace caches instead
        super().__init__(read_resource_settings={'enabled': False}, **kwargs)
        self._namespace_read_settings: ReadResourceSettings | None = read_resource_settings
        self._namespace_read_caches: dict[str | None, ResponseCachingMiddleware] = {}

    async def on_read_resource(
        self,
        context: MiddlewareContext[mcp.types.ReadResourceRequestParams],
        call_next: CallNext[mcp.types.ReadResourceRequestParams, ResourceResult],
    ) -> ResourceResult:
        request_context = context.fastmcp_context.request_context if context.fastmcp_context is not None else None
        # without a request context the active namespace is unknown, so the read cannot be cached safely
        if request_context is None:
            return await call_next(context)
        # the active namespace is state on the shared hvac adapter, which the namespace switch tool mutates in place
        namespace: str | None = request_context.lifespan_context['client'].adapter.namespace
        # a read that already holds a cache keeps writing to that cache even after it is discarded, so it cannot repopulate the new ones
        if namespace not in self._namespace_read_caches:
            self._namespace_read_caches[namespace] = ResponseCachingMiddleware(read_resource_settings=self._namespace_read_settings)
        return await self._namespace_read_caches[namespace].on_read_resource(context, call_next)

    async def on_call_tool(
        self,
        context: MiddlewareContext[mcp.types.CallToolRequestParams],
        call_next: CallNext[mcp.types.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        try:
            return await super().on_call_tool(context, call_next)
        finally:
            # a tool call, including one that failed part way, may have changed vault state or the active namespace
            self._namespace_read_caches.clear()
