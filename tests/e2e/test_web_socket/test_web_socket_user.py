import json

import pytest
import requests

import config
from app.app import Routes
from app.handlers.responses import Responses
from app.handlers.statements import Statements
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestWebSocketUser(BaseAPITest):
    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_get_user_success(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "statement": Statements.GET_USER,
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.GOT_USER
        assert message["instance"] == registered_user

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_change_user_success(self, registered_user, opened_connection):
        new_name = "new_name"

        await opened_connection.send(json.dumps({
            "statement": Statements.CHANGE_USER,
            "payload": {
                "fields": {"name": new_name}
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.CHANGED_USER
        assert message["instance"]["name"] == new_name

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_change_user_no_fields(self, registered_user, opened_connection):
        await opened_connection.send(json.dumps({
            "statement": Statements.CHANGE_USER
        }))
        message = json.loads(await opened_connection.recv())
        assert message == Responses.BAD_STATEMENT

    @pytest.mark.asyncio
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    async def test_change_user_password(self, registered_user, opened_connection):
        new_password = "password"

        await opened_connection.send(json.dumps({
            "statement": Statements.CHANGE_USER,
            "payload": {
                "fields": {"plain_password": new_password}
            }
        }))
        message = json.loads(await opened_connection.recv())
        assert message["statement"] == Statements.CHANGED_USER

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": registered_user["uuid"],
             "password": new_password}
        )
        assert response.status_code == 200


