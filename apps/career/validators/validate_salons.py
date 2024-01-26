from apps.career.models import Salons


class ValidateSalons:
    def __init__(self, id_salon: int):
        self.id_salon = id_salon

    def _queryset_validate(self) -> Salons:
        try:
            _queryset = Salons.objects.get(id=self.id_salon)
        except Salons.DoesNotExist:
            raise ValueError(f"El salon {self.id_salon} no existe")

        return _queryset

    def execute(self) -> Salons:
        return self._queryset_validate()
