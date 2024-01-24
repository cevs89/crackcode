from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class GroupStudy(BaseModel):
    """
    This models represent all GroupStudy.
        Field Required:
            name: str  | Required
            description: str | None
            course: ForeignKey | Required
            start_time: DateTimeField | Required
            end_time: DateTimeField | Required
        Examples:
            NO ME QUEDA CLARO SI UN GRUPO PUEDE TENER VARIOS CURSOS. Pero entiendo que si se crea un grupo
            distinto se le puede agregar un mismo curso que ya está relacionado con un grupo. Por eso el nombre del
            grupo debe ser unico con el curso, Podemos permitir crear un grupo con un mismo nombre siempre y cuando no
            pertenezcan al mismo grupo:

            Grupo 1, Curso Python
            Grupo 2, Curso Python
            ___
            Grupo 1, Curso UX/UI

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    course = models.ForeignKey(
        "apps_career.Courses",
        on_delete=models.CASCADE,
        related_name="course_group_study_related",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = _("Group Study")
        verbose_name_plural = _("Groups Studies")

        constraints = [
            models.UniqueConstraint(
                fields=["name", "course"],
                name="unique_constraint_group_study_name_course_has_unique",
            )
        ]

    def __str__(self):
        return f"{self.name} with {self.course.name}"
