from django.db import models
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Job, SavedJob
from .serializers import JobSerializer, SavedJobSerializer


class JobPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class JobSearchAPIView(generics.ListAPIView):
    serializer_class = JobSerializer
    pagination_class = JobPagination

    def get_queryset(self):
        queryset = (
            Job.objects
            .filter(status=Job.Status.PUBLISHED)
            .select_related("company", "recruiter")
        )

        params = self.request.query_params

        search = params.get("search")
        location = params.get("location")
        job_type = params.get("job_type")
        work_mode = params.get("work_mode")
        experience_level = params.get("experience_level")
        company = params.get("company")

        salary_min = params.get("salary_min")
        salary_max = params.get("salary_max")

        ordering = params.get("ordering", "-created_at")

        # Keyword search
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(skills__icontains=search)
                | Q(company__name__icontains=search)
            )

        # Location
        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        # Job type
        if job_type:
            queryset = queryset.filter(
                job_type=job_type
            )

        # Work mode
        if work_mode:
            queryset = queryset.filter(
                work_mode=work_mode
            )

        # Experience level
        if experience_level:
            queryset = queryset.filter(
                experience_level=experience_level
            )

        # Company
        if company:
            queryset = queryset.filter(
                company__name__icontains=company
            )

        # Salary
        if salary_min:
            queryset = queryset.filter(
                salary_max__gte=salary_min
            )

        if salary_max:
            queryset = queryset.filter(
                salary_min__lte=salary_max
            )

        # Allowed sorting
        allowed_ordering = [
            "created_at",
            "-created_at",
            "salary_min",
            "-salary_min",
            "salary_max",
            "-salary_max",
            "views_count",
            "-views_count",
        ]

        if ordering not in allowed_ordering:
            ordering = "-created_at"

        return queryset.order_by(ordering)


class JobDetailAPIView(generics.RetrieveAPIView):
    serializer_class = JobSerializer

    queryset = (
        Job.objects
        .filter(status=Job.Status.PUBLISHED)
        .select_related("company", "recruiter")
    )

    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()

        Job.objects.filter(
            id=job.id
        ).update(
            views_count=models.F("views_count") + 1
        )

        job.refresh_from_db()

        serializer = self.get_serializer(job)

        return Response(serializer.data)


class SaveJobAPIView(generics.CreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        job_id = request.data.get("job")

        if not job_id:
            return Response(
                {"detail": "job is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            job = Job.objects.get(
                id=job_id,
                status=Job.Status.PUBLISHED,
            )
        except Job.DoesNotExist:
            return Response(
                {"detail": "Published job not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        saved_job, created = SavedJob.objects.get_or_create(
            candidate=request.user,
            job=job,
        )

        serializer = self.get_serializer(saved_job)

        if not created:
            return Response(
                {
                    "detail": "Job already saved.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class SavedJobListAPIView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            SavedJob.objects
            .filter(candidate=self.request.user)
            .select_related("job", "job__company")
        )


class DeleteSavedJobAPIView(generics.DestroyAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(
            candidate=self.request.user
        )