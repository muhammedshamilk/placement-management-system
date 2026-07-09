from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = StudentProfile

        fields = [
            "id",
            "user",
            "username",
            "email",
            "phone",
            "gender",
            "dob",
            "department",
            "course",
            "academic_year",
            "cgpa",
            "skills",
            "linkedin",
            "github",
            "portfolio",
            "resume",
            "is_active",
            "created_at",
            "updated_at",
        ]