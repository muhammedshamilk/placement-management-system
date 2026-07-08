from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from .permissions import IsAdminOrRecruiter
from django.shortcuts import get_object_or_404

# Create Job
from companies.models import Company


class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def perform_create(self, serializer):

        # Admin can choose company
        if self.request.user.role == "admin":

            company_id = self.request.data.get("company")

            company = Company.objects.get(id=company_id)

            serializer.save(company=company)

        # Recruiter automatically gets own company
        else:

            company = get_object_or_404(
                Company,
                user=self.request.user
            )

            serializer.save(company=company)


# List Jobs
from companies.models import Company

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "location",
        "skills_required"
    ]

    def get_queryset(self):

        # Admin sees all jobs
        if self.request.user.role == "admin":
            return Job.objects.filter(is_active=True)

        # Recruiter sees only own jobs
        elif self.request.user.role == "recruiter":
            try:
                company = Company.objects.get(user=self.request.user)
                return Job.objects.filter(
                    company=company,
                    is_active=True
                )
            except Company.DoesNotExist:
                return Job.objects.none()

        # Students see only published jobs
        return Job.objects.filter(
            status="published",
            is_active=True
        )


# Job Detail
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(
        is_active=True
    )

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]


# Update Job
from rest_framework.exceptions import PermissionDenied
from companies.models import Company

class JobUpdateView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Job.objects.filter(is_active=True)

        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            return Job.objects.none()

        return Job.objects.filter(
            company=company,
            is_active=True
        )


# Soft Delete Job
class JobDeleteView(generics.DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Job.objects.filter(is_active=True)

        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            return Job.objects.none()

        return Job.objects.filter(
            company=company,
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()