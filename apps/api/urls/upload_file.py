from rest_framework.routers import DefaultRouter

from apps.api.views import UploadFileViewSet

router = DefaultRouter()
router.register("upload/file", UploadFileViewSet, basename="upload_file")
urlpatterns = router.urls
