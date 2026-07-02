from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )

    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    address = models.TextField()

    recruiter_name = models.CharField(max_length=200)
    recruiter_designation = models.CharField(max_length=100)

    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.company_name