from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification
from .models import OfferLetter
from .serializers import OfferLetterSerializer

from applications.models import Application
from companies.models import Company

from .permissions import (
    IsRecruiterOrAdmin,
    IsStudent,
)


class OfferLetterCreateView(generics.CreateAPIView):

    serializer_class = OfferLetterSerializer

    permission_classes = [
        IsAuthenticated,
        IsRecruiterOrAdmin
    ]

    def perform_create(self, serializer):

        application = get_object_or_404(
            Application,
            id=self.request.data.get("application")
        )

        if application.status != "selected":

            raise PermissionDenied(
                "Offer letters can only be uploaded for selected students."
            )

        if OfferLetter.objects.filter(
            application=application
        ).exists():

            raise PermissionDenied(
                "Offer letter already uploaded."
            )

        if self.request.user.role == "recruiter":

            company = Company.objects.get(
                user=self.request.user
            )

            if application.job.company != company:

                raise PermissionDenied(
                    "You cannot upload offers for another company."
                )

        offer = serializer.save(
            application=application
        )

        create_notification(

            user=application.student,

            title="Offer Letter Received",

            message=(
                f"You have received an offer letter "
                f"from {application.job.company.company_name} "
                f"for the position of "
                f"'{application.job.title}'."
            )

        )

class OfferLetterListView(generics.ListAPIView):

    serializer_class = OfferLetterSerializer

    permission_classes = [
        IsAuthenticated,
        IsRecruiterOrAdmin
    ]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return OfferLetter.objects.filter(
                is_active=True
            )

        company = Company.objects.get(
            user=self.request.user
        )

        return OfferLetter.objects.filter(
            application__job__company=company,
            is_active=True
        )


class MyOfferLettersView(generics.ListAPIView):

    serializer_class = OfferLetterSerializer

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    def get_queryset(self):

        return OfferLetter.objects.filter(

            application__student=self.request.user,

            is_active=True

        )


class AcceptOfferView(generics.UpdateAPIView):

    serializer_class = OfferLetterSerializer

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    def get_queryset(self):

        return OfferLetter.objects.filter(

            application__student=self.request.user,

            is_active=True

        )

    def perform_update(self, serializer):
        offer = serializer.save(
            status="accepted"
        )

        create_notification(

            user=offer.application.job.company.user,

            title="Offer Accepted",

            message=(
                f"{offer.application.student.username} "
                f"accepted the offer for "
                f"{offer.application.job.title}."
            )

        )


class DeclineOfferView(generics.UpdateAPIView):

    serializer_class = OfferLetterSerializer

    permission_classes = [
        IsAuthenticated,
        IsStudent
    ]

    def get_queryset(self):

        return OfferLetter.objects.filter(

            application__student=self.request.user,

            is_active=True

        )

    def perform_update(self, serializer):
        offer = serializer.save(
            status="declined"
        )

        create_notification(

            user=offer.application.job.company.user,

            title="Offer Declined",

            message=(
                f"{offer.application.student.username} "
                f"declined the offer for "
                f"{offer.application.job.title}."
            )

        )


