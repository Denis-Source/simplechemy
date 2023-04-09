import json
from uuid import uuid4

import pytest

from app.handlers.allowed_commands import AllowedCommands
from models.nonfungeble.game import Game
from services.events.model_events import ModelListedEvent, InstanceNotExistEvent, ModelDeletedEvent, ModelGotEvent, \
    ModelCreatedEvent
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketGame(BaseAPITest):
    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_created_success(self, opened_connection, another_opened_connection):
        name = "game name"
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        response1 = json.loads(await opened_connection.recv())
        response2 = json.loads(await another_opened_connection.recv())

        assert response1 == response2

        assert response1["message"] == ModelCreatedEvent.NAME
        assert response1["instance"]["name"] == name
        assert response1["instance"]["type"] == Game.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_created_default_name(self, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CREATE_GAME,
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelCreatedEvent.NAME
        assert response["instance"]["name"]
        assert response["instance"]["type"] == Game.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_got_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.GET_GAME,
            "payload": {
                "uuid": created_game["uuid"]
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelGotEvent.NAME
        assert response["instance"] == created_game

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_got_not_exist(self, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.GET_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == InstanceNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_deleted_success(self, opened_connection, another_opened_connection, created_game):
        await opened_connection.send(json.dumps(
            {"message": AllowedCommands.DELETE_GAME,
             "payload": {
                 "uuid": created_game["uuid"]
             }}
        ))

        response1 = json.loads(await opened_connection.recv())
        response2 = json.loads(await another_opened_connection.recv())

        assert response1 == response2
        assert response1["message"] == ModelDeletedEvent.NAME
        assert response1["instance"]["uuid"] == created_game["uuid"]

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.GET_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        response1 = json.loads(await opened_connection.recv())

        assert response1["message"] == InstanceNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_deleted_not_exist(self, opened_connection):
        await opened_connection.send(json.dumps(
            {"message": AllowedCommands.DELETE_GAME,
             "payload": {
                 "uuid": str(uuid4())
             }}
        ))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == InstanceNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_listed_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.LIST_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelListedEvent.NAME
        assert created_game in response["instances"]
