from dataclasses import fields, dataclass

from shared.dictable import Dictable


@dataclass
class Message(Dictable):
    def as_dict(self):
        dict_ = {}
        simple_types = [int, bool, str, float, list, dict]

        for field in fields(self):
            value = getattr(self, field.name)
            if type(value) in simple_types:
                dict_[field.name] = value
            elif hasattr(value, "as_dict"):
                dict_[field.name] = value.as_dict()
            else:
                raise NotImplementedError(f"Cannot covert field of class {type(field)}")

        return dict_
