from logging import getLogger

import config
from models.entity import Entity


class Game(Entity):
    NAME = "game model"
    logger = getLogger(NAME)

    def __init__(self, creator_user,  name: str = None, to_save=True, storage=config.get_storage(),
                 **kwargs):
        super().__init__(name=name, to_save=False, **kwargs)

        self.creator_uuid = creator_user.uuid
        self.users = []

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
