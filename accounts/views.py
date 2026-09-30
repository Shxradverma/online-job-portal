from django.db import transaction, IntegrityError
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from candidates.models import CandidateProfile
from .serializers import RegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                user = serializer.save()
                if user.role == "CANDIDATE":
                    CandidateProfile.objects.create(user=user)
        except IntegrityError:
            raise serializers.ValidationError("Username or email already exists.")

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({"id":user.id,"username":user.username,"email":user.email,"role":user.role})
