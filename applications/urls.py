from django.urls import path
from .views import *

urlpatterns = [

    path(
        'apply/',
        ApplyJobView.as_view()
    ),

    path(
        'my-applications/',
        MyApplicationsView.as_view()
    ),

    path(
        '',
        ApplicationListView.as_view()
    ),

    path(
        '<int:pk>/',
        ApplicationDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        ApplicationUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        ApplicationDeleteView.as_view()
    ),
]