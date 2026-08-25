from django.contrib import admin

from .models import CandidateProfile


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "headline",
        "location",
        "experience_years",
        "is_profile_complete",
        "created_at",
    )

    list_filter = (
        "is_profile_complete",
        "location",
    )

    search_fields = (
        "user__email",
        "user__username",
        "headline",
        "location",
        "skills",
    )