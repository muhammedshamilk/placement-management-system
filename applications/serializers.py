from rest_framework import serializers
from django.utils import timezone
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    # Student Details
    student_name = serializers.CharField(
        source="student.username",
        read_only=True
    )

    student_email = serializers.EmailField(
        source="student.email",
        read_only=True
    )

    # Job Details
    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.company_name",
        read_only=True
    )

    # Student Profile Details
    phone = serializers.CharField(
        source="student.studentprofile.phone",
        read_only=True
    )

    department = serializers.CharField(
        source="student.studentprofile.department",
        read_only=True
    )

    course = serializers.CharField(
        source="student.studentprofile.course",
        read_only=True
    )

    cgpa = serializers.DecimalField(
        source="student.studentprofile.cgpa",
        max_digits=4,
        decimal_places=2,
        read_only=True
    )

    skills = serializers.CharField(
        source="student.studentprofile.skills",
        read_only=True
    )

    linkedin = serializers.URLField(
        source="student.studentprofile.linkedin",
        read_only=True
    )

    github = serializers.URLField(
        source="student.studentprofile.github",
        read_only=True
    )

    portfolio = serializers.URLField(
        source="student.studentprofile.portfolio",
        read_only=True
    )

    profile_resume = serializers.FileField(
        source="student.studentprofile.resume",
        read_only=True
    )

    class Meta:

        model = Application

        fields = [
            "id",

            "student",
            "student_name",
            "student_email",

            "phone",
            "department",
            "course",
            "cgpa",
            "skills",
            "linkedin",
            "github",
            "portfolio",
            "profile_resume",

            "job",
            "job_title",
            "company_name",

            "resume",
            "cover_letter",

            "status",
            "applied_at",
            "is_active",
        ]

        read_only_fields = [
            "student",
            "student_name",
            "student_email",
            "phone",
            "department",
            "course",
            "cgpa",
            "skills",
            "linkedin",
            "github",
            "portfolio",
            "profile_resume",
            "job_title",
            "company_name",
            "applied_at",
            "is_active",
        ]
        # Disable automatic unique validator
        validators = []

    def validate(self, attrs):

        # Skip create validation during update
        if self.instance:
            return attrs

        request = self.context["request"]

        student = request.user
        job = attrs["job"]

        # Job must be active
        if not job.is_active:
            raise serializers.ValidationError({
                "error": "This job is no longer accepting applications."
            })

        # Deadline check
        if job.application_deadline < timezone.now().date():
            raise serializers.ValidationError({
                "error": "Application deadline has passed."
            })

        # Duplicate application check
        if Application.objects.filter(
                student=student,
                job=job,
                is_active=True
        ).exists():
            raise serializers.ValidationError({
                "error": "You have already applied for this job."
            })

        return attrs

