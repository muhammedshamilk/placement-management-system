from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


# ==========================
# My Notifications
# ==========================

class MyNotificationsView(generics.ListAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user,
            is_active=True
        )


# ==========================
# Mark Notification as Read
# ==========================

class MarkAsReadView(generics.UpdateAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def perform_update(self, serializer):

        serializer.save(
            is_read=True
        )


# ==========================
# Mark All Notifications Read
# ==========================

class MarkAllAsReadView(generics.GenericAPIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request):

        Notification.objects.filter(
            user=request.user,
            is_read=False,
            is_active=True
        ).update(
            is_read=True
        )

        return Response({
            "message": "All notifications marked as read."
        })


# ==========================
# Delete Notification
# ==========================

class NotificationDeleteView(generics.DestroyAPIView):

    serializer_class = NotificationSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def perform_destroy(self, instance):

        instance.is_active = False
        instance.save()