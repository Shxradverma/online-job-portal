from rest_framework import generics
from accounts.permissions import IsCandidate

from jobs.models import Job
from candidates.models import CandidateProfile

from .models import JobMatch
from .serializers import JobMatchSerializer
from .services import create_or_update_job_match


class MyJobMatchesAPIView(generics.ListAPIView):

    serializer_class = JobMatchSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return JobMatch.objects.filter(
            candidate=self.request.user
        ).select_related(
            "job",
            "job__company",
        )


class GenerateJobMatchAPIView(generics.CreateAPIView):

    serializer_class = JobMatchSerializer
    permission_classes = [IsCandidate]

    def create(self, request, *args, **kwargs):
        job_id = request.data.get("job")

        if not job_id:
            from rest_framework.response import Response
            from rest_framework import status

            return Response(
                {"detail": "job is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            job = Job.objects.select_related(
                "company"
            ).get(
                id=job_id,
                status=Job.Status.PUBLISHED,
            )
        except (Job.DoesNotExist, ValueError, TypeError):
            from rest_framework.response import Response
            from rest_framework import status

            return Response(
                {"detail": "Published job not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            profile = CandidateProfile.objects.get(
                user=request.user
            )
        except CandidateProfile.DoesNotExist:
            from rest_framework.response import Response
            from rest_framework import status

            return Response(
                {"detail": "Candidate profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        job_match = create_or_update_job_match(
            profile,
            job,
        )

        serializer = self.get_serializer(job_match)

        return Response(
            serializer.data,
            status=200,
        )