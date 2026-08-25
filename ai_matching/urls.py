from django.urls import path

from .views import (
    MyJobMatchesAPIView,
    GenerateJobMatchAPIView,
)


urlpatterns = [

    path(
        "my/",
        MyJobMatchesAPIView.as_view(),
        name="my-job-matches",
    ),

    path(
        "generate/",
        GenerateJobMatchAPIView.as_view(),
        name="generate-job-match",
    ),

]