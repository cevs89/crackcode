from rest_framework.routers import DefaultRouter

from apps.api.views import GroupStudyViewSet

router = DefaultRouter()
router.register("group/study", GroupStudyViewSet, basename="group_study")
urlpatterns = router.urls
