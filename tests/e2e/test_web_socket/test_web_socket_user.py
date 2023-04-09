import json

import pytest
import requests

import config
from app.app import Routes
from app.handlers.responses import Responses
from app.handlers.allowed_commands import AllowedCommands
from services.events.model_events import ModelChangedEvent, ModelGotEvent
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketUser(BaseAPITest):
    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_get_user_success(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.GET_USER,
        }))
        response = json.loads(await opened_connection.recv())
        assert response["message"] == ModelGotEvent.NAME
        assert response["instance"] == registered_user

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_change_user_success(self, registered_user, opened_connection):
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
    async def test_change_user_no_fields(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "message": AllowedCommands.CHANGE_USER
        }))
        response = json.loads(await opened_connection.recv())
        assert response == Responses.BAD_REQUEST

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_change_user_password(self, registered_user, opened_connection):
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
