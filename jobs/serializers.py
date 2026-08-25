from rest_framework import serializers

from .models import Job, SavedJob


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company",
            "company_name",
            "description",
            "requirements",
            "responsibilities",
            "skills",
            "job_type",
            "work_mode",
            "experience_level",
            "experience_min",
            "experience_max",
            "salary_min",
            "salary_max",
            "location",
            "vacancies",
            "application_deadline",
            "status",
            "views_count",
            "applications_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "views_count",
            "applications_count",
            "created_at",
            "updated_at",
        ]


class SavedJobSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True,
    )

    class Meta:
        model = SavedJob

        fields = [
            "id",
            "candidate",
            "job",
            "job_title",
            "company_name",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "created_at",
        ]