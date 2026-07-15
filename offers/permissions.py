from rest_framework.permissions import BasePermission


class IsRecruiter(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "recruiter"
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "student"
        )


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == "admin"
        )


class IsRecruiterOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in [
                "admin",
                "recruiter",
            ]
        )