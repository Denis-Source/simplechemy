from __future__ import annotations

from logging import getLogger
from typing import List

from models.fungeble.recipe import Recipe


class ElementNotExistException(Exception):
    def __init__(self, element_name):
        self.element_name = element_name

    def __str__(self):
        return f"Element with name {self.element_name} does not exist"


class ElementException(Exception):
    def __init__(self, element: Element, message: str):
        self.element = element
        self.message = message

    def __str__(self):
        return self.message


class ElementAlreadyHasRecipeException(ElementException):
    def __init__(self, element: Element, recipe: Recipe):
        self.element = element
        self.recipe = recipe

    def __str__(self):
        return f"{self.element.NAME} {self.element} already has {self.recipe.NAME} {self.recipe}"


class ElementAlreadyHasInvolvedRecipeException(ElementAlreadyHasRecipeException):
    def __str__(self):
        return f"{self.element.NAME} {self.element} already has involved {self.recipe.NAME} {self.recipe}"


class IncompleteElementContent(ElementException):
    def __init__(self, source):
        self.source = source

    def __str__(self):
        return f"incomplete element content from {self.source}"


class IncorrectElementRecipe(ElementException):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return f"element cannot be obtained with {[str(element) for element in self.elements]}"


class NotUnlockedElementException(ElementException):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return f"element ({self.element}) is not unlocked"


class Element:
    NAME = "element model"
    logger = getLogger(NAME)

    _instances = {}
    _recipes = {}
    _starting = []

    def __init__(self, name: str, starting=False, recipe: List[Recipe] = None, recipes: List[Recipe] = None):
        instance = self._instances.get(name)
        if instance:
            self.name = instance.name
            self.starting = starting
            self.involved_recipes = instance.involved_recipes
            self.recipes = instance.recipes
            return

        self.name = name
        self.starting = starting
        if recipe:
            self.recipes = recipe
        else:
            self.recipes = []

        self.involved_recipes = recipes
        if not recipes:
            self.involved_recipes = []

        self._instances[self.name] = self

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return str(self) < str(other)

    @classmethod
    def get_element_count(cls):
        return len(cls._instances.values())

    @classmethod
    def get(cls, name):
        cls.logger.debug(f"getting {cls.NAME} {name}")
        instance = cls._instances.get(name)
        if not instance:
            raise ElementNotExistException(name)
        return instance

    def add_recipe(self, recipe: Recipe):
        self.logger.debug(f"adding {recipe.NAME} ({recipe}) for {self.NAME} {self}")
        if recipe not in self.recipes:
            self.recipes.append(recipe)
            recipe_key = tuple(sorted(recipe.schema))
            self._recipes[recipe_key] = self
        else:
            self.logger.debug(f"{self.NAME} {self} already has {recipe.NAME} ({recipe})")
            raise ElementAlreadyHasRecipeException(self, recipe)

    def add_involved_recipe(self, recipe: Recipe):
        self.logger.debug(f"adding involved {recipe.NAME} ({recipe}) for {self.NAME} {self}")
        if recipe not in self.involved_recipes:
            self.involved_recipes.append(recipe)
        else:
            self.logger.debug(f"{self.NAME} {self} already has involved {recipe.NAME} ({recipe})")
            raise ElementAlreadyHasInvolvedRecipeException(self, recipe)

    @classmethod
    def get_result(cls, elements):
        recipe_key = tuple(sorted(elements))
        result = cls._recipes.get(recipe_key)
        if not result:
            raise IncorrectElementRecipe(elements)

        return result

    @classmethod
    def list(cls, starting=False):
        cls.logger.debug(f"listing {cls.NAME} instances")

        if starting:
            return cls._starting
        return list(cls._instances.values())

    @classmethod
    def load_from_txt(cls, filepath: str):
        # TODO REFACTOR
        cls.reset_all()
        cls.logger.debug(f"loading {cls.NAME} from .txt file")

        with open(filepath, "r") as f:
            lines = f.readlines()

        total_elements = len(set([line.split("=")[0].strip() for line in lines]))

        # starting elements
        cls.logger.debug("loading starting elements")
        for line in lines:
            if line.count("=") == 0:
                element = Element(
                    name=line.strip(),
                    starting=True,
                    recipes=[],
                    recipe=None
                )
                cls._starting.append(element)

        cls.logger.debug(f"loaded ({Element.get_element_count()}) starting elements")
        cls.logger.debug("loading secondary elements")

        # secondary elements
        while Element.get_element_count() != total_elements:
            previous_count = cls.get_element_count()
            for line in lines:
                if line.count("=") == 0:
                    continue

                result_name = line.split("=")[0].strip()
                recipe_names = [recipe_name.strip() for recipe_name in line.split("=")[1].strip().split("+")]
                try:
                    all_there = all([Element.get(element_name) for element_name in recipe_names])
                except ElementNotExistException:
                    all_there = False

                if all_there:
                    new_element = Element(result_name, recipe=None)
                    recipe = Recipe(result=new_element,
                                    schema=[Element.get(element_name) for element_name in recipe_names])
                    try:
                        new_element.add_recipe(recipe)
                    except ElementAlreadyHasRecipeException:
                        pass
                    for involved_element in recipe.schema:
                        try:
                            involved_element.add_involved_recipe(recipe)
                        except ElementAlreadyHasInvolvedRecipeException:
                            pass
            if previous_count == cls.get_element_count():
                raise IncompleteElementContent(filepath)

        cls.logger.debug(f"loaded total: ({Element.get_element_count()}) elements")
        return Element.list()

    @classmethod
    def reset_all(cls):
        cls._instances = {}
        cls._recipes = {}
        cls._starting = []
