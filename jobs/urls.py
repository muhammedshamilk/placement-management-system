from django.urls import path
from .views import *
from .views import JobMatchView
urlpatterns = [

    path(
        'create/',
        JobCreateView.as_view()
    ),

    path(
        '',
        JobListView.as_view()
    ),

    path(
        '<int:pk>/',
        JobDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        JobUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        JobDeleteView.as_view()
    ),
path(
    "<int:pk>/match/",
    JobMatchView.as_view(),
    name="job-match"
),
]