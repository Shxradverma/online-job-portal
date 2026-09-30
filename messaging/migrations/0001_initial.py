from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("applications", "0002_remove_application_unique_job_candidate_application_and_more"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Message", fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("body",models.TextField(max_length=5000)),
        ("created_at",models.DateTimeField(auto_now_add=True)),
        ("application",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="messages",to="applications.application")),
        ("sender",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,to=settings.AUTH_USER_MODEL)),
    ],options={"ordering":["created_at","id"]})]
