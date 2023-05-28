from io import BytesIO

import pytest
import requests
from PIL import Image

import config
from tests import conftest
from tests.e2e.base_api_test import BaseAPITest


class TestResourcesAPITest(BaseAPITest):
    @pytest.mark.timeout(conftest.TIMEOUT)
    @pytest.mark.usefixtures("app")
    def test_media_is_reachable(self, entered_game):
        unlocked_elements = entered_game["unlocked_elements"]
        response = requests.get(unlocked_elements[0]["image"])
        assert response.status_code == 200
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        assert image.format.lower() == config.IMAGE_FORMAT.lower()
