from logging import getLogger

import config
from models.element import Element, IncorrectElementRecipe
from models.element_position import ElementPosition, ElementPositionWrongGame
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

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_.update({
            "creator_uuid": self.creator_uuid,
            "users": [user.to_dict() for user in self.users],
            "element_positions": [element_p.to_dict() for element_p in self.element_positions],
            "unlocked_elements": [element.name for element in self.unlocked_elements]
        })
        return dict_

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
            y=y,
            game=self
        )
        self.element_positions.append(element_p)
        self.save()
        return element_p

    def remove_element_p(self, element_p):
        self.logger.debug(f"removing {element_p} from {self}")
        self.element_positions.remove(element_p)

    def move_element_p(self, element_p, x, y, user, is_done):
        if element_p.game_uuid != self.uuid:
            raise ElementPositionWrongGame(element_p, self)

        self.logger.debug(f"moving {element_p} in {self} by {user}")
        element_p.move_to(
            x=x,
            y=y,
            user=user,
            is_done=is_done
        )

        if is_done:
            try:
                self.logger.debug(f"attempting to craft a new element")
                return self.craft_new_element(element_p, x, y)
            except IncorrectElementRecipe:
                self.logger.debug(f"not a valid recipe")
                return None, []

    def craft_new_element(self, element_p, x, y):
        result_element, used_elements_p = self.search_within_range(element_p)

        self.logger.info(f"element crafted ({result_element})")
        if result_element not in self.unlocked_elements:
            self.logger.info(f"new element unlocked ({result_element})")
            self.unlocked_elements.append(result_element)

        new_element_p = ElementPosition(
            element=result_element,
            x=x,
            y=y,
            storage=element_p.storage,
            game=self
        )

        for used_ep in used_elements_p:
            used_ep.delete()
            self.remove_element_p(used_ep)

        return new_element_p, used_elements_p

    def search_within_range(self, element_p):
        self.logger.debug(f"searching near elements")
        close_elements_p = []
        for other_element_p in self.element_positions:
            if abs(element_p.x) - abs(other_element_p.x) <= self.CRAFTING_RANGE and abs(element_p.y) - abs(
                    other_element_p.y <= self.CRAFTING_RANGE):
                close_elements_p.append(other_element_p)

        return Element.get_result([element_p.element for element_p in close_elements_p]), close_elements_p

    def clear_elements_p(self):
        self.logger.info(f"cleared all elements")
        for ep in self.element_positions:
            ep.delete()

        self.element_positions = []
