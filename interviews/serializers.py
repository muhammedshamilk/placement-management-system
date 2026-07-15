from rest_framework import serializers
from django.utils import timezone
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    # IDs
    student = serializers.IntegerField(
        source="application.student.id",
        read_only=True
    )

    job = serializers.IntegerField(
        source="application.job.id",
        read_only=True
    )

    # Student
    student_name = serializers.CharField(
        source="application.student.username",
        read_only=True
    )

    student_email = serializers.EmailField(
        source="application.student.email",
        read_only=True
    )

    # Job
    job_title = serializers.CharField(
        source="application.job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="application.job.company.company_name",
        read_only=True
    )

    class Meta:

        model = Interview

        fields = [

            "id",

            "application",

            "student",
            "job",

            "student_name",
            "student_email",

            "job_title",
            "company_name",

            "interview_date",
            "interview_time",
            "interview_mode",
            "interview_location",
            "interviewer_name",

            "notes",

            "status",
            "result",

            "feedback",

            "created_at",
            "updated_at",
            "is_active",
        ]

        read_only_fields = [

            "application",

            "student",
            "job",

            "student_name",
            "student_email",

            "job_title",
            "company_name",

            "created_at",
            "updated_at",
            "is_active",
        ]

        validators = []

    def validate(self, attrs):

        interview_date = attrs.get("interview_date")

        if interview_date and interview_date < timezone.now().date():

            raise serializers.ValidationError({

                "error": "Interview date cannot be in the past."

            })

        return attrs