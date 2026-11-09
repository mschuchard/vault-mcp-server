"""test mcp vault error translation middleware"""

from unittest.mock import AsyncMock

import hvac.exceptions as hvac_exc
import mcp.types
import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import MiddlewareContext
from fastmcp.tools import ToolResult

from vault_mcp_server.mcp_bindings import errors


@pytest.fixture
def middleware() -> errors.VaultErrorMiddleware:
    return errors.VaultErrorMiddleware()


@pytest.fixture
def context() -> MiddlewareContext[mcp.types.CallToolRequestParams]:
    return MiddlewareContext(message=mcp.types.CallToolRequestParams(name='audit-device-enable', arguments={}), method='tools/call')


def failing_call_next(cause: BaseException | None) -> AsyncMock:
    # fastmcp wraps an exception raised by a tool function in a tool error whose cause is the original exception
    wrapper: ToolError = ToolError("Error calling tool 'audit-device-enable'")
    wrapper.__cause__ = cause
    return AsyncMock(side_effect=wrapper)


@pytest.mark.asyncio
async def test_successful_call_returned_unchanged(middleware: errors.VaultErrorMiddleware, context: MiddlewareContext) -> None:
    expected_result: ToolResult = ToolResult(content='success')
    call_next: AsyncMock = AsyncMock(return_value=expected_result)

    assert await middleware.on_call_tool(context, call_next) is expected_result
    call_next.assert_awaited_once_with(context)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('cause', 'expected_error_code'),
    [
        (hvac_exc.Forbidden('permission denied'), 'permission_denied'),
        (hvac_exc.InvalidRequest('invalid request'), 'invalid_request'),
        (hvac_exc.InvalidPath('no handler for route'), 'invalid_path'),
        (hvac_exc.VaultDown('vault is sealed'), 'vault_sealed_or_down'),
        # every other hvac exception falls through to the generic error code
        (hvac_exc.Unauthorized('missing client token'), 'vault_error'),
        (hvac_exc.RateLimitExceeded('rate limit quota exceeded'), 'vault_error'),
        (hvac_exc.InternalServerError('internal error'), 'vault_error'),
        (hvac_exc.VaultNotInitialized('vault is not initialized'), 'vault_error'),
        (hvac_exc.UnexpectedError('unexpected status'), 'vault_error'),
        (hvac_exc.VaultError('generic error'), 'vault_error'),
    ],
)
async def test_vault_error_translated(
    middleware: errors.VaultErrorMiddleware, context: MiddlewareContext, cause: hvac_exc.VaultError, expected_error_code: str
) -> None:
    result: ToolResult = await middleware.on_call_tool(context, failing_call_next(cause))

    assert isinstance(result, ToolResult)
    assert result.is_error is True
    assert result.structured_content is not None
    assert result.structured_content['error_code'] == expected_error_code
    assert result.structured_content['hvac_exception'] == type(cause).__name__
    assert isinstance(result.content[0], mcp.types.TextContent)
    assert result.content[0].text == f'Vault error ({expected_error_code}): {cause}'


@pytest.mark.asyncio
async def test_vault_error_details_preserved(middleware: errors.VaultErrorMiddleware, context: MiddlewareContext) -> None:
    cause: hvac_exc.Forbidden = hvac_exc.Forbidden(errors=['1 error occurred:', 'permission denied'], method='PUT', url='http://vault:8200/v1/sys/audit/newdev')

    result: ToolResult = await middleware.on_call_tool(context, failing_call_next(cause))

    assert result.structured_content == {
        'error_code': 'permission_denied',
        'hvac_exception': 'Forbidden',
        'method': 'PUT',
        'url': 'http://vault:8200/v1/sys/audit/newdev',
        'errors': ['1 error occurred:', 'permission denied'],
        'message': str(cause),
    }


@pytest.mark.asyncio
@pytest.mark.parametrize('cause', [ValueError('not a vault error'), None])
async def test_non_vault_error_reraised(middleware: errors.VaultErrorMiddleware, context: MiddlewareContext, cause: BaseException | None) -> None:
    call_next: AsyncMock = failing_call_next(cause)

    # the original exception object propagates, rather than a translated tool result
    with pytest.raises(ToolError) as exc_info:
        await middleware.on_call_tool(context, call_next)
    assert exc_info.value is call_next.side_effect


@pytest.fixture
def server_under_test() -> FastMCP:
    server: FastMCP = FastMCP(name='errors-test')
    server.add_middleware(errors.VaultErrorMiddleware())

    @server.tool(name='audit-device-enable')
    def enable_audit_device() -> None:
        raise hvac_exc.Forbidden(errors=['permission denied'], method='PUT', url='http://vault:8200/v1/sys/audit/newdev')

    @server.tool(name='unexpected-failure')
    def fail_unexpectedly() -> None:
        raise ValueError('not a vault error')

    @server.tool(name='succeed')
    def succeed() -> str:
        return 'success'

    return server


@pytest.mark.asyncio
async def test_tool_vault_error_returned_as_structured_error(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        result = await client.call_tool(name='audit-device-enable', raise_on_error=False)

    assert result.is_error is True
    assert result.structured_content['error_code'] == 'permission_denied'
    assert result.structured_content['hvac_exception'] == 'Forbidden'
    assert result.structured_content['method'] == 'PUT'
    assert result.structured_content['url'] == 'http://vault:8200/v1/sys/audit/newdev'
    assert result.structured_content['errors'] == ['permission denied']
    assert result.content[0].text == f'Vault error (permission_denied): {result.structured_content["message"]}'


@pytest.mark.asyncio
async def test_tool_vault_error_raised_to_client(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        with pytest.raises(ToolError, match=r'Vault error \(permission_denied\): permission denied, on PUT http://vault:8200/v1/sys/audit/newdev'):
            await client.call_tool(name='audit-device-enable')


@pytest.mark.asyncio
async def test_tool_non_vault_error_not_translated(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        with pytest.raises(ToolError, match='not a vault error') as exc_info:
            await client.call_tool(name='unexpected-failure')

    assert 'Vault error' not in str(exc_info.value)


@pytest.mark.asyncio
async def test_tool_success_unaffected(server_under_test: FastMCP) -> None:
    async with Client(server_under_test) as client:
        result = await client.call_tool(name='succeed')

    assert result.is_error is False
    assert result.data == 'success'
