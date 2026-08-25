from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class JobMatch(models.Model):

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_matches",
    )

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="candidate_matches",
    )

    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    matched_skills = models.JSONField(
        default=list,
        blank=True,
    )

    missing_skills = models.JSONField(
        default=list,
        blank=True,
    )

    recommendation = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = ("candidate", "job")
        ordering = ["-match_score", "-created_at"]

    def __str__(self):
        return (
            f"{self.candidate.email} - "
            f"{self.job.title} - "
            f"{self.match_score}%"
        )