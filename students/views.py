from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from .permissions import IsStudent
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from .permissions import IsAdminOrOfficer
from rest_framework.parsers import MultiPartParser, FormParser

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

# Student View Own Profile
class MyProfileView(APIView):

    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):

        try:
            profile = StudentProfile.objects.get(
                user=request.user,
                is_active=True
            )

            serializer = StudentProfileSerializer(profile)

            return Response(serializer.data)

        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


# Student Update Own Profile
class MyProfileUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsStudent]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def put(self, request):

        try:

            profile = StudentProfile.objects.get(
                user=request.user,
                is_active=True
            )

        except StudentProfile.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentProfileSerializer(

            profile,

            data=request.data,

            partial=True

        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(

            serializer.errors,

            status=status.HTTP_400_BAD_REQUEST

        )
from .permissions import IsAdminOrOfficer
from applications.models import Application
from companies.models import Company
from rest_framework.exceptions import PermissionDenied


class RecruiterStudentProfileView(generics.RetrieveAPIView):

    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        student = get_object_or_404(
            StudentProfile,
            user_id=self.kwargs["pk"],
            is_active=True
        )

        # Admin and Placement Officer can view any student
        if self.request.user.role in ["admin", "officer"]:
            return student

        # Only recruiters from the same company can view applicants
        if self.request.user.role == "recruiter":

            company = get_object_or_404(
                Company,
                user=self.request.user
            )

            applied = Application.objects.filter(
                student=student.user,
                job__company=company,
                is_active=True
            ).exists()

            if not applied:

                raise PermissionDenied(
                    "You cannot view this student's profile."
                )

            return student

        raise PermissionDenied("Permission denied.")