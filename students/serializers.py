from rest_framework import serializers
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    profile_completed = serializers.ReadOnlyField()

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    profile_photo = serializers.ImageField(
        required=False,
        allow_null=True
    )

    resume = serializers.FileField(
        required=False,
        allow_null=True
    )

    linkedin = serializers.URLField(
        required=True,
        allow_blank=True,
        allow_null=True
    )

    github = serializers.CharField(
        required=True,
        allow_blank=True,
        allow_null=True
    )

    portfolio = serializers.URLField(
        required=True,
        allow_blank=True,
        allow_null=True
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

            "profile_photo",

            "resume",

            "profile_completed",

        ]

        read_only_fields = [

            "id",

            "user",

            "username",

            "email",

        ]