import json
from uuid import uuid4

import pytest
import pytest_asyncio

from app.handlers.statements import Statements
from models.nonfungeble.game import Game
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketGame(BaseAPITest):
    @pytest_asyncio.fixture
    async def created_game(self, opened_connection):
        name = "test game"
        await opened_connection.send(json.dumps({
            "statement": Statements.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        message = json.loads(await opened_connection.recv())
        return message["instance"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_created_success(self, opened_connection):
        name = "game name"
        await opened_connection.send(json.dumps({
            "statement": Statements.CREATE_GAME,
            "payload": {
                "fields": {"name": name}
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.CREATED_GAME
        assert message["instance"]["name"] == name
        assert message["instance"]["type"] == Game.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_created_default_name(self, opened_connection):
        await opened_connection.send(json.dumps({
            "statement": Statements.CREATE_GAME,
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.CREATED_GAME
        assert message["instance"]["name"]
        assert message["instance"]["type"] == Game.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_got_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "statement": Statements.GET_GAME,
            "payload": {
                "uuid": created_game["uuid"]
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.GOT_GAME
        assert message["instance"] == created_game

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_got_not_exist(self, opened_connection):
        await opened_connection.send(json.dumps({
            "statement": Statements.GET_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.NOT_EXIST

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_deleted_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps(
            {"statement": Statements.DELETE_GAME,
             "payload": {
                 "uuid": created_game["uuid"]
             }}
        ))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.DELETED_GAME
        assert message["instance"]["uuid"] == created_game["uuid"]

        await opened_connection.send(json.dumps({
            "statement": Statements.GET_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.NOT_EXIST

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_deleted_not_exist(self, opened_connection):
        await opened_connection.send(json.dumps(
            {"statement": Statements.DELETE_GAME,
             "payload": {
                 "uuid": str(uuid4())
             }}
        ))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.NOT_EXIST

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_game_listed_success(self, opened_connection, created_game):
        await opened_connection.send(json.dumps({
            "statement": Statements.LIST_GAME,
            "payload": {
                "uuid": str(uuid4)
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.LISTED_GAME
        assert created_game in message["instances"]
