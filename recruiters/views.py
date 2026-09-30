from rest_framework import generics
from accounts.permissions import IsRecruiter
from companies.models import Company
from jobs.models import Job
from .serializers import CompanySerializer, RecruiterJobSerializer

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = CompanySerializer
    def get_queryset(self): return Company.objects.filter(created_by=self.request.user)
    def perform_create(self, serializer): serializer.save(created_by=self.request.user)

class RecruiterJobListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterJobSerializer
    def get_queryset(self): return Job.objects.filter(recruiter=self.request.user).select_related("company")
    def perform_create(self, serializer): serializer.save(recruiter=self.request.user)

class RecruiterJobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsRecruiter]
    serializer_class = RecruiterJobSerializer
    def get_queryset(self): return Job.objects.filter(recruiter=self.request.user).select_related("company")
