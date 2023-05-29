import pytest
import requests

import config
from app.app import Routes
from tests.e2e.base_api_test import BaseAPITest


class TestRegistration(BaseAPITest):
    @pytest.mark.usefixtures("app")
    def test_registration_success(self):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": "password"}
        )
        assert response.status_code == 200
        assert response.json()["instance"]["type"] == "user"

    @pytest.mark.usefixtures("app")
    def test_registration_with_name_success(self):
        name = "test name"

        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {
                "name": name,
                "password": "password"
             }
        )
        assert response.status_code == 200
        assert response.json()["instance"]["name"] == name

    @pytest.mark.usefixtures("app")
    def test_registration_no_password(self):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
        )
        assert response.status_code == 400

    @pytest.mark.usefixtures("app")
    def test_registration_wrong_type(self):
        response = requests.post(
            f"{config.get_api_url()}{Routes.register}",
            {"password": 2}
        )
        assert response.status_code != 500
