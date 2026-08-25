from rest_framework import serializers

from .models import JobMatch


class JobMatchSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True,
    )

    class Meta:
        model = JobMatch
        fields = [
            "id",
            "job",
            "job_title",
            "company_name",
            "candidate",
            "match_score",
            "matched_skills",
            "missing_skills",
            "recommendation",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "candidate",
            "match_score",
            "matched_skills",
            "missing_skills",
            "recommendation",
            "created_at",
            "updated_at",
        ]