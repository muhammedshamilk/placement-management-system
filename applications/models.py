from django.db import models
from accounts.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(
        upload_to="application_resumes/",
        blank=True,
        null=True
    )

    cover_letter = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="applied"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["student", "job"]

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"