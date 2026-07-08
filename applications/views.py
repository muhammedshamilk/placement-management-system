from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsStudent, IsAdminOrRecruiter
from companies.models import Company
from students.models import StudentProfile

class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Application.objects.filter(
            student=self.request.user,
            is_active=True
        )




# Student applies for a job

class ApplyJobView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


# Student views own applications





# Admin/Recruiter view all applications


class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Application.objects.filter(is_active=True)

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Application.objects.filter(
            job__company=company,
            is_active=True
        )


# View single application
class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Application.objects.filter(is_active=True)

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Application.objects.filter(
            job__company=company,
            is_active=True
        )


# Update status
class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Application.objects.filter(is_active=True)

        company = get_object_or_404(
            Company,
            user=self.request.user
        )

        return Application.objects.filter(
            job__company=company,
            is_active=True
        )


# Soft delete application
class ApplicationDeleteView(generics.DestroyAPIView):
    queryset = Application.objects.filter(is_active=True)
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()