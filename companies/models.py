from django.conf import settings
from django.db import models


class Company(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    logo = models.ImageField(
        upload_to="companies/logos/",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    industry = models.CharField(
        max_length=150,
        blank=True,
    )

    company_size = models.CharField(
        max_length=100,
        blank=True,
    )

    headquarters = models.CharField(
        max_length=200,
        blank=True,
    )

    founded_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_companies",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name