import json
from uuid import uuid4

import pytest
import pytest_asyncio

from app.handlers.allowed_commands import AllowedCommands
from models.nonfungeble.game import Game
from services.events.model_events import ModelListedEvent, InstanceNotExistEvent, ModelDeletedEvent, ModelGotEvent, \
    ModelCreatedEvent
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketGame(BaseAPITest):
    @pytest_asyncio.fixture
    async def created_game(self, opened_connection):
        name = "test game"
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        response = json.loads(await opened_connection.recv())
        return response["instance"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_created_success(self, opened_connection):
        name = "game name"
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelCreatedEvent.NAME
        assert response["instance"]["name"] == name
        assert response["instance"]["type"] == Game.NAME

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
    async def test_game_deleted_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps(
            {"message": AllowedCommands.DELETE_GAME,
             "payload": {
                 "uuid": created_game["uuid"]
             }}
        ))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelDeletedEvent.NAME
        assert response["instance"]["uuid"] == created_game["uuid"]

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
