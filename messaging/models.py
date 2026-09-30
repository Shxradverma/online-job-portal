from django.conf import settings
from django.db import models

class Message(models.Model):
    application = models.ForeignKey("applications.Application", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at", "id"]
