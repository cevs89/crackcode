from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BaseListViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = None
    serializer_class = None

    def list(self, request):
        queryset = self.queryset.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
