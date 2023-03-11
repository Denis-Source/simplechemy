import pytest

from models.entity import Entity
from storage.memory import MemoryStorage
from tests.integration.test_model_in_storage.base_test_model_in_storage import BaseTestModelInStorage


class TestEntityInMemoryStorage(BaseTestModelInStorage):
    storage = MemoryStorage()
    model_cls = Entity

    def test_model_to_dict_conversion(self, saved_instance: Entity):
        assert saved_instance.to_dict() == {
            "type": self.model_cls.NAME,
            "uuid": saved_instance.uuid,
            "name": saved_instance.name
        }

    def test_model_change(self, saved_instance):
        ordinary_name = "Fine Name"

        saved_instance.change(name=ordinary_name)

        assert self.storage.get(self.model_cls, saved_instance.uuid).name == ordinary_name
