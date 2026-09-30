from messaging.views import ApplicationMessagesAPIView
from interviews.views import ApplicationInterviewsAPIView, InterviewDetailAPIView
from analytics.views import DashboardAnalyticsAPIView
from notifications.views import ActivityAPIView
from django.contrib.auth import views as auth_views
from accounts.authentication import LoginAPIView
from accounts.views import RegisterAPIView, MeAPIView
from recruiters.views import CompanyListCreateAPIView, RecruiterJobListCreateAPIView, RecruiterJobDetailAPIView
from django.http import JsonResponse
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def home(request):
    return render(request, "index.html")


def job_detail(request, job_id):
    return render(
        request,
        "job-detail.html",
        {"job_id": job_id},
    )
def login_page(request):
    return render(request, "login.html")
def profile_page(request):
    return render(request, "profile.html")

urlpatterns = [
    path("api/analytics/", DashboardAnalyticsAPIView.as_view()),
    path("api/notifications/", ActivityAPIView.as_view()),
    path("api/applications/<int:pk>/messages/", ApplicationMessagesAPIView.as_view()),
    path("api/applications/<int:pk>/interviews/", ApplicationInterviewsAPIView.as_view()),
    path("api/interviews/<int:pk>/", InterviewDetailAPIView.as_view()),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("jobs/<int:job_id>/", job_detail),
    path("register/", lambda r: render(r, "register.html")),
    path("dashboard/", lambda r: render(r, "dashboard.html")),
    path("health/", lambda r: JsonResponse({"status":"ok"})),
    path("api/auth/register/", RegisterAPIView.as_view()),
    path("api/auth/me/", MeAPIView.as_view()),
    path("api/auth/token/refresh/", TokenRefreshView.as_view()),
    path("api/recruiter/companies/", CompanyListCreateAPIView.as_view()),
    path("api/recruiter/jobs/", RecruiterJobListCreateAPIView.as_view()),
    path("api/recruiter/jobs/<int:pk>/", RecruiterJobDetailAPIView.as_view()),
    path("", home, name="home"),

    path(
        "login/",
        login_page,
        name="login-page",
    ),
    path(
    "profile/",
    profile_page,
    name="profile-page",
),

    path("admin/", admin.site.urls),

    path(
        "api/auth/token/",
        LoginAPIView.as_view(),
        name="token-obtain-pair",
    ),

    path(
        "api/jobs/",
        include("jobs.urls"),
    ),

    path(
        "api/applications/",
        include("applications.urls"),
    ),

    path(
        "api/candidates/",
        include("candidates.urls"),
    ),

    path(
        "api/resumes/",
        include("resumes.urls"),
    ),

    path(
        "api/ai-matching/",
        include("ai_matching.urls"),
    ),

]

