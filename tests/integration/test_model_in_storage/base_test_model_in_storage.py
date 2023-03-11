from abc import ABC, abstractmethod

import pytest

from models.base import BaseModel, InstanceDoesNotExist
from storage.base import BaseStorage


class BaseTestModelInStorage(ABC):
    storage: BaseStorage = None
    model_cls: BaseModel = None

    @pytest.fixture
    def saved_instance(self):
        instance = self.model_cls(
            storage=self.storage
        )

        yield instance

        instance.delete()

    @pytest.fixture
    def not_saved_instance(self):
        instance = self.model_cls(
            storage=self.storage,
            to_save=False
        )

        yield instance

    def test_not_saves_if_needed(self, not_saved_instance):
        assert self.storage.get(self.model_cls, not_saved_instance.uuid) is None

    def test_model_is_created(self, saved_instance):
        saved_instance = self.storage.get(self.model_cls, saved_instance.uuid)

        assert saved_instance == saved_instance

    def test_model_list(self, saved_instance):
        assert self.model_cls.list(storage=self.storage)

    def test_model_is_deleted(self, saved_instance):
        saved_instance.delete()
        saved_instance = self.storage.get(self.model_cls, saved_instance.uuid)

        assert saved_instance is None

    def test_model_does_not_exist(self, not_saved_instance):
        with pytest.raises(InstanceDoesNotExist):
            self.model_cls.get(not_saved_instance.uuid, storage=self.storage)

    @abstractmethod
    def test_model_to_dict_conversion(self):
        raise NotImplementedError

    @abstractmethod
    def test_model_change(self):
        raise NotImplementedError