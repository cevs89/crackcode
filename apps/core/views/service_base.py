from abc import abstractmethod
from typing import Optional

from django.db.models import Model, QuerySet


class BaseService:
    def __init__(self) -> None:
        self.queryset: Optional[QuerySet]

    @abstractmethod
    def _update_models_data(self, queryset: QuerySet, **data) -> Model:
        pass

    @abstractmethod
    def save(self, get_model: Model, **data: dict) -> Model:
        pass

    @staticmethod
    def _get_query_all(get_model: Model, _filters: dict) -> QuerySet:
        return get_model.objects.filter(**_filters)

    def _get_queryset(
        self, get_model: Model, _filters: dict, id_obj: id = None
    ) -> None:
        if id_obj is not None:
            _filters = {"pk": id_obj}

        try:
            queryset = get_model.objects.get(**_filters)
        except get_model.DoesNotExist:
            raise ValueError(f"{get_model.__name__} Doesn't exists")

        self.queryset = queryset

    def edit(self, get_model: Model, **data: dict):
        self._get_queryset(get_model, data, data["id"])

        return self._update_models_data(self.queryset, **data)

    def list(self, get_model: Model, _filters: dict) -> QuerySet:
        return self._get_query_all(get_model, _filters)

    def details(self, get_model: Model, _filters: dict) -> QuerySet:
        self._get_queryset(get_model, _filters)
        return self.queryset

    @abstractmethod
    def delete(self, get_model: Model, id_obj: id) -> str:
        pass
