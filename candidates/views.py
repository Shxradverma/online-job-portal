from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


class CandidateProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def perform_update(self, serializer):
        serializer.save()