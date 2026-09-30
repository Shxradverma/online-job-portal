from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Portal", {"fields": ("role", "phone", "is_email_verified")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Portal", {"fields": ("email", "role")}),)


    list_display = (
        "username",
        "email",
        "role",
        "is_email_verified",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "is_email_verified",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    ordering = ("-created_at",)