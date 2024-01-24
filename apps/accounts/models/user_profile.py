from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class UserProfile(BaseModel):
    """
    This models represent User Profile.
        Field Required:
            user: OneToOneField | Unique | Required
            document_type: str max_length 10, Choices | None
            user_type: str max_length 5, Choices | None
            document_number: int | None
            country: ForeignKey | None
        Examples:
            El campo: document_type debería ser un modelo con una relación hacia todos los tipos de documentos,
            ahora mismo puse cualquiera, pero para el correcto funcionamiento de esto debería ser la relación

            Este campo será: user_type, dicho campo DEBERÍA ser una relación a los tipos de guardianes que éxisten.
            Ahora mismo solo tenemos:

            - padre
            - madre
            - tutor

            Pero en el futuro esto puede cambiar y las queries hacia string son más lentas que a una referencia DB,
            SE HACE PARA EFECTOS DE LA PRUEBA, PERO NO ESTÁ BIEN.

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_user_profile_related",
    )
    document_type = models.CharField(
        max_length=10,
        choices=(
            ("CEDULA", _("Cédula")),
            ("DNI", _("DNI")),
            ("PASAPORTE", _("Pasaporte")),
            ("OTRO", _("Otro")),
        ),
        default="DNI",
    )
    user_type = models.CharField(
        max_length=5,
        choices=(
            ("MADRE", _("Madre")),
            ("PADRE", _("Padre")),
            ("TUTOR", _("Tutor")),
        ),
        default="MADRE",
    )

    document_number = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey(
        "apps_core.Countries",
        on_delete=models.CASCADE,
        related_name="country_user_profile_related",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Perfil de Usuario")
        verbose_name_plural = _("Perfil de Usuarios")

        constraints = [
            models.UniqueConstraint(
                fields=["document_type", "document_number", "country"],
                name="unique_constraint_user_profile_document_type_document_number_and_country_has_unique",
            )
        ]

    def __str__(self):
        return f"{self.user}"
