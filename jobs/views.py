from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Job
from .serializers import JobSerializer
from .permissions import (
    IsAdminOrRecruiter,
    IsAllRoles,
)

from companies.models import Company


# =========================
# Create Job
# =========================

class JobCreateView(generics.CreateAPIView):

    serializer_class = JobSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def perform_create(self, serializer):

        # Admin selects company manually
        if self.request.user.role == "admin":

            company_id = self.request.data.get("company")

            company = get_object_or_404(
                Company,
                id=company_id
            )

            serializer.save(company=company)

        # Recruiter uses own company
        else:

            company = get_object_or_404(
                Company,
                user=self.request.user
            )

            serializer.save(company=company)


# =========================
# List Jobs
# =========================

class JobListView(generics.ListAPIView):

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated,
        IsAllRoles
    ]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        "title",
        "location",
        "skills_required",
    ]

    def get_queryset(self):

        # Admin & Placement Officer
        if self.request.user.role in ["admin", "officer"]:

            return Job.objects.filter(
                is_active=True
            )

        # Recruiter
        if self.request.user.role == "recruiter":

            company = get_object_or_404(
                Company,
                user=self.request.user
            )

            return Job.objects.filter(
                company=company,
                is_active=True
            )

        # Student
        return Job.objects.filter(
            status="published",
            is_active=True
        )


# =========================
# Job Detail
# =========================

class JobDetailView(generics.RetrieveAPIView):

    queryset = Job.objects.filter(
        is_active=True
    )

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated,
        IsAllRoles
    ]


# =========================
# Update Job
# =========================

class JobUpdateView(generics.UpdateAPIView):

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return Job.objects.filter(
                is_active=True
            )

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Job.objects.filter(
            company=company,
            is_active=True
        )


# =========================
# Delete Job (Soft Delete)
# =========================

class JobDeleteView(generics.DestroyAPIView):

    serializer_class = JobSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrRecruiter
    ]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return Job.objects.filter(
                is_active=True
            )

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Job.objects.filter(
            company=company,
            is_active=True
        )

    def perform_destroy(self, instance):

        instance.is_active = False

        instance.save()