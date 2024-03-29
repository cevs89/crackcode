from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class StudentsUserProfile(BaseModel):
    """
    This models represent profile for Students Users.
        Field Required:
            user: OneToOneField | Unique | Required
            guardian: ForeignKey | Required
        Examples:
            Teniendo en cuenta que los estudiantes son menores de edad, no tienen documentos de identidad como DNI,
            se creara aquí y se le relaciona un guardian o representante.

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_students_user_profile_related",
    )
    guardian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_students_user_profile_related",
    )

    class Meta:
        verbose_name = _("Perfil del Estudiante")
        verbose_name_plural = _("Perfil de Estudiante")

    def _validate_user_student(self):
        if not self.user.groups.filter(name__exact="student").exists():
            raise ValidationError({"teacher": _("El usuario debe ser un estudiante")})

    def _validate_user_guardian(self):
        if not self.guardian.groups.filter(name__exact="guardian").exists():
            raise ValidationError(
                {"teacher": _("El usuario debe ser un representante/guardian")}
            )

    def save(self, *args, **kwargs):
        self._validate_user_student()
        self._validate_user_guardian()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"
