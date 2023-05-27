import json

import pytest
import pytest_asyncio
import requests
import websockets

import config
from app.app import Routes
from app.handlers.allowed_commands import AllowedCommands


class BaseAPITest:
    @pytest.fixture(scope="session")
    def mock_password(self):
        return "password"

    @pytest.fixture(scope="session")
    def registered_user(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": "password"}
        )
        assert response.status_code == 200
        return response.json()["instance"]

    @pytest.fixture(scope="session")
    def another_registered_user(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": "password"}
        )
        assert response.status_code == 200
        return response.json()["instance"]

    @pytest.fixture(scope="session")
    def access_token(self, registered_user, mock_password):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": mock_password}
        )

        return response.json().get("token")

    @pytest.fixture(scope="session")
    def another_access_token(self, another_registered_user, mock_password):
        user_uuid = another_registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": mock_password}
        )

        return response.json().get("token")

    @pytest.fixture(scope="session")
    def access_header(self, access_token):
        return {"Authorization": f"bearer {access_token}"}

    @pytest.fixture(scope="session")
    def another_access_header(self, another_access_token):
        return {"Authorization": f"bearer {another_access_token}"}

    @pytest_asyncio.fixture
    async def opened_connection(self, access_header):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers=access_header) as websocket:
            await websocket.recv()
            yield websocket

            await websocket.close()

    @pytest_asyncio.fixture
    async def another_opened_connection(self, another_access_header):
        async with websockets.connect(f"{config.get_api_url(False)}{Routes.ws}",
                                      extra_headers=another_access_header) as websocket:
            await websocket.recv()
            yield websocket

            await websocket.close()

    @pytest_asyncio.fixture
    async def created_game(self, opened_connection, another_opened_connection):
        name = "test game"
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        response = json.loads(await opened_connection.recv())
        await another_opened_connection.recv()

        return response["instance"]

    @pytest_asyncio.fixture()
    async def entered_game(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ENTER_GAME,
            "payload": {
                "game_uuid": created_game["uuid"]
            }}
        ))

        response = json.loads(await opened_connection.recv())
        return response["game"]

    @pytest_asyncio.fixture()
    async def entered_game_by_two(self, opened_connection, another_opened_connection, entered_game):
        await another_opened_connection.send(json.dumps({
            "message": AllowedCommands.ENTER_GAME,
            "payload": {
                "game_uuid": entered_game["uuid"]
            }}
        ))
        await another_opened_connection.recv()
        await another_opened_connection.recv()
        response = json.loads(await opened_connection.recv())
        return response["game"]
