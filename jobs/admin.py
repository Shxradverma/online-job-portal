from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "recruiter",
        "job_type",
        "work_mode",
        "experience_level",
        "location",
        "status",
        "applications_count",
        "created_at",
    )

    list_filter = (
        "job_type",
        "work_mode",
        "experience_level",
        "status",
        "location",
    )

    search_fields = (
        "title",
        "company__name",
        "recruiter__email",
        "location",
        "skills",
    )

    ordering = ("-created_at",)