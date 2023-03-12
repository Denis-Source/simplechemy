import re
from abc import ABC, abstractmethod

import pytest

from storage.memory import MemoryStorage


class BaseTestModel(ABC):
    model_cls = None
    storage = MemoryStorage()

    @pytest.fixture
    def uuid_regex(self):
        return r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"

    @pytest.fixture
    def model_instance(self):
        return self.model_cls(storage=self.storage)

    @pytest.fixture
    def another_model_instance(self):
        return self.model_cls(storage=self.storage)

    def test_model_created(self, uuid_regex, model_instance):
        assert model_instance
        assert re.match(uuid_regex, model_instance.uuid)
        assert model_instance.name == f"{model_instance.NAME}-{model_instance.uuid}"

    def test_two_uuid_are_unique(self, model_instance, another_model_instance):
        assert model_instance.uuid != another_model_instance.uuid
        assert model_instance != another_model_instance

    @abstractmethod
    def test_correct_dict(self):
        raise NotImplementedError
