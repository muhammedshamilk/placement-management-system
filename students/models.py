from django.db import models
from accounts.models import User


class StudentProfile(models.Model):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    dob = models.DateField(
        blank=True,
        null=True
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    course = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    academic_year = models.IntegerField(
        blank=True,
        null=True
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True,
        null=True
    )

    linkedin = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )

    github = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )

    portfolio = models.URLField(
        max_length=255,
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(
        upload_to="student_profiles/",
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @property
    def profile_completed(self):

        required_fields = [

            self.phone,

            self.gender,

            self.dob,

            self.department,

            self.course,

            self.academic_year,

            self.cgpa,

            self.skills,

            self.resume,

        ]

        return all(required_fields)