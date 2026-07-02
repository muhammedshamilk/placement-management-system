from django.urls import path

from .views import (
    StudentCreateView,
    StudentListView,
    StudentDetailView,
    StudentUpdateView,
    StudentDeleteView
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
        '<int:pk>/',
        StudentDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        StudentUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        StudentDeleteView.as_view()
    ),

]