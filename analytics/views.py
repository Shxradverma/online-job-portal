from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jobs.models import Job, SavedJob
from applications.models import Application

class DashboardAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role == "RECRUITER":
            applications = Application.objects.filter(job__recruiter=request.user)
            jobs = Job.objects.filter(recruiter=request.user)
            extra = {"jobs":jobs.count(), "published_jobs":jobs.filter(status="PUBLISHED").count()}
        else:
            applications = Application.objects.filter(candidate=request.user)
            extra = {"saved_jobs":SavedJob.objects.filter(candidate=request.user).count()}
        return Response({"applications":applications.count(), "by_status":list(applications.values("status").annotate(count=Count("id"))), **extra})
