from django.contrib import admin

from .models import RecruiterProfile


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "company",
        "designation",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "company",
    )

    search_fields = (
        "user__email",
        "user__username",
        "company__name",
        "designation",
    )