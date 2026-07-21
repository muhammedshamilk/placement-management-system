from rest_framework import generics, filters, serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from .permissions import (
    IsAdminRole,
    IsRecruiter,
    IsAdminOrOfficer,
)


# =========================
# Create Company (Recruiter)
# =========================

class CompanyCreateView(generics.CreateAPIView):

    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
        IsRecruiter
    ]

    def perform_create(self, serializer):

        if Company.objects.filter(
            user=self.request.user,
            is_active=True
        ).exists():

            raise serializers.ValidationError({
                "error": "Company profile already exists."
            })

        serializer.save(
            user=self.request.user
        )


# =========================
# Company List (Admin/Officer)
# =========================

class CompanyListView(generics.ListAPIView):

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrOfficer
    ]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        "company_name",
        "industry",
        "recruiter_name",
    ]

    def get_queryset(self):

        return Company.objects.filter(
            is_active=True
        )


# =========================
# Company Detail (Admin/Officer)
# =========================

class CompanyDetailView(generics.RetrieveAPIView):

    queryset = Company.objects.filter(
        is_active=True
    )

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminOrOfficer
    ]


# =========================
# Update Company (Admin)
# =========================

class CompanyUpdateView(generics.UpdateAPIView):

    queryset = Company.objects.filter(
        is_active=True
    )

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminRole
    ]


# =========================
# Delete Company (Admin)
# =========================

class CompanyDeleteView(generics.DestroyAPIView):

    queryset = Company.objects.filter(
        is_active=True
    )

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsAdminRole
    ]

    def perform_destroy(self, instance):

        instance.soft_delete()


# =========================
# Recruiter - My Company
# =========================

class MyCompanyView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsRecruiter
    ]

    def get(self, request):

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

        serializer = CompanySerializer(company)

        return Response(serializer.data)
# =========================
# Recruiter - Update My Company
# =========================

from django.shortcuts import get_object_or_404

class MyCompanyUpdateView(generics.UpdateAPIView):

    serializer_class = CompanySerializer

    permission_classes = [
        IsAuthenticated,
        IsRecruiter
    ]

    def get_object(self):

        return get_object_or_404(
            Company,
            user=self.request.user,
            is_active=True
        )

    def update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return super().update(request, *args, **kwargs)