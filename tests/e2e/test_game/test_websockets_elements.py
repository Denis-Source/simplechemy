import json

import pytest
import pytest_asyncio

from app.handlers.allowed_commands import AllowedCommands
from services.events.game_events import GameAddedElementPEvent, GameElementNotExistEvent, GameMovedElementPEvent, \
    GameNewElementPCraftedEvent
from services.events.user_events import UserNotInGameEvent
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketGame(BaseAPITest):
    @pytest_asyncio.fixture()
    async def added_element_p(self, opened_connection, entered_game_by_two, another_opened_connection):
        element_name = entered_game_by_two["unlocked_elements"][0]

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        response = json.loads(await opened_connection.recv())
        await another_opened_connection.recv()
        return response["element_p"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_element_p_added_success(self, opened_connection, entered_game_by_two, another_opened_connection):
        element_name = entered_game_by_two["unlocked_elements"][0]

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == GameAddedElementPEvent.NAME
        assert response["element_p"]["element"]["name"] == element_name

        another_response = json.loads(await another_opened_connection.recv())
        assert another_response["message"] == GameAddedElementPEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_element_p_added_not_in_game(self, opened_connection, created_game):
        element_name = created_game["unlocked_elements"][0]
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == UserNotInGameEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_element_p_not_exist(self, opened_connection, entered_game):
        element_name = "Non Existent Element"

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == GameElementNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_element_p_not_unlocked(self, opened_connection, entered_game):
        # TODO hardcoded element name
        element_name = "Cloud"

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == GameElementNotExistEvent.NAME

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_move_element_p_success(self, opened_connection, another_opened_connection, entered_game_by_two,
                                          added_element_p):
        new_x = 0.3
        new_y = 0.4

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.MOVE_ELEMENT_P,
            "payload": {
                "element_p": added_element_p["uuid"],
                "x": new_x,
                "y": new_y,
                "is_done": True,
            }
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == GameMovedElementPEvent.NAME
        assert response["element_p"]["x"] == new_x
        assert response["element_p"]["y"] == new_y

        another_response = json.loads(await another_opened_connection.recv())
        assert another_response["message"] == GameMovedElementPEvent.NAME

    # TODO add failure test for the element p movement

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_crafted_element_p_success(self, opened_connection, another_opened_connection, entered_game_by_two):
        # TODO hardcoded elements names
        element_name = "Air"
        another_element_name = "Water"

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": element_name,
                "x": 0,
                "y": 0
            }
        }))
        # responses for the first element creation
        element_p = json.loads(await opened_connection.recv())["element_p"]
        await another_opened_connection.recv()

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.ADD_ELEMENT_P,
            "payload": {
                "element": another_element_name,
                "x": 0,
                "y": 0
            }
        }))

        # responses for the second element creation
        another_element_p = json.loads(await opened_connection.recv())["element_p"]
        await another_opened_connection.recv()

        new_x = 0.3
        new_y = 0.4
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.MOVE_ELEMENT_P,
            "payload": {
                "element_p": element_p["uuid"],
                "x": new_x,
                "y": new_y,
                "is_done": True,
            }
        }))
        # responses for the first movement (no new elements)
        await opened_connection.recv()
        await another_opened_connection.recv()

        await opened_connection.send(json.dumps({
            "message": AllowedCommands.MOVE_ELEMENT_P,
            "payload": {
                "element_p": another_element_p["uuid"],
                "x": new_x,
                "y": new_y,
                "is_done": True,
            }
        }))
        # responses for the second movement (new element crafted)
        response = json.loads(await opened_connection.recv())
        assert response["message"] == GameNewElementPCraftedEvent.NAME

        assert len(response["used_elements_p"]) == 2

        another_response = json.loads(await another_opened_connection.recv())
        assert another_response["message"] == GameNewElementPCraftedEvent.NAME
        # TODO add failure test for element p movement
