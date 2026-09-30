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
            "applied_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "status",
            "applied_at",
            "updated_at",
        ]

    def validate_job(self, job):
        if job.status != job.Status.PUBLISHED:
            raise serializers.ValidationError(
                "You can only apply to published jobs."
            )

        from django.utils import timezone
        if job.application_deadline and job.application_deadline < timezone.localdate():
            raise serializers.ValidationError("The application deadline has passed.")
        return job

    def validate_resume(self, resume):
        if resume and resume.candidate_id != self.context["request"].user.id:
            raise serializers.ValidationError("You can only use your own resume.")
        return resume

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

class RecruiterApplicationSerializer(ApplicationSerializer):
    candidate_name = serializers.CharField(source="candidate.username", read_only=True)
    candidate_email = serializers.EmailField(source="candidate.email", read_only=True)
    class Meta(ApplicationSerializer.Meta):
        fields = ApplicationSerializer.Meta.fields + ["candidate_name", "candidate_email", "recruiter_notes"]
        read_only_fields = fields
