from .views import ResumeDownloadAPIView
from django.urls import path

from .views import (
    ResumeListCreateAPIView,
    ResumeDetailAPIView,
)


urlpatterns = [
    path("<int:pk>/download/", ResumeDownloadAPIView.as_view()),
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
