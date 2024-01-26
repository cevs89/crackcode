from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    service = None
    serializer_class = None
    validations_class = None
    validations_update_class = None
    queryset = None
    _filters = {}

    def list(self, request, **kwargs):
        """Method GET"""
        try:
            queryset = self.service.list(self.queryset, self._filters)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """Method POST"""
        get_validation = self.validations_class(request.data)
        if get_validation.validate():
            try:
                query_save = self.service.save(self.queryset, **get_validation.data)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(query_save)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(get_validation.errors(), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        """Method GET with Params"""
        try:
            self._filters["pk"] = pk
            queryset = self.service.details(self.queryset, self._filters)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        """Method PUT with Params and Body"""
        get_validation = self.validations_update_class(request.data)
        if get_validation.validate():
            get_validation.data["id"] = pk
            try:
                query_edit = self.service.edit(self.queryset, **get_validation.data)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(query_edit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(get_validation.errors(), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """Method Delete with Params"""

        try:
            _response_delete = self.service.delete(self.queryset, pk)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": _response_delete}, status=status.HTTP_200_OK)
