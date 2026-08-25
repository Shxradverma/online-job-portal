from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resume
        fields = [
            "id",
            "candidate",
            "title",
            "file",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "created_at",
            "updated_at",
        ]
