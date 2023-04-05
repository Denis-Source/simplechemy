import pytest
import requests

import config
from app.app import Routes
from tests.e2e.base_api_test import BaseAPITest


class TestAuth(BaseAPITest):
    @pytest.fixture
    def mock_password(self):
        return "password"

    @pytest.mark.usefixtures("app")
    @pytest.fixture
    def registered_user_response(self, mock_password):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": mock_password}
        )

        yield response

    @pytest.mark.usefixtures("app")
    def test_registration_success(self, registered_user_response):
        assert registered_user_response.status_code == 200
        assert registered_user_response.json()["instance"]["type"] == "user"

    @pytest.mark.usefixtures("app")
    def test_registration_no_password(self, app):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
        )
        assert response.status_code == 400
