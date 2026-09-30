from django.db import models

class Interview(models.Model):
    application = models.ForeignKey("applications.Application", on_delete=models.CASCADE, related_name="interviews")
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    meeting_url = models.URLField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    notes = models.TextField(blank=True, max_length=5000)
    status = models.CharField(max_length=20, choices=[("SCHEDULED","Scheduled"),("COMPLETED","Completed"),("CANCELLED","Cancelled")], default="SCHEDULED")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["scheduled_at"]
