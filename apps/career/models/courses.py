from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Courses(BaseModel):
    """
    This models represent all courses.
        Field Required:
            name: str | Unique | Required
            slug: str | Unique | Required (Automatically)
            description: str | None
        Examples:
            None
        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    name = models.CharField(_("Name"), max_length=255, unique=True)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
