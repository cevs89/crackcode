from cerberus import Validator

from apps.api.helpers import SCHEMA
from apps.core.helpers import CustomErrorHandler


class UpdateValidationStudents:
    _array = {
        "guardian": {
            "type": "string",
            "required": True,
            "maxlength": 100,
            "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        }
    }

    schema = SCHEMA | _array

    def __init__(self, data):
        self.validator = Validator()
        self.validator.error_handler = CustomErrorHandler()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors
