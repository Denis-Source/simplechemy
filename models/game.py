from logging import getLogger

import config
from models.element import Element, IncorrectElementRecipe
from models.element_position import ElementPosition
from models.entity import Entity


class Game(Entity):
    NAME = "game model"
    logger = getLogger(NAME)

    CRAFTING_RANGE = 0.05

    def __init__(self, creator_user, name: str = None, to_save=True, storage=config.get_storage(),
                 **kwargs):
        super().__init__(name=name, to_save=False, **kwargs)

        self.creator_uuid = creator_user.uuid
        self.users = []
        self.element_positions = []
        self.unlocked_elements = Element.list(starting=True)

        if to_save:
            self.save()

    def __contains__(self, user):
        return user in self.users

    def add_user(self, user) -> None:
        self.logger.debug(f"adding {user.NAME} {user} to {self.NAME} {self}")
        self.users.append(user)
        self.save()

    def remove_user(self, user) -> None:
        self.logger.debug(f"removing {user.NAME} {user} from {self.NAME} {self}")
        self.users.remove(user)
        self.save()

    def add_element_p(self, element, x=0, y=0):
        self.logger.debug(f"adding {ElementPosition.NAME} to {self}")
        element_p = ElementPosition(
            element=element,
            x=x,
            y=y
        )
        self.element_positions.append(element_p)
        self.save()
        return element_p

    def remove_element_p(self, element_p):
        self.logger.debug(f"removing {element_p} from {self}")
        self.element_positions.remove(element_p)

    def move_element_p(self, element_p, x, y, user, is_done):
        # TODO check game id of the ep and

        self.logger.debug(f"moving {element_p} in {self} by {user}")
        element_p.move_to(
            x=x,
            y=y,
            user=user,
            is_done=is_done
        )

        if is_done:
            try:
                result_element, used_elements_p = self.search_within_range(element_p)

                self.unlocked_elements.append(result_element)

                new_element_p = ElementPosition(
                    element=result_element,
                    x=x,
                    y=y,
                    storage=element_p.storage
                )

                for used_ep in used_elements_p:
                    used_ep.delete()
                return new_element_p, used_elements_p
            except IncorrectElementRecipe:
                return None, []

    def search_within_range(self, element_p):
        close_elements_p = []
        for other_element_p in self.element_positions:
            if abs(element_p.x) - abs(other_element_p.x) <= self.CRAFTING_RANGE and abs(element_p.y) - abs(
                    other_element_p.y <= self.CRAFTING_RANGE):
                close_elements_p.append(other_element_p)

        return Element.get_result([element_p.element for element_p in close_elements_p]), close_elements_p
