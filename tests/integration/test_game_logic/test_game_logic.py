import pytest

import config
from models.element import Element
from models.element_position import ElementPosition, ElementPositionWrongGame
from models.game import Game
from models.user import User
from storage.memory import MemoryStorage


class TestGameLogic:
    storage = MemoryStorage()

    @pytest.fixture
    def saved_user(self):
        instance = User(
            storage=self.storage,
        )

        yield instance

        instance.delete()

    @pytest.fixture
    def element_cls(self):
        filepath = config.get_element_content_path()
        Element.load_from_txt(filepath)

        yield Element
        Element.reset_all()

    @pytest.fixture
    def saved_instance(self, saved_user, element_cls):
        instance = Game(
            creator_user=saved_user,
            storage=self.storage
        )
        saved_user.enter_game(instance)

        yield instance

        instance.delete()

    @pytest.fixture
    def another_saved_instance(self, saved_user, element_cls, saved_instance):
        instance = Game(
            creator_user=saved_user,
            storage=self.storage
        )
        saved_user.leave_game(saved_instance)
        saved_user.enter_game(instance)

        yield instance

        instance.delete()

    @pytest.fixture
    def starting_element(self, element_cls):
        element = element_cls.list(starting=True)[0]

        return element

    @pytest.fixture
    def obtainable_element(self, element_cls):
        for e in element_cls.list():
            if not e.starting:
                return e

    def test_add_element_p(self, element_cls, saved_instance, starting_element):
        saved_instance.add_element_p(
            element=starting_element,
            x=0,
            y=0
        )

        assert starting_element in [element_p.element for element_p in saved_instance.element_positions]

    def test_remove_element_p(self, element_cls, saved_instance, starting_element):
        element_p = saved_instance.add_element_p(
            element=starting_element,
            x=0,
            y=0
        )

        assert saved_instance.element_positions

        saved_instance.remove_element_p(element_p)

        assert not saved_instance.element_positions

    def test_move_element_p(self, element_cls, saved_user, saved_instance, starting_element):
        element_p = saved_instance.add_element_p(
            element=starting_element,
            x=0,
            y=0
        )

        assert saved_instance.element_positions[0].x == 0
        assert saved_instance.element_positions[0].y == 0

        saved_instance.move_element_p(
            element_p=element_p,
            x=0.3,
            y=0.3,
            user=saved_user,
            is_done=True,

        )

        element_p = self.storage.get(ElementPosition, element_p.uuid)

        assert element_p
        assert element_p.x == element_p.y == 0.3

        assert saved_instance.element_positions[0].x == 0.3
        assert saved_instance.element_positions[0].y == 0.3

    def test_new_element_created(self, element_cls, obtainable_element, saved_user, saved_instance):
        elements = obtainable_element.recipes[0].schema
        element_ps = []
        for e in elements:
            ep = saved_instance.add_element_p(
                element=e,
                x=0,
                y=0,
            )
            element_ps.append(ep)

        for ep in element_ps[:-1]:
            saved_instance.move_element_p(
                element_p=ep,
                x=0.3,
                y=0.3,
                user=saved_user,
                is_done=True
            )

        result_ep, used_elements_p = saved_instance.move_element_p(
            element_p=element_ps[-1],
            x=0.3,
            y=0.3,
            user=saved_user,
            is_done=True
        )

        assert result_ep
        assert result_ep.element == obtainable_element
        assert set(used_elements_p) == set(element_ps)

    def test_if_unlocked_elements_correct(self, element_cls, saved_instance):
        assert set(saved_instance.unlocked_elements) == set(element_cls.list(starting=True))

    def test_if_game_can_be_completed(self, element_cls, saved_instance, saved_user):
        for element in saved_instance.unlocked_elements:
            for recipy in element.involved_recipes:
                if all([r_elem in saved_instance.unlocked_elements for r_elem in recipy.schema]):
                    ep = [saved_instance.add_element_p(
                        r_elem
                    ) for r_elem in recipy.schema]

                    result, ele = saved_instance.move_element_p(
                        element_p=ep[-1],
                        user=saved_user,
                        is_done=True,
                        x=0,
                        y=0
                    )
                    saved_instance.clear_elements_p()

        assert set(saved_instance.unlocked_elements) == set(Element.list())

    def test_move_element_p_but_wrong_game_uuid(self, starting_element, saved_instance, another_saved_instance,
                                                saved_user):
        element_p = saved_instance.add_element_p(starting_element)

        with pytest.raises(ElementPositionWrongGame):
            another_saved_instance.move_element_p(
                element_p=element_p,
                x=0.3,
                y=0.3,
                user=saved_user,
                is_done=True
            )
