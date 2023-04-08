import json
import time

import pytest
import websockets
from websockets.exceptions import ConnectionClosedError

import config
from app.app import Routes
from app.handlers.auth.jwt_utils import encode_jwt
from app.handlers.responses import Responses
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocket(BaseAPITest):
    @pytest.mark.asyncio
    async def test_opened_success(self, access_header):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers=access_header) as websocket:
            message = await websocket.recv()
            assert json.loads(message) == Responses.WS_OPENED

    @pytest.mark.asyncio
    async def test_opened_no_token(self):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      ) as websocket:
            with pytest.raises(ConnectionClosedError):
                message = await websocket.recv()

    @pytest.mark.asyncio
    async def test_opened_invalid_token(self, registered_user):
        invalid_token = encode_jwt(registered_user["uuid"], secret="invalid secret")
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers={"Authorization": f"bearer {invalid_token}"}
                                      ) as websocket:
            with pytest.raises(ConnectionClosedError):
                message = await websocket.recv()
