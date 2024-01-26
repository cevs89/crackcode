from django.db import IntegrityError, transaction

from apps.career.models import Enrollments, Salons


class AddEnrollments:
    def __init__(self, data_user: dict, data_salons: Salons):
        self.data_user = data_user
        self.data_salons = data_salons

    def _save_data(self) -> None:
        try:
            with transaction.atomic():
                _query_save = Enrollments()
                _query_save.student_id = self.data_user["id"]
                _query_save.salon = self.data_salons
                _query_save.save()
        except (Exception, IntegrityError) as e:
            raise ValueError(str(e))

    def execute(self) -> None:
        self._save_data()
