from django.db import transaction
from django.db.models import F

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer


class ApplyJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        application = serializer.save(
            candidate=self.request.user
        )

        # Increase job application counter
        type(application.job).objects.filter(
            id=application.job.id
        ).update(
            applications_count=F("applications_count") + 1
        )


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects
            .filter(candidate=self.request.user)
            .select_related(
                "job",
                "job__company",
                "resume",
            )
        )


class ApplicationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects
            .filter(candidate=self.request.user)
            .select_related(
                "job",
                "job__company",
                "resume",
            )
        )


class WithdrawApplicationAPIView(generics.UpdateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            status=Application.Status.WITHDRAWN
        )


class RecruiterApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects
            .filter(job__recruiter=self.request.user)
            .select_related(
                "job",
                "job__company",
                "candidate",
                "resume",
            )
        )


class RecruiterJobApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]

        return (
            Application.objects
            .filter(
                job_id=job_id,
                job__recruiter=self.request.user,
            )
            .select_related(
                "job",
                "job__company",
                "candidate",
                "resume",
            )
        )


class UpdateApplicationStatusAPIView(generics.UpdateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects
            .filter(job__recruiter=self.request.user)
            .select_related(
                "job",
                "job__company",
                "candidate",
                "resume",
            )
        )