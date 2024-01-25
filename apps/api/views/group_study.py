from apps.api.helpers import BaseListViewSet
from apps.api.serializers import GroupStudySerializer
from apps.career.models import GroupStudy


class GroupStudyViewSet(BaseListViewSet):
    queryset = GroupStudy
    serializer_class = GroupStudySerializer
