from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter

from .models import StudentProfile
from .serializers import StudentProfileSerializer
from .permissions import IsAdminOrOfficer


# Add Student
class StudentCreateView(generics.CreateAPIView):

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOfficer]


# View All Students
class StudentListView(generics.ListAPIView):

    queryset = StudentProfile.objects.filter(
        is_active=True
    )

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOfficer]

    filter_backends = [SearchFilter]

    search_fields = [
        'user__username',
        'department',
        'course',
        'skills'
    ]


# View Single Student
class StudentDetailView(generics.RetrieveAPIView):

    queryset = StudentProfile.objects.filter(
        is_active=True
    )

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOfficer]


# Update Student
class StudentUpdateView(generics.UpdateAPIView):

    queryset = StudentProfile.objects.filter(
        is_active=True
    )

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOfficer]


# Soft Delete Student
class StudentDeleteView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrOfficer
    ]

    def delete(self, request, pk):

        try:

            student = StudentProfile.objects.get(
                pk=pk
            )

            student.is_active = False
            student.save()

            return Response(
                {
                    "message":
                    "Student profile deactivated successfully"
                },
                status=status.HTTP_200_OK
            )

        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error":
                    "Student not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )