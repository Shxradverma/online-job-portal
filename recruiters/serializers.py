from rest_framework import serializers
from companies.models import Company
from jobs.models import Job
from jobs.serializers import JobSerializer
from applications.models import Application

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "description", "website", "industry", "company_size", "headquarters"]

class RecruiterJobSerializer(JobSerializer):
    def validate_company(self, company):
        if company.created_by_id != self.context["request"].user.id:
            raise serializers.ValidationError("Choose a company owned by your account.")
        return company
    def validate(self, attrs):
        def val(key): return attrs.get(key, getattr(self.instance, key, None))
        for low, high in [("salary_min", "salary_max"), ("experience_min", "experience_max")]:
            if val(low) is not None and val(high) is not None and val(low) > val(high):
                raise serializers.ValidationError({high:"Maximum must be at least the minimum."})
        if val("vacancies") == 0:
            raise serializers.ValidationError({"vacancies":"At least one vacancy is required."})
        return attrs

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "recruiter_notes"]
    def validate_status(self, value):
        if self.instance.status == Application.Status.WITHDRAWN:
            raise serializers.ValidationError("A withdrawn application cannot be changed.")
        if value not in ["REVIEWING", "SHORTLISTED", "REJECTED", "HIRED"]:
            raise serializers.ValidationError("Choose reviewing, shortlisted, rejected or hired.")
        return value
