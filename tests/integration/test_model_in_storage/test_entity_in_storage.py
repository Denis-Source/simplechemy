import pytest

from models.nonfungeble.entity import Entity
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.base_test_model_in_storage import BaseTestModelInStorage


class TestEntityInMemoryStorage(BaseTestModelInStorage):
    storage = MemoryStorage()
    model_cls = Entity

    def test_model_change(self, saved_instance):
        ordinary_name = "Fine Name"

        saved_instance.change(name=ordinary_name)

        assert self.storage.get(self.model_cls, saved_instance.uuid).name == ordinary_name
