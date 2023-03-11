import re

import pytest

from models.entity import Entity
from storage.memory import MemoryStorage


class BaseTestModel:
    model_cls = None
    storage = MemoryStorage()

    @pytest.fixture
    def uuid_regex(self):
        return r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"

    @pytest.fixture
    def ordinary_name(self):
        return "fine name"

    def test_model_created(self, uuid_regex):
        instance = self.model_cls(storage=self.storage)
        assert instance
        assert re.match(uuid_regex, instance.uuid)
        assert instance.name == f"{instance.NAME}-{instance.uuid}"

    def test_model_name_specified(self, ordinary_name):
        instance = self.model_cls(
            name=ordinary_name,
            storage=self.storage
        )

        assert instance.name == ordinary_name

    def test_two_uuid_are_unique(self, ordinary_name):
        instance1 = self.model_cls(
            storage=self.storage,
            name=ordinary_name
        )
        instance2 = self.model_cls(
            storage=self.storage,
            name=ordinary_name
        )
        assert instance1.uuid != instance2.uuid
        assert instance1 != instance2
        assert instance1.name == instance2.name

    def test_correct_dict(self):
        model = self.model_cls(storage=self.storage)
        model.to_dict() == {
            "name": model.name,
            "uuid": model.uuid
        }


class TestEntityModel(BaseTestModel):
    model_cls = Entity
