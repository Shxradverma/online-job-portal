from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    role = serializers.ChoiceField(choices=["CANDIDATE", "RECRUITER"])
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password", "first_name", "last_name", "role"]
        read_only_fields = ["id"]
    def validate_email(self, value):
        value = value.strip().lower()
        if get_user_model().objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    def validate(self, attrs):
        try:
            validate_password(attrs["password"], get_user_model()(**{k:v for k,v in attrs.items() if k != "password"}))
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})
        return attrs
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
