from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:

        model = Company

        fields = [
            "id",
            "username",
            "company_name",
            "industry",
            "website",
            "email",
            "phone",
            "address",
            "recruiter_name",
            "recruiter_designation",
            "logo",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "is_active",
            "created_at",
            "updated_at",
        ]