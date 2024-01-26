from rest_framework import status, viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.validators import ValidateUploadFile
from apps.core.services import MassiveDataSave, UploadFileService


class UploadFileViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
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

        """
        Este proceso debería ser una tarea en segundo plano, como: Celery.
        """
        try:
            _response = MassiveDataSave(date_file).execute()
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(_response, status=status.HTTP_201_CREATED)
