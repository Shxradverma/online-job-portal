from rest_framework import generics
from accounts.permissions import IsCandidate

from .models import CandidateProfile
from .serializers import CandidateProfileSerializer


class CandidateProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsCandidate]

    def get_object(self):
        profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def perform_update(self, serializer):
        profile = serializer.save()
        profile.is_profile_complete = bool(profile.headline and profile.skills and profile.location and profile.bio)
        profile.save(update_fields=["is_profile_complete"])