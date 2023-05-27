import pytest
import requests

import config
from app.app import Routes
from app.handlers.auth.jwt_utils import decode_jwt
from tests.e2e.base_api_test import BaseAPITest


class TestLogin(BaseAPITest):
    @pytest.mark.usefixtures("app")
    def test_login_success(self, registered_user, mock_password):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": mock_password}
        )

        assert response.status_code == 200
        token = response.json().get("token")
        decoded = decode_jwt(token)

        assert decoded.get("sub") == response.json().get("instance").get("uuid")

    @pytest.mark.usefixtures("app")
    def test_login_invalid_user_uuid(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": "invalid_uuid",
             "password": mock_password}
        )

        assert response.status_code == 404

    @pytest.mark.usefixtures("app")
    def test_login_missing_password(self, registered_user):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid}
        )

        assert response.status_code == 400

    @pytest.mark.usefixtures("app")
    def test_login_missing_user_uuid(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"password": mock_password}
        )

        assert response.status_code == 400

    @pytest.mark.usefixtures("app")
    def test_login_invalid_password(self, registered_user):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": "invalid_password"}
        )

        assert response.status_code == 401
