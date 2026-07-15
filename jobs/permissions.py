from rest_framework.permissions import BasePermission


# =========================
# Admin
# =========================

class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "admin"
        )


# =========================
# Placement Officer
# =========================

class IsOfficer(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "officer"
        )


# =========================
# Recruiter
# =========================

class IsRecruiter(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "recruiter"
        )


# =========================
# Student
# =========================

class IsStudent(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "student"
        )


# =========================
# Admin OR Recruiter
# =========================

class IsAdminOrRecruiter(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "recruiter",
            ]
        )


# =========================
# Admin OR Officer
# =========================

class IsAdminOrOfficer(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "officer",
            ]
        )


# =========================
# Admin OR Recruiter OR Officer
# =========================

class IsAdminRecruiterOfficer(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "recruiter",
                "officer",
            ]
        )


# =========================
# All Roles
# =========================

class IsAllRoles(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "officer",
                "recruiter",
                "student",
            ]
        )