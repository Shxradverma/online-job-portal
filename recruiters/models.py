from django.conf import settings
from django.db import models

from companies.models import Company


class RecruiterProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="recruiters",
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="recruiters/profile/",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.user.email} - {self.company.name}"