from rest_framework.permissions import BasePermission


class IsAdminOrRecruiter(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "recruiter",
            ]
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "student"
        )


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