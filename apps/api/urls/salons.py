from rest_framework.routers import DefaultRouter

from apps.api.views import SalonsViewSet

router = DefaultRouter()
router.register("salons/study", SalonsViewSet, basename="salons_study")
urlpatterns = router.urls
