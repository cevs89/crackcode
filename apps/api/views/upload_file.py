from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.validators import ValidateUploadFile
from apps.api.views.users import GuardiansViewSet, StudentsViewSet
from apps.core.services import UploadFileService


class UploadFileViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    # serializer_class = UploadFileSerializer
    # queryset = FileUploadCSV.objects.filter()
    service_file = UploadFileService
    service = UploadFileService
    parser_class = (FileUploadParser,)
    validations_class = ValidateUploadFile()

    def create(self, request):
        try:
            file_validate = self.validations_class.file(request.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        try:
            date_file = self.service_file(file_validate).dict()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        _student_view = StudentsViewSet()
        _guardian_view = GuardiansViewSet()

        """
        Este proceso debería ser una tarea en segundo plano, como: Celery.
        """
        _response = []
        _list_errors = []
        _request = HttpRequest()
        _request.method = "POST"
        # FALTA GUARDAR EL SALON
        for _data in date_file:
            _guardian_data = {
                "first_name": _data["guardian_name"],
                "last_name": _data["guardian_last_name"],
                "email": _data["guardian_email"],
                # 'salon_id': _data["salon_id"],
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
            _response.append(response_student.data)

        if len(_list_errors) > 0:
            _response = _list_errors
        else:
            _response = _response
        return Response(_response, status=status.HTTP_201_CREATED)
