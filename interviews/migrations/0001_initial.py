from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("applications", "0002_remove_application_unique_job_candidate_application_and_more")]
    operations = [migrations.CreateModel(name="Interview",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("scheduled_at",models.DateTimeField()),
        ("duration_minutes",models.PositiveIntegerField(default=30)),
        ("meeting_url",models.URLField(blank=True)),
        ("location",models.CharField(blank=True,max_length=250)),
        ("notes",models.TextField(blank=True,max_length=5000)),
        ("status",models.CharField(choices=[("SCHEDULED","Scheduled"),("COMPLETED","Completed"),("CANCELLED","Cancelled")],default="SCHEDULED",max_length=20)),
        ("created_at",models.DateTimeField(auto_now_add=True)),
        ("updated_at",models.DateTimeField(auto_now=True)),
        ("application",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="interviews",to="applications.application")),
    ],options={"ordering":["scheduled_at"]})]
