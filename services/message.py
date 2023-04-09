from dataclasses import fields, dataclass

from shared.dictable import Dictable


@dataclass
class Message(Dictable):
    NAME = "message"

    @staticmethod
    def convert(obj):
        if type(obj) in [int, bool, str, float, dict]:
            return obj
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        elif type(obj) in [set, list]:
            return [Message.convert(v) for v in obj]
        else:
            raise NotImplementedError(f"Cannot covert field of class {type(obj)}")

    def as_dict(self):
        dict_ = {}
        for field in fields(self):
            value = getattr(self, field.name)
            dict_[field.name] = self.convert(value)
            dict_["message"] = self.NAME
        return dict_
