from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminRole


# Create Company
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# List + Search Companies
class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'company_name',
        'industry',
        'recruiter_name'
    ]

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


# Company Detail
class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Update Company
class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Soft Delete Company
class CompanyDeleteView(generics.DestroyAPIView):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def perform_destroy(self, instance):
        instance.soft_delete()