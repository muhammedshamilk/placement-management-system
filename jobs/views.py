from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from .permissions import IsAdminOrRecruiter


# Create Job
class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRecruiter]


# List Jobs
class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        'title',
        'location',
        'skills_required'
    ]

    def get_queryset(self):
        return Job.objects.filter(
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
class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.filter(
        is_active=True
    )

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,
                          IsAdminOrRecruiter]


# Soft Delete Job
class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.filter(
        is_active=True
    )

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,
                          IsAdminOrRecruiter]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()