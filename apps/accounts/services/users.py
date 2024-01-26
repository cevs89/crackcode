from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from apps.accounts.services import SaveGroupUser, UserProfileService
from apps.accounts.validators import ValidateExistsUser
from apps.core.views import BaseService

User = get_user_model()


class UsersService(BaseService):
    def __init__(self, group_user: str):
        self.group_user = group_user
        super().__init__()

    def _update_models_data(self, queryset: User, **data) -> User:
        try:
            with transaction.atomic():
                _update_models = queryset
                _update_models.first_name = data["first_name"]
                _update_models.last_name = data["last_name"]
                _update_models.save()

                UserProfileService(self.group_user, _update_models, data).execute()

        except (Exception, IntegrityError) as e:
            raise ValueError(str(e))

        return _update_models

    @staticmethod
    def _normalize_email(email: str) -> str:
        return str(email.lower().strip().replace(" ", ""))

    def save(self, get_model: User, **data: dict) -> Model:
        ValidateExistsUser(str(data["email"])).execute()

        try:
            with transaction.atomic():
                _save_models = get_model()
                _save_models.first_name = data["first_name"]
                _save_models.last_name = data["last_name"]
                _save_models.email = self._normalize_email(str(data["email"]))
                _save_models.set_password("123456")
                _save_models.is_staff = False
                _save_models.is_active = True
                _save_models.save()

                SaveGroupUser(self.group_user, _save_models).execute()
                UserProfileService(self.group_user, _save_models, data).execute()

        except (Exception, IntegrityError) as e:
            raise ValueError(str(e))

        return _save_models

    def delete(self, get_model: Model, id_obj: id) -> str:
        self._get_queryset(get_model, {"pk": id_obj})

        try:
            self.queryset.delete()
        except Exception as e:
            raise ValueError(str(e))

        _msg_response = _("El usuario ha sido borrado")
        return _msg_response
