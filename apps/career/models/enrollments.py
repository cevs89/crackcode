from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Enrollments(BaseModel):
    """
    This models represent all GroupStudy.
        Field Required:
            student: ForeignKey | required
            salon: ForeignKey | required
            course: ForeignKey | required
            group_study: ForeignKey | required

        _validate_user_student:
            Validaré que el usuario que se guarde siempre sea un Estudiante, debe tener su grupo de usuario asignado,
            aquí me apoyo con el modelo Group de Django, para el propósito del proyecto el modelo Grupo es suficiente.

        Examples:
            El Estudiante no puede estar 2 veces en un mismo salon, grupo o curso.
            Esta relación se hacen para evitar por medio de UniqueConstraint que esto suceda, síno se tendría que
            hacer con logica, que no me parece tan limpio.

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_enrollments_related",
    )

    salon = models.ForeignKey(
        "apps_career.Salons",
        on_delete=models.CASCADE,
        related_name="salon_enrollments_related",
    )
    course = models.ForeignKey(
        "apps_career.Courses",
        on_delete=models.CASCADE,
        related_name="course_enrollments_related",
    )
    group_study = models.ForeignKey(
        "apps_career.GroupStudy",
        on_delete=models.CASCADE,
        related_name="group_study_enrollments_related",
    )

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")

        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_constraint_enrollments_student_course_has_unique",
            ),
            models.UniqueConstraint(
                fields=["student", "group_study"],
                name="unique_constraint_enrollments_student_group_study_has_unique",
            ),
            models.UniqueConstraint(
                fields=["student", "salon"],
                name="unique_constraint_enrollments_student_salon_has_unique",
            ),
        ]

    def _validate_user_student(self):
        if not self.student.groups.filter(name__exact="student").exists():
            raise ValidationError({"teacher": _("El usuario debe ser un estudiante")})

    def save(self, *args, **kwargs):
        self._validate_user_student()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}"
