from rest_framework.routers import DefaultRouter

from apps.api.views import UploadFileViewSet

router = DefaultRouter()
router.register("upload/file", UploadFileViewSet, basename="Upload File")
urlpatterns = router.urls
