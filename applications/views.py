from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from notifications.utils import create_notification

from django.shortcuts import get_object_or_404

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import (
    IsStudent,
    IsAdminOrRecruiter,
    IsAdminRecruiterOfficer,
)

from companies.models import Company
from jobs.models import Job


# =========================
# Student - My Applications
# =========================

class MyApplicationsView(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):

        return Application.objects.filter(
            student=self.request.user,
            is_active=True
        )


# =========================
# Student - Apply Job
# =========================

class ApplyJobView(generics.CreateAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):

        serializer.save(student=self.request.user)


# =========================
# Admin / Recruiter / Officer
# =========================

class ApplicationListView(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminRecruiterOfficer
    ]

    def get_queryset(self):

        # Admin & Officer
        if self.request.user.role in ["admin", "officer"]:

            return Application.objects.filter(
                is_active=True
            )

        # Recruiter
        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Application.objects.filter(
            job__company=company,
            is_active=True
        )


# =========================
# View Single Application
# =========================

class ApplicationDetailView(generics.RetrieveAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminRecruiterOfficer
    ]

    def get_queryset(self):

        if self.request.user.role in ["admin", "officer"]:

            return Application.objects.filter(
                is_active=True
            )

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Application.objects.filter(
            job__company=company,
            is_active=True
        )


# =========================
# Recruiter/Admin Update Status
# =========================

class ApplicationUpdateView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def patch(self, request, pk):

        application = get_object_or_404(
            Application,
            pk=pk,
            is_active=True
        )

        status = request.data.get(
            "status",
            application.status
        )

        application.status = status
        application.save()

        # -----------------------------
        # Notifications
        # -----------------------------

        if status == "under_review":

            create_notification(

                user=application.student,

                title="Application Under Review",

                message=f"Your application for '{application.job.title}' is under review."

            )

        elif status == "shortlisted":

            create_notification(

                user=application.student,

                title="Application Shortlisted",

                message=f"Congratulations! You have been shortlisted for '{application.job.title}'."

            )

        elif status == "rejected":

            create_notification(

                user=application.student,

                title="Application Rejected",

                message=f"Your application for '{application.job.title}' was not selected."

            )

        serializer = ApplicationSerializer(application)

        return Response(serializer.data)
# =========================
# Soft Delete
# =========================

class ApplicationDeleteView(generics.DestroyAPIView):

    queryset = Application.objects.filter(
        is_active=True
    )

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def perform_destroy(self, instance):

        instance.is_active = False

        instance.save()


# =========================
# Check Already Applied
# =========================

class CheckApplicationView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    def get(self, request, job_id):

        applied = Application.objects.filter(
            student=request.user,
            job_id=job_id,
            is_active=True
        ).exists()

        return Response({

            "applied": applied

        })


# =========================
# Applications of One Job
# =========================

class JobApplicationListView(generics.ListAPIView):

    serializer_class = ApplicationSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminRecruiterOfficer
    ]

    def get_queryset(self):

        job = get_object_or_404(
            Job,
            id=self.kwargs["job_id"]
        )

        # Admin & Placement Officer
        if self.request.user.role in ["admin", "officer"]:

            return Application.objects.filter(
                job=job,
                is_active=True
            )

        # Recruiter
        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        if job.company != company:

            raise PermissionDenied(
                "You cannot view applications for another company's job."
            )

        return Application.objects.filter(
            job=job,
            is_active=True
        )