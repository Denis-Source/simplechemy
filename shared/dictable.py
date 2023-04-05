from abc import ABC


class Dictable(ABC):
    def as_dict(self):
        raise NotImplementedError
