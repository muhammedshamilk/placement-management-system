from django.db import models
from accounts.models import User


class StudentProfile(models.Model):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    dob = models.DateField()

    department = models.CharField(max_length=100)

    course = models.CharField(max_length=100)

    academic_year = models.IntegerField()

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    skills = models.TextField()

    linkedin = models.URLField(
        blank=True,
        null=True
    )

    github = models.URLField(
        blank=True,
        null=True
    )

    portfolio = models.URLField(
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to='resumes/'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username