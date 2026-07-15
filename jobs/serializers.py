from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.company_name",
        read_only=True
    )

    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_name",
            "title",
            "description",
            "requirements",
            "location",
            "salary_package",
            "job_type",
            "vacancies",
            "minimum_cgpa",
            "skills_required",
            "application_deadline",
            "status",
            "created_at",
            "applications_count",
        ]

        read_only_fields = [
            "company",
            "company_name",
            "applications_count",
        ]

    def get_applications_count(self, obj):

        return obj.applications.filter(
            is_active=True
        ).count()