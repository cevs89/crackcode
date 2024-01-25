from django.contrib.auth import get_user_model

from apps.accounts.services import UsersService
from apps.api.serializers import UsersSerializer
from apps.api.validators import (
    UpdateValidationStudents,
    UpdateValidationUsers,
    ValidationStudents,
    ValidationUsers,
)
from apps.core.views import BaseViewSet

User = get_user_model()


class StudentsViewSet(BaseViewSet):
    service = UsersService("student")
    _filters = {"is_active": True, "groups__name": "student"}
    queryset = User
    serializer_class = UsersSerializer
    validations_class = ValidationStudents
    validations_update_class = UpdateValidationStudents


class TeachersViewSet(BaseViewSet):
    service = UsersService("teacher")
    _filters = {"is_active": True, "groups__name": "teacher"}
    queryset = User
    serializer_class = UsersSerializer
    validations_class = ValidationUsers
    validations_update_class = UpdateValidationUsers


class GuardiansViewSet(BaseViewSet):
    service = UsersService("guardian")
    _filters = {"is_active": True, "groups__name": "guardian"}
    queryset = User
    serializer_class = UsersSerializer
    validations_class = ValidationUsers
    validations_update_class = UpdateValidationUsers
