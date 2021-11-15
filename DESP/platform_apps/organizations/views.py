from rest_framework import generics
# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from .models import Organization
from .serializers import OrganizationSerializer


# ====================  Organization  ==================== #


class OrganizationViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors only
            return request.user.user_type in ('S',)
        elif request.method == 'POST':
            # supervisors only
            return request.user.user_type in ('S',)
        elif request.method in ('PUT', 'PATCH'):
            # supervisors only
            return request.user.user_type in ('S',)
        elif request.method == 'DELETE':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class OrganizationView(ListBulkCreateUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (OrganizationViewPermission,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


# ==================== Organization Detail ==================== #


class OrganizationDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors or self
            return request.user.user_type in ('S',) or (request.user.org.id == view.kwargs.get('id'))
        elif request.method in ('PUT', 'PATCH'):
            # supervisors - all, managers - self
            return request.user.user_type in ('S',) or \
                   (request.user.user_type in ('M',) and (request.user.org.id == view.kwargs.get('id')))
        elif request.method == 'DELETE':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"
    permission_classes = (OrganizationDetailViewPermission,)

    # can only delete those associate with no children orgs, no users, and no projects
    # enforced by database on_delete = restrict
