from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import IsRecruiter
from applications.models import Application
from .models import Interview

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ["id","application","scheduled_at","duration_minutes","meeting_url","location","notes","status"]
        read_only_fields = ["id","application"]
    def validate_duration_minutes(self, value):
        if not 5 <= value <= 480:
            raise serializers.ValidationError("Choose a duration from 5 to 480 minutes.")
        return value
    def validate_scheduled_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Choose a future interview time.")
        return value
    def validate(self, attrs):
        if not self.instance and not (attrs.get("meeting_url") or attrs.get("location")):
            raise serializers.ValidationError("Provide a meeting URL or interview location.")
        return attrs

class ApplicationInterviewsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InterviewSerializer
    def application(self):
        return get_object_or_404(Application.objects.filter(Q(candidate=self.request.user)|Q(job__recruiter=self.request.user)),pk=self.kwargs["pk"])
    def get_queryset(self): return Interview.objects.filter(application=self.application())
    def perform_create(self, serializer):
        application = self.application()
        if self.request.user.role != "RECRUITER" or application.job.recruiter_id != self.request.user.id:
            raise PermissionDenied("Only the job's recruiter can schedule an interview.")
        if application.status in ["WITHDRAWN", "REJECTED", "HIRED"]:
            raise serializers.ValidationError("This application is no longer active.")
        serializer.save(application=application, status="SCHEDULED")

class InterviewDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = InterviewSerializer
    def get_queryset(self): return Interview.objects.filter(application__job__recruiter=self.request.user)
