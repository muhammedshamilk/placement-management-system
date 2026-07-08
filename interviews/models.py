from django.db import models
from applications.models import Application


class Interview(models.Model):

    INTERVIEW_MODE = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    RESULT_CHOICES = (
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='interview'
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    interview_mode = models.CharField(
        max_length=20,
        choices=INTERVIEW_MODE
    )

    interview_location = models.CharField(
        max_length=255
    )

    interviewer_name = models.CharField(
        max_length=150
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='pending'
    )

    feedback = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application.student.username} - {self.application.job.title}"