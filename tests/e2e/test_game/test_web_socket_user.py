import json
from uuid import uuid4

import pytest
import requests
from websockets.exceptions import ConnectionClosedError

import config
from app.app import Routes
from app.handlers.allowed_commands import AllowedCommands
from app.handlers.responses import Responses
from services.events.model_events import ModelChangedEvent, ModelGotEvent, InstanceNotExistEvent
from services.events.user_events import UserEnteredGameEvent, UserAlreadyInGameEvent
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketUser(BaseAPITest):
    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_got_user_success(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.GET_USER,
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelGotEvent.NAME
        assert response["instance"] == registered_user

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_changed_user_success(self, registered_user, opened_connection):
        new_name = "new_name"

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CHANGE_USER,
            "payload": {
                "fields": {"name": new_name}
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelChangedEvent.NAME
        assert response["instance"]["name"] == new_name

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_changed_user_no_fields(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CHANGE_USER
        }))
        with pytest.raises(ConnectionClosedError):
            await opened_connection.recv()

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_changed_user_password(self, registered_user, opened_connection):
        new_password = "password"

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CHANGE_USER,
            "payload": {
                "fields": {"plain_password": new_password}
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelChangedEvent.NAME

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": registered_user["uuid"],
             "password": new_password}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_user_entered_game_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ENTER_GAME,
            "payload": {
                "game_uuid": created_game["uuid"]
            }}
        ))

        response = json.loads(await opened_connection.recv())
        assert response["message"] == UserEnteredGameEvent.NAME
        assert response["instance"]["game_uuid"] == created_game["uuid"]
        assert response["game"]["uuid"] == created_game["uuid"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_user_entered_game_not_exist(self, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ENTER_GAME,
            "payload": {
                "game_uuid": str(uuid4())
            }}
        ))

        response = json.loads(await opened_connection.recv())
        assert response["message"] == InstanceNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_user_entered_game_already_in_game(self, opened_connection, entered_game):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ENTER_GAME,
            "payload": {
                "game_uuid": entered_game["uuid"]
            }}
        ))

        response = json.loads(await opened_connection.recv())
        assert response["message"] == UserAlreadyInGameEvent.NAME
