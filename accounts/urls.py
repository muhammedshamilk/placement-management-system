from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    ProfileView,
    ChangePasswordView,
    UserListView,
    UserDetailView,
    UserDeleteView,
    RecruiterListView,
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView
)
import os

print("USING URL FILE:", os.path.abspath(__file__))

print("ACCOUNTS URLS LOADED")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("recruiters/",RecruiterListView.as_view(),name="recruiter-list"),
path(
    "forgot-password/",
    ForgotPasswordView.as_view(),
    name="forgot-password"
),
path(
    "verify-otp/",
    VerifyOTPView.as_view(),
    name="verify-otp"
),
path(
    "reset-password/",
    ResetPasswordView.as_view(),
    name="reset-password",
),
]

print("Loaded urlpatterns:", urlpatterns)

