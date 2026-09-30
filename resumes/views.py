from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from accounts.permissions import IsCandidate

from .models import Resume
from .serializers import ResumeSerializer


class ResumeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Resume.objects.filter(
            candidate=self.request.user
        )

    def perform_create(self, serializer):
        from django.db import transaction
        from django.contrib.auth import get_user_model
        with transaction.atomic():
            get_user_model().objects.select_for_update().get(pk=self.request.user.pk)
            if serializer.validated_data.get("is_default"):
                self.get_queryset().update(is_default=False)
            serializer.save(candidate=self.request.user)


class ResumeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    def perform_update(self, serializer):
        from django.db import transaction
        from django.contrib.auth import get_user_model
        with transaction.atomic():
            get_user_model().objects.select_for_update().get(pk=self.request.user.pk)
            if serializer.validated_data.get("is_default"):
                self.get_queryset().exclude(pk=serializer.instance.pk).update(is_default=False)
            serializer.save()

    serializer_class = ResumeSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Resume.objects.filter(
            candidate=self.request.user
        )

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class ResumeDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        resume = get_object_or_404(Resume.objects.filter(Q(candidate=request.user) | Q(applications__job__recruiter=request.user)).distinct(), pk=pk)
        try:
            stream = resume.file.open("rb")
        except FileNotFoundError:
            raise Http404("Resume file is no longer available.")
        response = FileResponse(stream, as_attachment=True, filename="resume.pdf", content_type="application/pdf")
        response["Cache-Control"] = "private, no-store"
        return response
