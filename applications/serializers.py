from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True,
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "job",
            "job_title",
            "company_name",
            "candidate",
            "resume",
            "cover_letter",
            "status",
            "recruiter_notes",
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "recruiter_notes",
            "applied_at",
            "updated_at",
        ]

    def validate_job(self, job):
        if job.status != job.Status.PUBLISHED:
            raise serializers.ValidationError(
                "You can only apply to published jobs."
            )

        return job

    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            job = attrs.get("job")

            if (
                job
                and self.instance is None
                and Application.objects.filter(
                    job=job,
                    candidate=request.user,
                ).exists()
            ):
                raise serializers.ValidationError(
                    "You have already applied to this job."
                )

        return attrs