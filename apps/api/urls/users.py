from rest_framework.routers import DefaultRouter

from apps.api.views import GuardiansViewSet, StudentsViewSet, TeachersViewSet

router = DefaultRouter()
router.register("students", StudentsViewSet, basename="students")
router.register("teachers", TeachersViewSet, basename="teachers")
router.register("guardians", GuardiansViewSet, basename="guardians")
urlpatterns = router.urls
