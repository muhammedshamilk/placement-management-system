from django.urls import path

from .views import (
    StudentCreateView,
    StudentListView,
    StudentDetailView,
    StudentUpdateView,
    StudentDeleteView,
    MyProfileView,
    MyProfileUpdateView,
    RecruiterStudentProfileView

)

urlpatterns = [

    path(
        'create/',
        StudentCreateView.as_view()
    ),

    path(
        '',
        StudentListView.as_view()
    ),



    path(
        'update/<int:pk>/',
        StudentUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        StudentDeleteView.as_view()
    ),
    path(
        "my-profile/",
        MyProfileView.as_view(),
        name="my-profile"
    ),

    path(
        "my-profile/update/",
        MyProfileUpdateView.as_view(),
        name="my-profile-update"
    ),
    path(
        "recruiter/<int:pk>/",
        RecruiterStudentProfileView.as_view()
    ),

    path(
        "<int:pk>/",
        StudentDetailView.as_view()
    ),

]