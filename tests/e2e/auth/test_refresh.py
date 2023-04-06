import time

import pytest
import requests

import config
from app.app import Routes
from app.handlers.auth.jwt_utils import decode_jwt
from tests.e2e.base_api_test import BaseAPITest


class TestRefresh(BaseAPITest):
    @pytest.fixture
    def mock_password(self):
        return "password"

    @pytest.fixture
    def registered_user(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": "password"}
        )
        assert response.status_code == 200
        return response.json()["instance"]

    @pytest.fixture
    def logged_response(self, mock_password, registered_user):
        user_uuid = registered_user["uuid"]

        response = requests.post(
            f"{config.get_api_url()}{Routes.login}",
            {"user_uuid": user_uuid,
             "password": mock_password}
        )

        return response

    @pytest.mark.usefixtures("app")
    def test_refresh_success(self, registered_user, logged_response):
        old_token = logged_response.json().get("token")

        time.sleep(2)

        response = requests.post(
            f"{config.get_api_url()}{Routes.refresh}",
            headers={"Authorization": f"Bearer {old_token}"}
        )
        assert response.status_code == 200
        token = response.json().get("token")

        assert token != old_token
        decoded_old = decode_jwt(old_token)
        decoded = decode_jwt(token)
        assert decoded.get("iat") != decoded_old.get("iat")
        assert decoded.get("sub") == decoded_old.get("sub")

    @pytest.mark.usefixtures("app")
    def test_refresh_invalid_token_type(self, registered_user, logged_response):
        old_token = logged_response.json().get("token")

        response = requests.post(
            f"{config.get_api_url()}{Routes.refresh}",
            headers={"Authorization": f"Basic {old_token}"}
        )
        assert response.status_code == 401

    @pytest.mark.usefixtures("app")
    def test_refresh_invalid_token(self):
        response = requests.post(
            f"{config.get_api_url()}{Routes.refresh}",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    @pytest.mark.usefixtures("app")
    def test_refresh_no_auth_header(self, registered_user, logged_response):
        response = requests.post(
            f"{config.get_api_url()}{Routes.refresh}"
        )
        assert response.status_code == 401
