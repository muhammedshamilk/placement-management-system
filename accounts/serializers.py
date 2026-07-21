from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from students.models import StudentProfile
from .models import User
from companies.models import Company

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
            'role'
        ]

    def validate_username(self, value):

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Email is already registered."
            )

        return value

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )

        return attrs

    def create(self, validated_data):

        print("========== REGISTER SERIALIZER EXECUTED ==========")

        validated_data.pop("confirm_password")

        user = User.objects.create_user(

            username=validated_data["username"],

            email=validated_data["email"],

            role=validated_data["role"],

            password=validated_data["password"]

        )

        # -------------------------
        # Student
        # -------------------------

        if user.role == "student":

            StudentProfile.objects.create(

                user=user

            )

        # -------------------------
        # Recruiter
        # -------------------------

        elif user.role == "recruiter":

            print("Creating company for:", user.username)

            company = Company.objects.create(

                user=user,

                company_name="",

                industry="",

                website="",

                email=user.email,

                phone="",

                address="",

                recruiter_name=user.username,

                recruiter_designation="",

                description="",

            )

            print("Company Created:", company.id)

        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'role'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match."
                }
            )

        return attrs