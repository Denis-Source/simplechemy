from models.base import ModelException
from models.fungeble.element import Element
from models.nonfungeble.entity import Entity


class ElementPositionException(ModelException):
    pass


class ElementPositionOutOfBounds(ElementPositionException):
    def __init__(self, element_position):
        self.element_position = element_position

    def __str__(self):
        return f"{self.element_position} is out of bounds"


class ElementPosition(Entity):
    BOUNDS = 0, 1

    NAME = "elem_p"

    def __init__(self, element: Element, x: int, y: int, game=None, **kwargs):
        super().__init__(**kwargs)

        self.element = element
        self.x, self.y = x, y
        self.carried_by = None

        if game:
            self.game_uuid = game.uuid

    def __str__(self):
        return f"{self.uuid}-{self.element.name.lower().replace(' ', '_')}"

    def move_to(self, x: int, y: int, user, is_done: bool):
        if not self.BOUNDS[0] <= x < self.BOUNDS[1] or not self.BOUNDS[0] <= y < self.BOUNDS[1]:
            raise ElementPositionOutOfBounds(self)
        self.x, self.y = x, y
        if not is_done:
            self.carried_by = user
        else:
            self.carried_by = None

    def as_dict(self) -> dict:
        dict_ = super().as_dict()

        carried_by_d = None
        if self.carried_by:
            carried_by_d = self.carried_by.as_dict()

        dict_.update({
            "carried_by": carried_by_d,
            "x": self.x,
            "y": self.y,
            "element": self.element.as_dict()
        })
        return dict_
