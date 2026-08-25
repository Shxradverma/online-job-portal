from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "candidate",
        "job",
        "status",
        "applied_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "candidate__email",
        "candidate__username",
        "job__title",
        "job__company__name",
    )

    ordering = ("-applied_at",)