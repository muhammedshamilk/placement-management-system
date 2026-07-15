from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )



class IsRecruiter(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "recruiter"
        )



class IsAdminOrOfficer(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role in ["admin", "officer"]
        )