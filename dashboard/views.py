from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin,IsOfficer,IsRecruiter, IsStudent

from students.models import StudentProfile
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from interviews.models import Interview
from accounts.models import User


class AdminDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        data = {

            "total_students": StudentProfile.objects.filter(
                is_active=True
            ).count(),

            "total_officers": User.objects.filter(
                role="officer",
                is_active=True
            ).count(),

            "total_recruiters": User.objects.filter(
                role="recruiter",
                is_active=True
            ).count(),

            "total_companies": Company.objects.filter(
                is_active=True
            ).count(),

            "total_jobs": Job.objects.filter(
                is_active=True
            ).count(),

            "active_jobs": Job.objects.filter(
                is_active=True,
                status="published"
            ).count(),

            "closed_jobs": Job.objects.filter(
                status="closed"
            ).count(),

            "total_applications": Application.objects.filter(
                is_active=True
            ).count(),

            "total_interviews": Interview.objects.filter(
                is_active=True
            ).count(),

            "selected_students": Application.objects.filter(
                status="selected",
                is_active=True
            ).count(),

            "rejected_students": Application.objects.filter(
                status="rejected",
                is_active=True
            ).count(),

        }

        return Response(data)




class OfficerDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsOfficer]

    def get(self, request):

        data = {

            "total_students": StudentProfile.objects.filter(
                is_active=True
            ).count(),

            "total_companies": Company.objects.filter(
                is_active=True
            ).count(),

            "total_jobs": Job.objects.filter(
                is_active=True
            ).count(),

            "active_jobs": Job.objects.filter(
                is_active=True,
                status="published"
            ).count(),

            "total_applications": Application.objects.filter(
                is_active=True
            ).count(),

            "total_interviews": Interview.objects.filter(
                is_active=True
            ).count(),

            "selected_students": Application.objects.filter(
                status="selected",
                is_active=True
            ).count(),

            "rejected_students": Application.objects.filter(
                status="rejected",
                is_active=True
            ).count(),

        }

        return Response(data)



class RecruiterDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request):

        company = Company.objects.get(user=request.user)

        jobs = Job.objects.filter(
            company=company,
            is_active=True
        )

        applications = Application.objects.filter(
            job__company=company,
            is_active=True
        )

        interviews = Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )

        data = {

            "company_name": company.company_name,

            "jobs_posted": jobs.count(),

            "active_jobs": jobs.filter(
                status="published"
            ).count(),

            "closed_jobs": jobs.filter(
                status="closed"
            ).count(),

            "applications_received": applications.count(),

            "shortlisted_candidates": applications.filter(
                status="shortlisted"
            ).count(),

            "interviews_scheduled": interviews.filter(
                status="scheduled"
            ).count(),

            "selected_candidates": applications.filter(
                status="selected"
            ).count(),
        }

        return Response(data)



class StudentDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):

        applications = Application.objects.filter(
            student=request.user,
            is_active=True
        )

        interviews = Interview.objects.filter(
            application__student=request.user,
            is_active=True
        )

        data = {

            "jobs_applied": applications.count(),

            "under_review": applications.filter(
                status="under_review"
            ).count(),

            "shortlisted": applications.filter(
                status="shortlisted"
            ).count(),

            "upcoming_interviews": interviews.filter(
                status="scheduled"
            ).count(),

            "selected_jobs": applications.filter(
                status="selected"
            ).count(),

            "rejected_jobs": applications.filter(
                status="rejected"
            ).count(),
        }

        return Response(data)