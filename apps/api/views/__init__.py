from apps.api.views.group_study import GroupStudyViewSet
from apps.api.views.salons import SalonsViewSet
from apps.api.views.upload_file import UploadFileViewSet
from apps.api.views.users import GuardiansViewSet, StudentsViewSet, TeachersViewSet

__all__ = [
    "StudentsViewSet",
    "TeachersViewSet",
    "GuardiansViewSet",
    "UploadFileViewSet",
    "GroupStudyViewSet",
    "SalonsViewSet",
]
