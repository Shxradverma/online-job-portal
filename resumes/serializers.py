from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.SerializerMethodField()
    upload = serializers.FileField(write_only=True, required=False)

    def get_file(self, obj):
        return "/api/resumes/%s/download/" % obj.pk

    def to_internal_value(self, data):
        data = data.copy()
        if "file" in data:
            data["upload"] = data["file"]
        return super().to_internal_value(data)

    def validate(self, attrs):
        upload = attrs.pop("upload", None)
        if not self.instance and not upload:
            raise serializers.ValidationError({"file":"A PDF resume is required."})
        if upload:
            if upload.size > 5 * 1024 * 1024 or not upload.name.lower().endswith(".pdf"):
                raise serializers.ValidationError({"file":"Upload a PDF of at most 5 MB."})
            header = upload.read(5)
            upload.seek(0)
            if header != b"%PDF-":
                raise serializers.ValidationError({"file":"Invalid PDF document."})
            attrs["file"] = upload
        return attrs

    class Meta:
        model = Resume
        fields = [
            "id",
            "candidate",
            "title",
            "file",
            "upload",
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
