import csv

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import HttpRequest

from apps.api.views.users import GuardiansViewSet, StudentsViewSet
from apps.career.validators import AddEnrollments, ValidateSalons

User = get_user_model()


class UploadFileService:
    def __init__(self, df_file):
        self.df_file = df_file

    def dict(self):
        file_save = ContentFile(self.df_file.encode(), "file_save.csv")
        csv_content = file_save.read().decode()
        csv_reader = csv.DictReader(csv_content.splitlines())

        for row in csv_reader:
            yield row


class MassiveDataSave:
    def __init__(self, _generator):
        self.generator = _generator

    @staticmethod
    def validate_guardian(email: str) -> bool:
        _email = email.lower().strip().replace(" ", " ")
        try:
            User.objects.get(email__exact=_email)
        except User.DoesNotExist:
            return False

        return True

    def _save_users(self) -> list:
        _student_view = StudentsViewSet()
        _guardian_view = GuardiansViewSet()

        _response = []
        _list_errors = []
        _request = HttpRequest()
        _request.method = "POST"

        for _data in self.generator:
            try:
                _queryset = ValidateSalons(_data["salon_id"]).execute()
            except Exception as e:
                raise ValueError(str(e))

            if self.validate_guardian(_data["guardian_email"]) is False:
                _guardian_data = {
                    "first_name": _data["guardian_name"],
                    "last_name": _data["guardian_last_name"],
                    "email": _data["guardian_email"],
                }

                if _data["guardian_document"]:
                    _guardian_data["document_number"] = int(
                        float(_data["guardian_document"])
                    )

                if _data["guardian_document_type"]:
                    _guardian_data["document_type"] = _data[
                        "guardian_document_type"
                    ].upper()

                if _data["guardian_type"]:
                    _guardian_data["user_type"] = _data["guardian_type"].upper()

                if _data["guardian_country"]:
                    _guardian_data["country"] = _data["guardian_country"].upper()

                _request.data = _guardian_data

                response_guardian = _guardian_view.create(_request)
                if response_guardian.status_code != 200:
                    _guardian_data["errors"] = response_guardian.data
                    _list_errors.append(_guardian_data)
                _response.append(response_guardian.data)

            # Students
            _student_data = {
                "first_name": _data["student_name"],
                "last_name": _data["student_last_name"],
                "email": _data["student_email"],
                "guardian": _data["guardian_email"],
            }
            _request.data = _student_data

            response_student = _student_view.create(_request)
            if response_student.status_code != 200:
                _student_data["errors"] = response_student.data
                _list_errors.append(_student_data)

            if response_student.status_code == 200:
                AddEnrollments(response_student.data, _queryset).execute()

            _response.append(response_student.data)

        if len(_list_errors) > 0:
            _response = _list_errors
        else:
            _response = _response

        return _response

    def execute(self) -> list:
        return self._save_users()
