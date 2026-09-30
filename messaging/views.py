from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from applications.models import Application
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)
    body = serializers.CharField(max_length=5000, allow_blank=False)
    class Meta:
        model = Message
        fields = ["id", "application", "sender", "sender_name", "body", "created_at"]
        read_only_fields = ["id", "application", "sender", "created_at"]

class ApplicationMessagesAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    def application(self):
        return get_object_or_404(Application.objects.filter(Q(candidate=self.request.user) | Q(job__recruiter=self.request.user)), pk=self.kwargs["pk"])
    def get_queryset(self):
        return Message.objects.filter(application=self.application()).select_related("sender")
    def perform_create(self, serializer):
        serializer.save(application=self.application(), sender=self.request.user)
