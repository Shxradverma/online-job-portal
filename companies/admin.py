from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "industry",
        "company_size",
        "headquarters",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "industry",
        "company_size",
    )

    search_fields = (
        "name",
        "industry",
        "headquarters",
    )