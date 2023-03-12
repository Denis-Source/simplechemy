from random import shuffle

import pytest

import config
from models.element import Element, IncompleteElementContent


class TestElementsAndRecipes:
    @pytest.fixture
    def element_cls(self):
        yield Element
        Element.reset_all()

    @pytest.fixture
    def mock_recipes(self):
        return "Air\n" \
               "Water\n" \
               "Fire\n" \
               "Soil\n" \
               "Bird = Air + Life\n" \
               "Life = Energy + Water\n" \
               "Energy = Thunderbolt + Thunderbolt\n" \
               "Thunderbolt = Cloud + Cloud\n" \
               "Cloud = Air + Water\n" \
               "Compass = Electricity + Magnet\n" \
               "Electricity = Metal + Thunderbolt\n" \
               "Metal = Fire + Stone\n" \
               "Stone = Soil + Soil\n" \
               "Magnet = Electricity + Metal", 14

    @pytest.fixture
    def mock_txt_file_with_recipes(self, mock_recipes, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(mock_recipes[0])

        return filepath, mock_recipes[1]

    @pytest.fixture
    def incomplete_mock_recipes(self, mock_recipes):
        return mock_recipes[0] + \
               "Puddle = Road + Water\n", mock_recipes[1] + 2

    @pytest.fixture
    def mock_recipes_with_more_than_one_option(self):
        return "Air\n" \
               "Water\n" \
               "Cloud = Air + Water\n" \
               "Cloud = Air + Air", 3

    @pytest.fixture
    def mock_txt_file_with_recipes_with_more_than_one_option(self, mock_recipes_with_more_than_one_option, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(mock_recipes_with_more_than_one_option[0])

        return filepath, mock_recipes_with_more_than_one_option[1]

    @pytest.fixture
    def incomplete_mock_txt_file_with_recipes(self, incomplete_mock_recipes, tmpdir):
        filepath = tmpdir.join("mock_recipes.txt")
        with open(filepath, "w") as f:
            f.write(incomplete_mock_recipes[0])

        return filepath

    def test_element_loaded_from_txt(self, element_cls, mock_txt_file_with_recipes):
        filepath, correct_amount = mock_txt_file_with_recipes

        elements = element_cls.load_from_txt(filepath)
        assert len(elements) == correct_amount
        assert element_cls.get_element_count() == correct_amount

    def test_element_loaded_from_txt_shuffled(self, element_cls, mock_recipes, tmpdir):
        recipe, correct_amount = mock_recipes
        elements_example = None

        for i in range(2):
            filepath = tmpdir.join(f"mock_recipes{i}.txt")
            with open(filepath, "w") as f:
                shuffled_recipe = [line.strip() for line in recipe.split("\n")]
                shuffle(shuffled_recipe)
                f.write(
                    "\n".join(shuffled_recipe)
                )

            elements = element_cls.load_from_txt(filepath)
            assert len(elements) == correct_amount
            assert element_cls.get_element_count() == correct_amount

            # confirm that every single result is identical to the first one
            if not elements_example:
                elements_example = elements
            else:
                assert set(elements) == set(elements_example)

    def test_incomplete_element_content(self, element_cls, incomplete_mock_txt_file_with_recipes):
        with pytest.raises(IncompleteElementContent):
            element_cls.load_from_txt(incomplete_mock_txt_file_with_recipes)

    def test_elements_can_have_two_or_more_recipes(self, element_cls,
                                                   mock_txt_file_with_recipes_with_more_than_one_option):
        filepath, correct_amount = mock_txt_file_with_recipes_with_more_than_one_option

        elements = element_cls.load_from_txt(filepath)
        assert len(elements) == correct_amount
        assert element_cls.get_element_count() == correct_amount

    def test_if_element_content_path(self, element_cls):
        filepath = config.get_element_content_path()
        element_cls.load_from_txt(filepath)
        assert element_cls.list()

    def check_obtainability(self, element: Element, obtainability_dict: dict = None):
        if element.starting:
            status = True
            obtainability_dict[element] = status
            return status
        else:
            status = all(
                all(self.check_obtainability(recipe_element, obtainability_dict)
                    for recipe_element in recipe.schema)
                for recipe in element.recipes)
            obtainability_dict[element] = status
            return status

    def test_if_all_elements_in_content_path_obtainable(self, element_cls):
        filepath = config.get_element_content_path()
        element_cls.load_from_txt(filepath)

        obtain_dict = {}

        for element in element_cls.list():
            self.check_obtainability(element, obtain_dict)

        assert all([obtain_dict.values()])
