import pytest
from models.fungeble.element import Element
from models.nonfungeble.game import Game
from models.nonfungeble.user import User

import config
from services.utils import load_from_txt
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestGameInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = Game

    @pytest.fixture(scope="module")
    def element_cls(self):
        filepath = config.get_element_content_path()
        load_from_txt(filepath)

        yield Element
        Element.reset_all()

    @pytest.fixture
    def saved_user(self):
        instance = User()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def saved_instance(self, element_cls, saved_user):
        filepath = config.get_element_content_path()
        load_from_txt(filepath)
        instance = self.model_cls(
            creator_user=saved_user,
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def not_saved_instance(self, element_cls, saved_user):
        filepath = config.get_element_content_path()
        load_from_txt(filepath)
        instance = self.model_cls(
            creator_user=saved_user,
        )

        yield instance
