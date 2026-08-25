from django.urls import path

from .views import (
    ResumeListCreateAPIView,
    ResumeDetailAPIView,
)


urlpatterns = [
    path(
        "",
        ResumeListCreateAPIView.as_view(),
        name="resume-list-create",
    ),

    path(
        "<int:pk>/",
        ResumeDetailAPIView.as_view(),
        name="resume-detail",
    ),
]
