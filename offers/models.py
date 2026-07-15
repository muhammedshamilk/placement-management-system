from django.db import models
from applications.models import Application


class OfferLetter(models.Model):

    STATUS_CHOICES = (

        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),

    )

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="offer_letter"
    )

    offer_letter = models.FileField(
        upload_to="offer_letters/"
    )

    offer_date = models.DateField()

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="sent"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.application.student.username} - Offer Letter"