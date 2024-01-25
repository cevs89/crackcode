from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ValidateExistsUser:
    def __init__(self, email: str):
        self.email = email
        self.queryset = None

    def _normalize_email(self) -> None:
        self.email = self.email.lower().strip().replace(" ", "")

    def _queryset_exists(self) -> None:
        queryset = User.objects.filter(email=self.email)
        if queryset.exists():
            raise ValueError(
                _(
                    f"El Email {self.email} ya existe, por favor intente de nuevo con otro email"
                )
            )

    def execute(self) -> str:
        self._normalize_email()
        self._queryset_exists()
        return self.email

    @property
    def get_queryset(self) -> QuerySet:
        try:
            _query_user = User.objects.get(email=self.email)
        except User.DoesNotExist:
            raise ValueError(_("El guardian no existe"))
        return _query_user
