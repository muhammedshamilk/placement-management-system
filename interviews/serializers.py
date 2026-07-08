from rest_framework import serializers
from django.utils import timezone
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = "__all__"

        read_only_fields = [
            "created_at",
            "updated_at",
            "is_active",
        ]

        validators = []

    def validate(self, attrs):

        application = attrs["application"]

        # Prevent duplicate interview
        if Interview.objects.filter(
            application=application,
            is_active=True
        ).exists():

            raise serializers.ValidationError({
                "error": "Interview already scheduled for this application."
            })

        # Prevent past interview dates
        if attrs["interview_date"] < timezone.now().date():
            raise serializers.ValidationError({
                "error": "Interview date cannot be in the past."
            })

        return attrs