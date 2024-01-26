from cerberus import Validator

from apps.accounts.models import UserProfile
from apps.api.helpers import SCHEMA
from apps.core.helpers import CustomErrorHandler


class ValidationUsers:
    _array = {
        "email": {
            "type": "string",
            "required": True,
            "maxlength": 100,
            "regex": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        },
        "document_type": {
            "type": "string",
            "required": False,
            "empty": False,
            "allowed": list(dict(UserProfile.DOCUMENT_TYPE_CHOICES).keys()),
        },
        "user_type": {
            "type": "string",
            "required": False,
            "empty": False,
            "allowed": list(dict(UserProfile.USER_TYPE_CHOICES).keys()),
        },
        "document_number": {"type": "integer", "required": False, "empty": False},
        "country": {
            "type": "string",
            "required": False,
            "maxlength": 2,
            "empty": False,
            "allowed": ["VE", "CO", "AR"],
        },
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
