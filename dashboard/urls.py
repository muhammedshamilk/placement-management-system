from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("officer/", OfficerDashboardView.as_view(), name="officer-dashboard"),
    path("recruiter/", RecruiterDashboardView.as_view(), name="recruiter-dashboard"),
    path("student/", StudentDashboardView.as_view(), name="student-dashboard"),
]