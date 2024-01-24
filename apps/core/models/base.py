# Ui universal
import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Base Models:
    Purpose:
        Se hace un modelo base para evitar escribir los mismos campos en todos los modelos,
        evitar repetir código es lo mejor que podemos aplicar.
    Fields:
        uuid: podríamos usarlo como ID unico para operaciones donde no nos importe que vean el ID
        is_active: Todos los registro dentro de una DB deben manejar estados
        created_at: Fecha de creación, solo se modifica su única vez cuando se crea
        modified_at: Fecha de modificación, se modifica siempre que se actualice el modelo
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        verbose_name="UUID",
        unique=True,
        editable=False,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
