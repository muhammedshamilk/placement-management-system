from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_notification
from .models import Interview
from .serializers import InterviewSerializer
from .permissions import (
    IsAdminOrRecruiter,
    IsAdminRecruiterOfficer,
    IsStudent,
)
from django.shortcuts import get_object_or_404

# Create Interview
from applications.models import Application
from companies.models import Company
from rest_framework.exceptions import PermissionDenied

class InterviewCreateView(generics.CreateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def perform_create(self, serializer):

        application_id = self.request.data.get("application")



        application = get_object_or_404(
            Application,
            id=application_id
        )
        # Already scheduled?

        if Interview.objects.filter(

                application=application,

                is_active=True

        ).exists():
            raise PermissionDenied(

                "Interview already scheduled for this application."

            )

        if application.status == "rejected":
            raise PermissionDenied(
                "Rejected applications cannot be scheduled."
            )

        if application.status != "shortlisted":
            raise PermissionDenied(
                "Only shortlisted applications can be scheduled."
            )



        # Admin
        # Admin
        if self.request.user.role == "admin":


            serializer.save(application=application)

            application.status = "interview_scheduled"
            application.save()

            create_notification(

                user=application.student,

                title="Interview Scheduled",

                message=(
                    f"Your interview for '{application.job.title}' "
                    f"has been scheduled on "
                    f"{serializer.instance.interview_date} "
                    f"at {serializer.instance.interview_time}."
                )

            )

            return

        # Recruiter
        company = Company.objects.get(user=self.request.user)

        if application.job.company != company:
            raise PermissionDenied(
                "You cannot schedule interviews for another company's applications."
            )

        serializer.save(application=application)

        application.status = "interview_scheduled"
        application.save()

        create_notification(

            user=application.student,

            title="Interview Scheduled",

            message=(
                f"Your interview for '{application.job.title}' "
                f"has been scheduled on "
                f"{serializer.instance.interview_date} "
                f"at {serializer.instance.interview_time}."
            )

        )


# List Interviews
from companies.models import Company

class InterviewListView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminRecruiterOfficer
    ]

    def get_queryset(self):

        # Admin & Placement Officer
        if self.request.user.role in ["admin", "officer"]:
            return Interview.objects.filter(
                is_active=True
            )

        # Recruiter
        try:

            company = Company.objects.get(
                user=self.request.user
            )

        except Company.DoesNotExist:

            return Interview.objects.none()

        return Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )


# Interview Detail
class InterviewDetailView(generics.RetrieveAPIView):

    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        # Admin & Officer
        if self.request.user.role in ["admin", "officer"]:

            return Interview.objects.filter(
                is_active=True
            )

        # Recruiter
        elif self.request.user.role == "recruiter":

            try:

                company = Company.objects.get(
                    user=self.request.user
                )

            except Company.DoesNotExist:

                return Interview.objects.none()

            return Interview.objects.filter(
                application__job__company=company,
                is_active=True
            )

        # Student
        elif self.request.user.role == "student":

            return Interview.objects.filter(
                application__student=self.request.user,
                is_active=True
            )

        return Interview.objects.none()
# Update Interview
class InterviewUpdateView(generics.UpdateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Interview.objects.filter(is_active=True)

        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            return Interview.objects.none()

        return Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )

class InterviewUpdateView(generics.UpdateAPIView):

    serializer_class = InterviewSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return Interview.objects.filter(
                is_active=True
            )

        try:

            company = Company.objects.get(
                user=self.request.user
            )

        except Company.DoesNotExist:

            return Interview.objects.none()

        return Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )

    def update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return super().update(request, *args, **kwargs)


# Update Interview Result
class InterviewResultUpdateView(generics.UpdateAPIView):

    serializer_class = InterviewSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return Interview.objects.filter(
                is_active=True
            )

        try:

            company = Company.objects.get(
                user=self.request.user
            )

        except Company.DoesNotExist:

            return Interview.objects.none()

        return Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )

    def update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):

        interview = serializer.save()

        application = interview.application

        if interview.result == "selected":

            application.status = "selected"

            create_notification(

                user=application.student,

                title="Congratulations!",

                message=(
                    f"You have been selected for "
                    f"'{application.job.title}'."
                )

            )

        elif interview.result == "rejected":

            application.status = "rejected"

            create_notification(

                user=application.student,

                title="Interview Result",

                message=(
                    f"Unfortunately, you were not selected for "
                    f"'{application.job.title}'."
                )

            )

        elif interview.status == "scheduled":

            application.status = "interview_scheduled"

        application.save()

# Soft Delete Interview
class InterviewDeleteView(generics.DestroyAPIView):

    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Interview.objects.filter(is_active=True)

        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            return Interview.objects.none()

        return Interview.objects.filter(
            application__job__company=company,
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# Student - My Interviews
class MyInterviewView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Interview.objects.filter(
            application__student=self.request.user,
            is_active=True
        )



