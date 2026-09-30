"""Core regression suite. Run: python manage.py test."""
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APITestCase
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from resumes.models import Resume
from candidates.models import CandidateProfile
from ai_matching.services import calculate_job_match

@override_settings(SECURE_SSL_REDIRECT=False, STORAGES={"default":{"BACKEND":"django.core.files.storage.InMemoryStorage"},"staticfiles":{"BACKEND":"django.contrib.staticfiles.storage.StaticFilesStorage"}}, REST_FRAMEWORK={"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework_simplejwt.authentication.JWTAuthentication"],"DEFAULT_THROTTLE_RATES":{"anon":"1000/minute","user":"1000/minute","login":"1000/minute"}})
class PortalTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.candidate = User.objects.create_user(username="candidate", email="candidate@example.com", password="Test-password-476", role="CANDIDATE")
        self.other = User.objects.create_user(username="other", email="other@example.com", password="Test-password-476", role="CANDIDATE")
        self.recruiter = User.objects.create_user(username="recruiter", email="recruiter@example.com", password="Test-password-476", role="RECRUITER")
        self.other_recruiter = User.objects.create_user(username="recruiter2", email="recruiter2@example.com", password="Test-password-476", role="RECRUITER")
        self.company = Company.objects.create(name="Test Company", created_by=self.recruiter)
        self.job = Job.objects.create(company=self.company, recruiter=self.recruiter, title="Django Developer", description="Build web applications", status="PUBLISHED", skills="Python,Django")
    def auth(self, user): self.client.force_authenticate(user)
    def apply(self, **extra):
        return self.client.post('/api/applications/apply/', {"job":self.job.pk, **extra}, format='json')
    def test_public_job_and_pages(self):
        self.assertEqual(self.client.get('/api/jobs/').status_code,200)
        for url in ['/', '/login/', '/register/', '/dashboard/', '/jobs/%s/'%self.job.pk, '/password-reset/']:
            self.assertEqual(self.client.get(url).status_code,200, url)
    def test_invalid_salary_returns_400(self):
        self.assertEqual(self.client.get('/api/jobs/?salary_min=abc').status_code,400)
    def test_draft_job_is_private(self):
        self.job.status='DRAFT';self.job.save()
        self.assertEqual(self.client.get('/api/jobs/%s/'%self.job.pk).status_code,404)
    def test_expired_job_is_excluded(self):
        self.job.application_deadline=timezone.localdate()-timedelta(days=1);self.job.save()
        self.assertEqual(self.client.get('/api/jobs/').data['count'],0)
        self.auth(self.candidate);self.assertEqual(self.apply().status_code,400)
    def test_register_candidate(self):
        r=self.client.post('/api/auth/register/',{'username':'newuser','email':'new@example.com','password':'Strong-new-password-846','role':'CANDIDATE'})
        self.assertEqual(r.status_code,201,r.data)
        self.assertNotIn('password',r.data)
        self.assertTrue(CandidateProfile.objects.filter(user_id=r.data['id']).exists())
    def test_register_cannot_create_admin(self):
        r=self.client.post('/api/auth/register/',{'username':'baduser','email':'bad@example.com','password':'Strong-password-846','role':'ADMIN'})
        self.assertEqual(r.status_code,400)
    def test_weak_password_rejected(self):
        r=self.client.post('/api/auth/register/',{'username':'weak','email':'weak@example.com','password':'123','role':'CANDIDATE'})
        self.assertEqual(r.status_code,400)
    def test_jwt_login_refresh(self):
        r=self.client.post('/api/auth/token/',{'username':'candidate','password':'Test-password-476'})
        self.assertEqual(r.status_code,200)
        self.assertEqual(self.client.post('/api/auth/token/refresh/',{'refresh':r.data['refresh']}).status_code,200)
    def test_candidate_cannot_create_jobs(self):
        self.auth(self.candidate)
        self.assertEqual(self.client.post('/api/recruiter/jobs/',{}).status_code,403)
    def test_recruiter_cannot_apply(self):
        self.auth(self.recruiter);self.assertEqual(self.apply().status_code,403)
    def test_apply_status_is_always_applied(self):
        self.auth(self.candidate);r=self.apply(status='HIRED')
        self.assertEqual(r.status_code,201,r.data)
        self.assertEqual(r.data['status'],'APPLIED')
        self.job.refresh_from_db();self.assertEqual(self.job.applications_count,1)
    def test_duplicate_application_does_not_increment_counter(self):
        self.auth(self.candidate);self.apply()
        self.assertEqual(self.apply().status_code,400)
        self.job.refresh_from_db();self.assertEqual(self.job.applications_count,1)
    def test_foreign_resume_rejected(self):
        resume=Resume.objects.create(candidate=self.other,file='resumes/private.pdf')
        self.auth(self.candidate);self.assertEqual(self.apply(resume=resume.pk).status_code,400)
    def test_candidate_cannot_read_other_application(self):
        a=Application.objects.create(candidate=self.other,job=self.job)
        self.auth(self.candidate);self.assertEqual(self.client.get('/api/applications/%s/'%a.pk).status_code,404)
    def test_withdraw_cannot_reassign_job(self):
        a=Application.objects.create(candidate=self.candidate,job=self.job)
        other_job=Job.objects.create(company=self.company,recruiter=self.recruiter,title='Other',description='Other',status='PUBLISHED')
        self.auth(self.candidate)
        self.assertEqual(self.client.patch('/api/applications/%s/withdraw/'%a.pk,{'job':other_job.pk},format='json').status_code,200)
        a.refresh_from_db();self.assertEqual(a.job_id,self.job.pk);self.assertEqual(a.status,'WITHDRAWN')
    def test_recruiter_can_update_only_own_applicant(self):
        a=Application.objects.create(candidate=self.candidate,job=self.job)
        self.auth(self.other_recruiter)
        self.assertEqual(self.client.patch('/api/applications/%s/status/'%a.pk,{'status':'HIRED'}).status_code,404)
        self.auth(self.recruiter)
        self.assertEqual(self.client.patch('/api/applications/%s/status/'%a.pk,{'status':'SHORTLISTED'}).status_code,200)
    def test_withdrawn_application_cannot_be_reopened(self):
        a=Application.objects.create(candidate=self.candidate,job=self.job,status='WITHDRAWN')
        self.auth(self.recruiter)
        self.assertEqual(self.client.patch('/api/applications/%s/status/'%a.pk,{'status':'HIRED'}).status_code,400)
    def test_recruiter_cannot_modify_foreign_job(self):
        self.auth(self.other_recruiter)
        self.assertEqual(self.client.patch('/api/recruiter/jobs/%s/'%self.job.pk,{'title':'Changed'}).status_code,404)
    def test_recruiter_cannot_post_under_foreign_company(self):
        self.auth(self.other_recruiter)
        r=self.client.post('/api/recruiter/jobs/',{'company':self.company.pk,'title':'Test','description':'Test'})
        self.assertEqual(r.status_code,400)
    def test_job_salary_validation(self):
        self.auth(self.recruiter)
        r=self.client.patch('/api/recruiter/jobs/%s/'%self.job.pk,{'salary_min':100,'salary_max':50})
        self.assertEqual(r.status_code,400)
    def test_save_is_idempotent_and_private(self):
        self.auth(self.candidate)
        self.assertEqual(self.client.post('/api/jobs/save/',{'job':self.job.pk}).status_code,201)
        self.assertEqual(self.client.post('/api/jobs/save/',{'job':self.job.pk}).status_code,200)
        self.auth(self.other);self.assertEqual(len(self.client.get('/api/jobs/saved/').data),0)
    def test_bad_job_id_is_client_error(self):
        self.auth(self.candidate)
        self.assertEqual(self.client.post('/api/jobs/save/',{'job':'oops'}).status_code,404)
    def test_resume_upload_and_private_download(self):
        self.auth(self.candidate)
        r=self.client.post('/api/resumes/',{'title':'CV','file':SimpleUploadedFile('cv.pdf',b'%PDF-1.4\n%%EOF',content_type='application/pdf')},format='multipart')
        self.assertEqual(r.status_code,201,r.data)
        url=r.data['file'];self.assertEqual(self.client.get(url).status_code,200)
        self.auth(self.other);self.assertEqual(self.client.get(url).status_code,404)
        self.auth(self.recruiter);self.assertEqual(self.client.get(url).status_code,404)
        Application.objects.create(candidate=self.candidate,job=self.job,resume_id=r.data['id'])
        self.assertEqual(self.client.get(url).status_code,200)
    def test_resume_rejects_fake_pdf(self):
        self.auth(self.candidate)
        r=self.client.post('/api/resumes/',{'file':SimpleUploadedFile('cv.pdf',b'<html>bad</html>')},format='multipart')
        self.assertEqual(r.status_code,400)
    def test_recruiter_notes_not_exposed_to_candidate(self):
        Application.objects.create(candidate=self.candidate,job=self.job,recruiter_notes='Private')
        self.auth(self.candidate)
        self.assertNotIn('recruiter_notes',self.client.get('/api/applications/my/').data[0])
    def test_profile_completion(self):
        self.auth(self.candidate)
        r=self.client.patch('/api/candidates/profile/',{'headline':'Developer','bio':'Building software','skills':'Python','location':'Delhi'})
        self.assertEqual(r.status_code,200)
        self.assertTrue(CandidateProfile.objects.get(user=self.candidate).is_profile_complete)
    def test_skill_match_is_deterministic(self):
        profile=CandidateProfile.objects.create(user=self.candidate,skills=' python, SQL ')
        score=calculate_job_match(profile,self.job)
        self.assertEqual(score['score'],50)
        self.assertEqual(score['matched_skills'],['python'])
        self.assertEqual(score['missing_skills'],['django'])
    def test_application_messages_are_private(self):
        a=Application.objects.create(candidate=self.candidate,job=self.job)
        url='/api/applications/%s/messages/'%a.pk
        self.auth(self.candidate)
        self.assertEqual(self.client.post(url,{'body':'Hello recruiter'}).status_code,201)
        self.auth(self.recruiter)
        self.assertEqual(self.client.get(url).data[0]['body'],'Hello recruiter')
        self.auth(self.other)
        self.assertEqual(self.client.get(url).status_code,404)
        self.assertEqual(self.client.post(url,{'body':'Unauthorized'}).status_code,404)
    def test_interview_permissions(self):
        a=Application.objects.create(candidate=self.candidate,job=self.job)
        url='/api/applications/%s/interviews/'%a.pk
        payload={'scheduled_at':(timezone.now()+timedelta(days=1)).isoformat(),'duration_minutes':30,'location':'Office'}
        self.auth(self.candidate)
        self.assertEqual(self.client.post(url,payload).status_code,403)
        self.auth(self.recruiter)
        response=self.client.post(url,payload)
        self.assertEqual(response.status_code,201,response.data)
        self.auth(self.candidate)
        self.assertEqual(len(self.client.get(url).data),1)
        self.auth(self.other)
        self.assertEqual(self.client.get(url).status_code,404)
        self.auth(self.recruiter)
        self.assertEqual(self.client.patch('/api/interviews/%s/'%response.data['id'],{'status':'CANCELLED'}).status_code,200)
    def test_analytics_and_activity_are_scoped(self):
        Application.objects.create(candidate=self.candidate,job=self.job)
        self.auth(self.other)
        self.assertEqual(self.client.get('/api/analytics/').data['applications'],0)
        self.assertEqual(self.client.get('/api/notifications/').data,[])
        self.auth(self.recruiter)
        self.assertEqual(self.client.get('/api/analytics/').data['applications'],1)
        self.assertEqual(len(self.client.get('/api/notifications/').data),1)
    def test_password_reset_sends_email_and_changes_password(self):
        import re
        from django.core import mail
        response=self.client.post('/password-reset/', {'email':self.candidate.email})
        self.assertEqual(response.status_code,302)
        self.assertEqual(len(mail.outbox),1)
        path=re.search(r'http://testserver(/reset/[^\s]+)',mail.outbox[0].body).group(1)
        confirmation=self.client.get(path)
        self.assertEqual(confirmation.status_code,302)
        result=self.client.post(confirmation.url,{'new_password1':'A-new-strong-password-582','new_password2':'A-new-strong-password-582'})
        self.assertEqual(result.status_code,302)
        self.candidate.refresh_from_db();self.assertTrue(self.candidate.check_password('A-new-strong-password-582'))
    def test_only_one_default_resume(self):
        self.auth(self.candidate)
        for number in [1,2]:
            response=self.client.post('/api/resumes/',{'title':str(number),'is_default':True,'file':SimpleUploadedFile('cv.pdf',b'%PDF-1.4\n%%EOF')},format='multipart')
            self.assertEqual(response.status_code,201,response.data)
        self.assertEqual(Resume.objects.filter(candidate=self.candidate,is_default=True).count(),1)
