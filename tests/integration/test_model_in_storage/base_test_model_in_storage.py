from abc import ABC, abstractmethod

import pytest

from models.base import BaseModel
from storage.base import BaseStorage


class BaseTestModelInStorage(ABC):
    storage: BaseStorage = None
    model_cls: BaseModel = None

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls()
        self.storage.put(instance)

        yield instance
        self.storage.delete(instance)

    @pytest.fixture
    def not_saved_instance(self):
        instance = self.model_cls()

        yield instance

    def test_model_is_created(self, saved_instance):
        saved_instance = self.storage.get(self.model_cls, saved_instance.uuid)

        assert saved_instance == saved_instance

    def test_model_list(self, saved_instance):
        instances = self.storage.list(self.model_cls)
        assert len(instances) == 1

    def test_model_is_deleted(self, saved_instance):
        self.storage.delete(saved_instance)
        saved_instance = self.storage.get(self.model_cls, saved_instance.uuid)

        assert saved_instance is None

    def test_model_does_not_exist(self, not_saved_instance):
        assert self.storage.get(self.model_cls, not_saved_instance.uuid) is None

    @abstractmethod
    def test_model_change(self):
        raise NotImplementedError
