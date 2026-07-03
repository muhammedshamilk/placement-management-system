from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsStudent, IsAdminOrRecruiter


# Student applies for a job
class ApplyJobView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]


# Student views own applications
class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Application.objects.filter(
            student=self.request.user,
            is_active=True
        )


# Admin/Recruiter view all applications
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def get_queryset(self):
        return Application.objects.filter(
            is_active=True
        )


# View single application
class ApplicationDetailView(generics.RetrieveAPIView):
    queryset = Application.objects.filter(is_active=True)
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]


# Update status
class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.filter(is_active=True)
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]


# Soft delete application
class ApplicationDeleteView(generics.DestroyAPIView):
    queryset = Application.objects.filter(is_active=True)
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()