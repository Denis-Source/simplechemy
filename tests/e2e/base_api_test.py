import pytest
import requests

import config
from app.app import Routes


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
    def access_token(self, registered_user, mock_password):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": mock_password}
        )

        return response.json().get("token")

    @pytest.fixture(scope="session")
    def access_header(self, access_token):
        return {"Authorization": f"bearer {access_token}"}