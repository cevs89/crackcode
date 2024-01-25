from apps.api.helpers import BaseListViewSet
from apps.api.serializers import SalonsSerializer
from apps.career.models import Salons


class SalonsViewSet(BaseListViewSet):
    queryset = Salons
    serializer_class = SalonsSerializer
