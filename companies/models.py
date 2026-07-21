from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    industry = models.CharField(
        max_length=200,
        blank=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    recruiter_name = models.CharField(
        max_length=200,
        blank=True
    )

    recruiter_designation = models.CharField(
        max_length=100,
        blank=True
    )

    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
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

    def soft_delete(self):

        self.is_active = False

        self.save()

    def __str__(self):

        return self.company_name if self.company_name else self.user.username