from dataclasses import fields, dataclass

from shared.dictable import Dictable


@dataclass
class Message(Dictable):
    @staticmethod
    def convert(obj):
        if type(obj) in [int, bool, str, float, dict]:
            return obj
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        elif type(obj) in [set, list]:
            return [Message.convert(v) for v in obj]
        else:
            raise NotImplementedError(f"Cannot covert field of class {type(field)}")

    def as_dict(self):
        dict_ = {}
        simple_types = [int, bool, str, float, list, dict]

        for field in fields(self):
            value = getattr(self, field.name)
            dict_[field.name] = self.convert(value)
        return dict_
