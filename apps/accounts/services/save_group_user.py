from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SaveGroupUser:
    def __init__(self, group_user: str, user_data: User):
        self.group_user = group_user
        self.user_data = user_data

    def _validate_user_group(self) -> None:
        try:
            self.query_group = Group.objects.get(name__iexact=self.group_user)
        except Group.DoesNotExist:
            # Se supone que esto no debería pasar
            raise ValueError(_("El grupo no existe, porfavor intente de nuevo"))

    def _add_group_user_create(self) -> None:
        try:
            self.query_group.user_set.add(self.user_data)
        except Exception as e:
            # Se supone que esto no debería pasar
            raise ValueError(
                _(f"Error al intentar guardar el grupo {self.group_user}:"),
                f"Technical detail {e}",
            )

    def execute(self) -> None:
        self._validate_user_group()
        self._add_group_user_create()
