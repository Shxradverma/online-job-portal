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
        TokenObtainPairView.as_view(),
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


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )