"""hvac to mcp error translation middleware"""

import hvac.exceptions as hvac_exc
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools import ToolResult


class VaultErrorMiddleware(Middleware):
    """Restructure an hvac exception into a structured tool error.

    Preserves the original hvac error type/status/message rather than
    discarding them, so the caller still has enough to act on.
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next) -> ToolResult:
        try:
            return await call_next(context)
        except Exception as exc:
            cause: BaseException | None = exc.__cause__
            if not isinstance(cause, hvac_exc.VaultError):
                raise
            match cause:
                case hvac_exc.Forbidden():
                    code = 'permission_denied'
                case hvac_exc.InvalidRequest():
                    code = 'invalid_request'
                case hvac_exc.InvalidPath():
                    code = 'invalid_path'
                case hvac_exc.VaultDown():
                    code = 'vault_sealed_or_down'
                case _:
                    code = 'vault_error'
            return ToolResult(
                content=[{'type': 'text', 'text': f'Vault error ({code}): {cause}'}],
                is_error=True,
                structured_content={
                    'error_code': code,
                    'hvac_exception': type(cause).__name__,
                    'status_code': getattr(cause, 'status_code', None),
                    'errors': getattr(cause, 'errors', None),
                    'message': str(cause),
                },
            )
