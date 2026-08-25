from rest_framework import serializers

from .models import CandidateProfile


class CandidateProfileSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = CandidateProfile

        fields = [
            "id",
            "user",
            "username",
            "user_email",
            "profile_photo",
            "bio",
            "location",
            "headline",
            "skills",
            "experience_years",
            "current_job_title",
            "expected_salary",
            "notice_period",
            "linkedin_url",
            "github_url",
            "portfolio_url",
            "is_profile_complete",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "username",
            "user_email",
            "is_profile_complete",
            "created_at",
            "updated_at",
        ]