from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Salons(BaseModel):
    """
    This models represent all GroupStudy.
        Field Required:
            name: str  | Required
            group_study: OneToOneField | Required
            teacher: ForeignKey | Required

        _validate_user:
            Validara que el usuario que se guarde siempre sea un profesor, debe tener su grupo de usuario asignado,
            aquí me apoyo con el modelo Group de Django. para el propósito del proyecto el modelo Grupo es suficiente.

        Examples:
            None

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    name = models.CharField(_("Name"), max_length=255)
    group_study = models.OneToOneField(
        "apps_career.GroupStudy",
        on_delete=models.CASCADE,
        related_name="group_study_salons_related",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_salons_related",
    )

    class Meta:
        verbose_name = _("Salon")
        verbose_name_plural = _("Salons")

    def _validate_user(self):
        if not self.teacher.groups.filter(name__exact="teacher").exists():
            raise ValidationError({"teacher": _("El usuario debe ser un profesor")})

    def save(self, *args, **kwargs):
        self._validate_user()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
