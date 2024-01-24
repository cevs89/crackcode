from django.db import models

from apps.core.models import BaseModel


class Countries(BaseModel):
    """
    This models represent all country available list.
        Field Required:
            name: str -> max_length 255 | Unique | Required
            code: str -> max_length 2 | Required
        Examples:
            code is ISO 3166 country codes.
            - Peru = PE
            - Colombia = CO
            - Argentina = AR
            - Venezuela = VE

        Fields heritage - BaseModel
            uuid
            is_active
            created_at
            modified_at
    """

    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=2)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"
