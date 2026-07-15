from rest_framework import serializers

from .models import OfferLetter


class OfferLetterSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="application.student.username",
        read_only=True
    )

    company_name = serializers.CharField(
        source="application.job.company.company_name",
        read_only=True
    )

    job_title = serializers.CharField(
        source="application.job.title",
        read_only=True
    )

    class Meta:

        model = OfferLetter

        fields = [

            "id",

            "application",

            "student_name",

            "company_name",

            "job_title",

            "offer_letter",

            "offer_date",

            "joining_date",

            "status",

            "created_at"

        ]