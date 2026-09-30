from accounts.permissions import IsCandidate, IsRecruiter
from recruiters.serializers import ApplicationStatusSerializer
from rest_framework import serializers
from rest_framework.response import Response
from django.db import IntegrityError
from django.db import transaction
from django.db.models import F

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer, RecruiterApplicationSerializer


class ApplyJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                application = serializer.save(candidate=self.request.user)
                type(application.job).objects.filter(id=application.job.id).update(applications_count=F("applications_count") + 1)
        except IntegrityError:
            raise serializers.ValidationError("You have already applied to this job.")


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsCandidate]

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
    permission_classes = [IsCandidate]

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
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        application = self.get_queryset().select_for_update().get(pk=self.get_object().pk)
        if application.status in [Application.Status.HIRED, Application.Status.REJECTED]:
            raise serializers.ValidationError("This application is already finalized.")
        application.status = Application.Status.WITHDRAWN
        application.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(application).data)


class RecruiterApplicationsAPIView(generics.ListAPIView):
    serializer_class = RecruiterApplicationSerializer
    permission_classes = [IsRecruiter]

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
    serializer_class = RecruiterApplicationSerializer
    permission_classes = [IsRecruiter]

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
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_object(self):
        instance = super().get_object()
        return self.get_queryset().select_for_update().get(pk=instance.pk)

    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsRecruiter]

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