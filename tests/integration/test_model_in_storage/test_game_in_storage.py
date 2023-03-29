import pytest

import config
from models.element import Element
from models.game import Game
from models.user import User
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.test_entity_in_storage import TestEntityInMemoryStorage


class TestGameInMemoryStorage(TestEntityInMemoryStorage):
    storage = MemoryStorage()
    model_cls = Game

    @pytest.fixture
    def element_cls(self):
        filepath = config.get_element_content_path()
        Element.load_from_txt(filepath)

        yield Element
        Element.reset_all()

    @pytest.fixture
    def saved_user(self):
        instance = User(
            storage=self.storage
        )
        yield instance
        instance.delete()

    @pytest.fixture
    def saved_instance(self, element_cls, saved_user):
        instance = self.model_cls(
            creator_user=saved_user,
            storage=self.storage
        )

        yield instance

        instance.delete()

    @pytest.fixture
    def not_saved_instance(self, element_cls, saved_user):
        filepath = config.get_element_content_path()
        element_cls.load_from_txt(filepath)
        instance = self.model_cls(
            creator_user=saved_user,
            storage=self.storage,
            to_save=False
        )

        yield instance