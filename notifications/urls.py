from django.urls import path
from .views import *

urlpatterns = [

    path(
        "",
        MyNotificationsView.as_view()
    ),

    path(
        "read/<int:pk>/",
        MarkAsReadView.as_view()
    ),

    path(
        "read-all/",
        MarkAllAsReadView.as_view()
    ),

    path(
        "delete/<int:pk>/",
        NotificationDeleteView.as_view()
    ),

]