from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(
        "obtain/token/",
        include("apps.api.urls.obtain_token"),
    ),
    path(
        "users/",
        include("apps.api.urls.users"),
    ),
    path(
        "masive/",
        include("apps.api.urls.upload_file"),
    ),
    path(
        "",
        include("apps.api.urls.group_study"),
    ),
]
