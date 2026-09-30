from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from applications.models import Application
from interviews.models import Interview
from messaging.models import Message

class ActivityAPIView(APIView):
    """A recent activity feed; this is not an email/push delivery system."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        own = Q(candidate=request.user)|Q(job__recruiter=request.user)
        applications = Application.objects.filter(own)
        rows = [{"type":"application", "application":a.pk, "text":a.job.title+": "+a.get_status_display(), "at":a.updated_at} for a in applications.select_related("job").order_by("-updated_at")[:20]]
        for item in Interview.objects.filter(application__in=applications).select_related("application__job").order_by("-updated_at")[:20]:
            rows.append({"type":"interview", "application":item.application_id, "text":item.application.job.title+": interview "+item.status.lower(), "at":item.updated_at})
        for item in Message.objects.filter(application__in=applications).exclude(sender=request.user).select_related("sender").order_by("-created_at")[:20]:
            rows.append({"type":"message", "application":item.application_id, "text":"New message from "+item.sender.username, "at":item.created_at})
        return Response(sorted(rows, key=lambda row:row["at"], reverse=True)[:30])
