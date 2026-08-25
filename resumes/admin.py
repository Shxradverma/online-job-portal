from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "candidate",
        "title",
        "is_default",
        "created_at",
    )

    list_filter = (
        "is_default",
        "created_at",
    )

    search_fields = (
        "candidate__email",
        "candidate__username",
        "title",
    )