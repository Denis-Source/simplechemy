from __future__ import annotations

from logging import getLogger
from typing import List

from models.recipe import Recipe


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


class Element:
    NAME = "element model"
    logger = getLogger(NAME)
    _instances = {}

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
        involved_recipes = "\n".join([f"{str(recipe)}" for recipe in self.involved_recipes])
        return f"{self.name}"

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def get_element_count(cls):
        return len(cls._instances.values())

    @classmethod
    def get(cls, name):
        cls.logger.debug(f"getting {cls.NAME} {name}")
        return cls._instances.get(name)

    def add_recipe(self, recipe: Recipe):
        self.logger.debug(f"adding {recipe.NAME} ({recipe}) for {self.NAME} {self}")
        if recipe not in self.recipes:
            self.recipes.append(recipe)
        else:
            self.logger.debug(f"{self.NAME} {self} already has {recipe.NAME} ({recipe})")
            raise ElementAlreadyHasRecipeException(self, recipe)

    def add_involved_recipe(self, recipe: Recipe):
        self.logger.debug(f"adding involved {recipe.NAME} ({recipe}) for {self.NAME} {self}")
        if not recipe in self.involved_recipes:
            self.involved_recipes.append(recipe)
        else:
            self.logger.debug(f"{self.NAME} {self} already has involved {recipe.NAME} ({recipe})")
            raise ElementAlreadyHasInvolvedRecipeException(self, recipe)

    @classmethod
    def list(cls):
        cls.logger.debug(f"listing {cls.NAME} instances")
        return list(cls._instances.values())

    @classmethod
    def load_from_txt(cls, filepath: str):
        cls.logger.debug(f"loading {cls.NAME} from .txt file")

        with open(filepath, "r") as f:
            lines = f.readlines()
        total_lines = len(lines)

        # starting elements
        cls.logger.debug(f"loading starting elements")
        for line in lines:
            if line.count(" ") == 0:
                Element(
                    name=line.strip(),
                    starting=True,
                    recipes=[],
                    recipe=None
                )
        cls.logger.debug(f"loaded ({Element.get_element_count()}) starting elements")
        cls.logger.debug(f"loading secondary elements")
        # secondary element
        while Element.get_element_count() != total_lines:
            for line in lines:
                if line.count(" ") == 0:
                    continue

                result_name = line.split("=")[0].strip()
                recipe_names = [recipe_name.strip() for recipe_name in line.split("=")[1].strip().split("+")]
                if all([Element.get(element_name) for element_name in recipe_names]):
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

        cls.logger.debug(f"loaded total: ({Element.get_element_count()}) elements")
        return Element.list()

    @classmethod
    def reset_all(cls):
        cls._instances = {}