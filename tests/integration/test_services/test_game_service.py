import pytest

import config
from models.fungeble.element import Element, IncorrectElementRecipe
from models.nonfungeble.element_position import ElementPosition
from models.nonfungeble.game import Game
from models.nonfungeble.user import User
from services.commands.model_commands import ModelCreateCommand
from services.commands.game_commands import GameAddElementPCommand, GameRemoveElementPCommand, GameMoveElementPCommand
from services.events.game_events import GameAddedElementPEvent, GameElementNotExistEvent, \
    GameRemovedElementPEvent, GameElementPNotInGameEvent, GameMovedElementPEvent, GameElementPOutOfBoundsEvent, \
    GameNewElementPCraftedEvent
from services.handlers.game_handler_service import GameHandlerService
from tests.integration.test_services.base_test_model_service import BaseTestModelServices


class TestGameServices(BaseTestModelServices):
    model_cls = Game
    handler_cls = GameHandlerService

    @pytest.fixture
    def saved_user(self, reset_storage):
        instance = User()
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    @pytest.fixture(scope="module")
    def element_cls(self):
        filepath = config.get_element_content_path()
        Element.load_from_txt(filepath)

        yield Element
        Element.reset_all()

    @pytest.fixture
    def saved_instance(self, saved_user, element_cls):
        instance = self.model_cls(
            creator_user=saved_user
        )
        self.storage.put(instance)
        yield instance
        self.storage.delete(instance)

    def test_created(self, reset_storage, saved_user):
        cmd = ModelCreateCommand(
            model_cls_name=self.model_cls.NAME,
            fields={
                "name": "test name",
                "creator_user": saved_user
            }
        )

        event = self.message_bus.handle(cmd)

        saved_instance = self.storage.get(
            model_cls=self.model_cls,
            uuid=event.instance.uuid
        )

        assert event.instance == saved_instance
        assert event.instance.name == cmd.fields.get("name")
        assert self.storage.get(Game, event.instance.uuid).creator_uuid == saved_user.uuid

    def test_add_element_p_success(self, element_cls, saved_instance, reset_storage):
        for element in element_cls.list(starting=True):
            cmd = GameAddElementPCommand(
                instance=saved_instance,
                element=element,
                x=0,
                y=0
            )

            event = self.message_bus.handle(cmd)
            assert isinstance(event, GameAddedElementPEvent)
            assert event.element_p.element == element
            assert event.element_p.x == event.element_p.y == 0

            assert event.element_p == self.storage.get(ElementPosition, event.element_p.uuid)
            assert event.element_p in self.storage.get(Game, saved_instance.uuid).element_positions

    def test_add_element_p_locked(self, element_cls, saved_instance, reset_storage):
        for element in element_cls.list():
            if element.starting:
                continue

            cmd = GameAddElementPCommand(
                instance=saved_instance,
                element=element,
                x=0,
                y=0
            )

            event = self.message_bus.handle(cmd)
            assert isinstance(event, GameElementNotExistEvent)

    def test_add_element_p_not_exist(self, element_cls, saved_instance):
        non_existent_element_name = "00"
        cmd = GameAddElementPCommand(
            instance=saved_instance,
            element=non_existent_element_name,
            x=0,
            y=0
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameElementNotExistEvent)

    @pytest.fixture
    def saved_added_element_p(self, saved_instance, element_cls):
        element_p = saved_instance.add_element_p(element_cls.list(starting=True)[0])
        self.storage.put(element_p)
        self.storage.put(saved_instance)
        yield element_p
        self.storage.delete(element_p)

    @pytest.fixture
    def another_saved_added_element_p(self, saved_instance, saved_added_element_p, element_cls):
        element = saved_added_element_p.element
        another_element = None
        for u_e in saved_instance.unlocked_elements:
            try:
                element_cls.get_result([element, u_e])
                another_element = u_e
            except IncorrectElementRecipe:
                pass

        if not another_element:
            raise Exception("cannot find element for the test")

        element_p = saved_instance.add_element_p(another_element)
        self.storage.put(element_p)
        self.storage.put(saved_instance)
        yield element_p
        self.storage.delete(element_p)

    def test_remove_element_p_success(self, saved_instance, saved_added_element_p):
        assert saved_instance == self.storage.get(ElementPosition, saved_instance.uuid)
        assert saved_added_element_p in self.storage.get(Game, saved_instance.uuid).element_positions

        cmd = GameRemoveElementPCommand(
            saved_instance,
            saved_added_element_p
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameRemovedElementPEvent)

        assert saved_added_element_p not in self.storage.get(Game, saved_instance.uuid).element_positions
        assert self.storage.get(ElementPosition, saved_added_element_p.uuid) is None

    def test_remove_element_p_not_in_game(self, saved_instance, saved_added_element_p):
        saved_instance.remove_element_p(
            element_p=saved_added_element_p
        )
        self.storage.delete(saved_added_element_p)
        self.storage.put(saved_instance)

        assert self.storage.get(ElementPosition, saved_added_element_p.uuid) is None
        cmd = GameRemoveElementPCommand(
            saved_instance,
            saved_added_element_p
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameElementPNotInGameEvent)

    def test_move_element_p_success(self, saved_user, saved_instance, saved_added_element_p):
        new_x = 0.3
        new_y = 0.4

        cmd = GameMoveElementPCommand(
            instance=saved_instance,
            element_p=saved_added_element_p,
            x=new_x,
            y=new_y,
            user=saved_user,
            is_done=True
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameMovedElementPEvent)
        assert event.element_p.x == new_x
        assert event.element_p.y == new_y

        assert self.storage.get(ElementPosition, saved_added_element_p.uuid).x == new_x
        assert self.storage.get(ElementPosition, saved_added_element_p.uuid).y == new_y

    def test_move_element_p_not_in_game(self, saved_user, saved_instance, saved_added_element_p):
        saved_instance.remove_element_p(saved_added_element_p)
        self.storage.delete(saved_added_element_p)

        cmd = GameMoveElementPCommand(
            instance=saved_instance,
            element_p=saved_added_element_p,
            x=0.3,
            y=0.4,
            user=saved_user,
            is_done=True
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameElementPNotInGameEvent)

    def test_move_element_p_out_of_bounds(self, saved_instance, saved_user, saved_added_element_p):
        new_x = 0.3 + ElementPosition.BOUNDS[0]
        new_y = 0.3 + ElementPosition.BOUNDS[1]

        cmd = GameMoveElementPCommand(
            instance=saved_instance,
            element_p=saved_added_element_p,
            x=new_x,
            y=new_y,
            user=saved_user,
            is_done=True
        )

        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameElementPOutOfBoundsEvent)

    def test_move_elements_crafted_success(self, saved_instance, saved_user, saved_added_element_p,
                                           another_saved_added_element_p, element_cls):
        cmd = GameMoveElementPCommand(
            instance=saved_instance,
            element_p=saved_added_element_p,
            x=0,
            y=0,
            user=saved_user,
            is_done=True
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameNewElementPCraftedEvent)
        assert event.element_p.element == element_cls.get_result([saved_added_element_p.element,
                                                                  another_saved_added_element_p.element])
        assert event.element_p.element in self.storage.get(Game, saved_instance.uuid).unlocked_elements

    def test_move_elements_crafted_not_done(self, saved_instance, saved_user, saved_added_element_p,
                                            another_saved_added_element_p, ):
        cmd = GameMoveElementPCommand(
            instance=saved_instance,
            element_p=saved_added_element_p,
            x=0,
            y=0,
            user=saved_user,
            is_done=False
        )
        event = self.message_bus.handle(cmd)
        assert isinstance(event, GameMovedElementPEvent)
        assert len(self.storage.get(Game, saved_instance.uuid).element_positions) == 2
