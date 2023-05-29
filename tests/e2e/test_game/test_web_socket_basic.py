import json

import pytest
import websockets
from websockets.exceptions import ConnectionClosedError

import config
from app.handlers.allowed_commands import AllowedCommands
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
        # assert not another_opened_connection.closed

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_second_connection_fail(self, ws_authentication_message, opened_connection):
        async with websockets.connect(config.get_api_url(False)) as websocket:
            await websocket.recv()
            with pytest.raises(ConnectionClosedError):
                await websocket.send(ws_authentication_message)
                await websocket.recv()

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_no_token(self):
        async with websockets.connect(config.get_api_url(False)) as websocket:
            await websocket.recv()
            with pytest.raises(ConnectionClosedError):
                await websocket.send(json.dumps({
                    "message": AllowedCommands.GET_USER,
                }))
                await websocket.recv()

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_opened_invalid_token(self, registered_user):
        invalid_token = encode_jwt(registered_user["uuid"], secret="invalid secret")
        async with websockets.connect(config.get_api_url(False)) as websocket:
            await websocket.recv()
            with pytest.raises(ConnectionClosedError):
                await websocket.send(json.dumps({
                    "message": "authorization",
                    "payload": {
                        "token": invalid_token
                    }
                }))
                await websocket.recv()
