import pytest

from models.element import Element
from models.recipe import Recipe


class TestRecipeModel:
    @pytest.fixture
    def element_cls(self):
        yield Element
        Element.reset_all()


    @pytest.fixture
    def element_one(self, element_cls):
        return element_cls(
            "Air",
            starting=True,
        )

    @pytest.fixture
    def element_two(self, element_cls):
        return element_cls(
            "Water",
            starting=True
        )

    def test_equal_recipes(self, element_one, element_two, element_cls):
        result_element = element_cls("Cloud")
        recipe_one = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        recipe_two = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        assert recipe_one == recipe_two
        assert recipe_one.schema == recipe_two.schema

    def test_different_recipes(self, element_one, element_two, element_cls):
        result_element = element_cls("Cloud")

        recipe_one = Recipe(
            result=result_element,
            schema=[element_one, element_two]
        )

        recipe_two = Recipe(
            result=result_element,
            schema=[element_two, element_two]
        )

        assert recipe_one != recipe_two
        assert recipe_one.result == recipe_two.result
        assert recipe_one.schema != recipe_two.schema
