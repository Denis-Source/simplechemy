import pytest
import websockets
from websockets.exceptions import ConnectionClosedError

import config
from app.app import Routes
from app.handlers.auth.jwt_utils import encode_jwt
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocket(BaseAPITest):
    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_success(self, opened_connection):
        assert not opened_connection.closed

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_success_two_connections(self, opened_connection, another_opened_connection):
        assert not opened_connection.closed
        assert not another_opened_connection.closed

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_second_connection_fail(self, access_header, opened_connection):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers=access_header) as websocket:
            with pytest.raises(ConnectionClosedError):
                await websocket.recv()

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_no_token(self):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      ) as websocket:
            with pytest.raises(ConnectionClosedError):
                await websocket.recv()

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_invalid_token(self, registered_user):
        invalid_token = encode_jwt(registered_user["uuid"], secret="invalid secret")
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers={"Authorization": f"bearer {invalid_token}"}
                                      ) as websocket:
            with pytest.raises(ConnectionClosedError):
                await websocket.recv()
