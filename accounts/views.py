from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import User
from .serializers import VerifyOTPSerializer
from .serializers import ResetPasswordSerializer
from .models import PasswordResetOTP

from .utils import generate_otp, send_otp_email

from .serializers import ForgotPasswordSerializer

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from .permissions import IsAdminRole



class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, *args, **kwargs):

        print("REGISTER VIEW CALLED")

        return super().post(request, *args, **kwargs)
# List Users
class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# User Detail
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


# Soft Delete User
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():

            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not request.user.check_password(old_password):

                return Response(
                    {"error": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            request.user.set_password(new_password)
            request.user.save()

            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors)

class RecruiterListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_queryset(self):
        return User.objects.filter(
            role="recruiter",
            is_active=True
        )


class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            try:

                user = User.objects.get(
                    email=email,
                    is_active=True
                )

            except User.DoesNotExist:

                return Response(
                    {
                        "error": "No account found with this email."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Delete previous unused OTPs

            PasswordResetOTP.objects.filter(
                user=user,
                is_used=False
            ).delete()

            otp = generate_otp()

            PasswordResetOTP.objects.create(

                user=user,

                otp=otp

            )

            send_otp_email(user.email, otp)

            return Response(

                {
                    "message": "OTP sent successfully."
                },

                status=status.HTTP_200_OK

            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VerifyOTPView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            otp = serializer.validated_data["otp"]

            try:

                user = User.objects.get(
                    email=email,
                    is_active=True
                )

            except User.DoesNotExist:

                return Response(
                    {
                        "error": "Invalid email."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            try:

                otp_obj = PasswordResetOTP.objects.get(

                    user=user,

                    otp=otp,

                    is_used=False

                )

            except PasswordResetOTP.DoesNotExist:

                return Response(

                    {
                        "error": "Invalid OTP."
                    },

                    status=status.HTTP_400_BAD_REQUEST

                )

            if otp_obj.is_expired():

                return Response(

                    {
                        "error": "OTP has expired."
                    },

                    status=status.HTTP_400_BAD_REQUEST

                )

            return Response(

                {
                    "message": "OTP verified successfully."
                },

                status=status.HTTP_200_OK

            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class ResetPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["email"]

            otp = serializer.validated_data["otp"]

            password = serializer.validated_data["password"]

            try:

                user = User.objects.get(
                    email=email,
                    is_active=True
                )

            except User.DoesNotExist:

                return Response(
                    {
                        "error": "Invalid email."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            try:

                otp_obj = PasswordResetOTP.objects.get(
                    user=user,
                    otp=otp,
                    is_used=False
                )

            except PasswordResetOTP.DoesNotExist:

                return Response(
                    {
                        "error": "Invalid OTP."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if otp_obj.is_expired():

                return Response(
                    {
                        "error": "OTP has expired."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Change password

            user.set_password(password)

            user.save()

            # Mark OTP as used

            otp_obj.is_used = True

            otp_obj.save()

            return Response(

                {
                    "message": "Password reset successfully."
                },

                status=status.HTTP_200_OK

            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )