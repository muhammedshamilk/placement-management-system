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
from rest_framework import status

from applications.serializers import ApplicationSerializer

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

            # 👇 Add this
            "pending_applications": Application.objects.filter(
                status="pending",
                is_active=True
            ).count(),

            "total_interviews": Interview.objects.filter(
                is_active=True
            ).count(),

            # 👇 Add this
            "scheduled_interviews": Interview.objects.filter(
                status="scheduled",
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

            "pending_applications": Application.objects.filter(
                status="pending",
                is_active=True
            ).count(),

            "scheduled_interviews": Interview.objects.filter(
                status="scheduled",
                is_active=True
            ).count(),
        }

        return Response(data)



class RecruiterDashboardView(APIView):

    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request):

        try:

            company, created = Company.objects.get_or_create(

                user=request.user,

                defaults={

                    "company_name": "",

                    "industry": "",

                    "website": "",

                    "email": request.user.email,

                    "phone": "",

                    "address": "",

                    "recruiter_name": request.user.username,

                    "recruiter_designation": "",

                    "description": "",

                }

            )

        except Company.DoesNotExist:

            return Response(
                {
                    "error": "Company profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

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
            "logo": request.build_absolute_uri(company.logo.url) if company.logo else None,
            "jobs_posted": jobs.count(),

            "active_jobs": jobs.filter(
                status="published"
            ).count(),

            "closed_jobs": jobs.filter(
                status="closed"
            ).count(),

            "applications_received": applications.count(),

            "pending_applications": applications.filter(
                status="pending"
            ).count(),

            "under_review": applications.filter(
                status="under_review"
            ).count(),

            "shortlisted_candidates": applications.filter(
                status="shortlisted"
            ).count(),

            "interviews_scheduled": interviews.filter(
                status="scheduled"
            ).count(),

            "selected_candidates": applications.filter(
                status="selected"
            ).count(),

            "rejected_candidates": applications.filter(
                status="rejected"
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

from rest_framework import generics

class RecentApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return (
            Application.objects
                .filter(is_active=True)
                .order_by("-created_at")[:5]
         )
