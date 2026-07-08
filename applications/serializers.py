from rest_framework import serializers
from .models import Application
from jobs.models import Job
from django.utils import timezone

from students.models import StudentProfile


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"

        read_only_fields = [
            "student",
            "status",
            "applied_at",
            "is_active"
        ]

        # Disable automatic unique_together validator
        validators = []

    def validate(self, attrs):

        request = self.context["request"]

        student = request.user
        job = attrs["job"]

        # Job closed
        if not job.is_active:
            raise serializers.ValidationError({
                "error": "This job is no longer accepting applications."
            })

        # Deadline validation
        if job.application_deadline < timezone.now().date():
            raise serializers.ValidationError({
                "error": "Application deadline has passed."
            })

        # Duplicate validation
        if Application.objects.filter(
                student=student,
                job=job,
                is_active=True
        ).exists():
            raise serializers.ValidationError({
                "error": "You have already applied for this job."
            })

        return attrs