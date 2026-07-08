from django.db import models
from companies.models import Company
from datetime import date


class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    requirements = models.TextField()

    location = models.CharField(max_length=100)

    salary_package = models.CharField(max_length=100)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    vacancies = models.PositiveIntegerField(default=1)

    minimum_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    skills_required = models.TextField()

    application_deadline = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )


    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title