from django.urls import path

from .views import (
    JobSearchAPIView,
    JobDetailAPIView,
    SaveJobAPIView,
    SavedJobListAPIView,
    DeleteSavedJobAPIView,
)


urlpatterns = [
    path(
        "",
        JobSearchAPIView.as_view(),
        name="job-list",
    ),

    path(
        "search/",
        JobSearchAPIView.as_view(),
        name="job-search",
    ),

    path(
        "<int:id>/",
        JobDetailAPIView.as_view(),
        name="job-detail",
    ),

    path(
        "save/",
        SaveJobAPIView.as_view(),
        name="job-save",
    ),

    path(
        "saved/",
        SavedJobListAPIView.as_view(),
        name="saved-jobs",
    ),

    path(
        "saved/<int:pk>/",
        DeleteSavedJobAPIView.as_view(),
        name="saved-job-delete",
    ),
]