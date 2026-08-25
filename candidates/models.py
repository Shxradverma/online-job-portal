from django.conf import settings
from django.db import models


class CandidateProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )

    profile_photo = models.ImageField(
        upload_to="candidates/profile/",
        blank=True,
        null=True,
    )

    bio = models.TextField(blank=True)

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    headline = models.CharField(
        max_length=200,
        blank=True,
    )

    skills = models.TextField(
        blank=True,
        help_text="Comma-separated skills",
    )

    experience_years = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0,
    )

    current_job_title = models.CharField(
        max_length=150,
        blank=True,
    )

    expected_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    notice_period = models.CharField(
        max_length=100,
        blank=True,
    )

    linkedin_url = models.URLField(blank=True)

    github_url = models.URLField(blank=True)

    portfolio_url = models.URLField(blank=True)

    is_profile_complete = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.user.email} - Candidate"