from django.urls import path
from .views import *

urlpatterns = [

    path(
        'create/',
        InterviewCreateView.as_view()
    ),

    path(
        '',
        InterviewListView.as_view()
    ),

    path(
        '<int:pk>/',
        InterviewDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        InterviewUpdateView.as_view()
    ),

    path(
        'result/<int:pk>/',
        InterviewResultUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        InterviewDeleteView.as_view()
    ),

    path(
        'my-interviews/',
        MyInterviewView.as_view()
    ),
]