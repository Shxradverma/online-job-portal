from django.urls import path

from .views import (
    ApplyJobAPIView,
    MyApplicationsAPIView,
    ApplicationDetailAPIView,
    WithdrawApplicationAPIView,
    RecruiterApplicationsAPIView,
    RecruiterJobApplicationsAPIView,
    UpdateApplicationStatusAPIView,
)
urlpatterns = [
    path(
        "apply/",
        ApplyJobAPIView.as_view(),
        name="apply-job",
    ),

    path(
        "my/",
        MyApplicationsAPIView.as_view(),
        name="my-applications",
    ),

    path(
        "<int:pk>/",
        ApplicationDetailAPIView.as_view(),
        name="application-detail",
    ),

    path(
        "<int:pk>/withdraw/",
        WithdrawApplicationAPIView.as_view(),
        name="withdraw-application",
    ),
path(
    "recruiter/",
    RecruiterApplicationsAPIView.as_view(),
    name="recruiter-applications",
),

path(
    "recruiter/job/<int:job_id>/",
    RecruiterJobApplicationsAPIView.as_view(),
    name="recruiter-job-applications",
),
path(
    "<int:pk>/status/",
    UpdateApplicationStatusAPIView.as_view(),
    name="update-application-status",
),
]