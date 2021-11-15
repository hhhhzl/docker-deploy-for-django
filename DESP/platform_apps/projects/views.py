from django.apps import apps
from rest_framework import generics
# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission

from .models import Project, Progress
from .serializers import ProjectSerializer, ProgressSerializer


# ====================  Project  ==================== #


class ProjectViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # see ProjectView.get_queryset()
            return True
        elif request.method == 'POST':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ProjectView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (ProjectViewPermission,)
    filterset_fields = ["admin"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        # admins and supervisors - all, others - self
        qs = super().get_queryset()
        if self.request.user.user_type in ('A', 'S'):
            return qs
        return qs.filter(org__in=[self.request.user.org])

    def perform_create(self, serializer):
        request = serializer.context.get("request")
        serializer.save(**{
            "admin": request.user
        })


# ====================  Project Detail ==================== #


class ProjectDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # see has_object_permission()
            return True
        elif request.method in ('PUT', 'PATCH'):
            # supervisors only
            return request.user.user_type in ('S',)
        elif request.method == 'DELETE':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        # admins and supervisors - all, others - self
        if request.user.user_type in ("A", "S"):
            return True
        return (apps.get_model("junctions", "ProjectOrganization").objects
                .filter(project=obj, org=request.user.org).exists())


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "id"
    permission_classes = (ProjectDetailViewPermission,)


# ====================  Progress  ==================== #


class ProgressViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins only
            return request.user.user_type in ('A',)
        elif request.method == 'POST':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ProgressView(generics.ListCreateAPIView, generics.GenericAPIView):
    serializer_class = ProjectSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (ProgressViewPermission,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Progress.objects.filter(project=self.kwargs.get("project"))


# ====================  Progress Detail  ==================== #


class ProgressDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins only
            return request.user.user_type in ('A',)
        elif request.method in ('PUT', 'PATCH'):
            # admins only
            return request.user.user_type in ('A',)
        elif request.method in 'DELETE':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ProgressDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    serializer_class = ProgressSerializer
    lookup_field = "id"
    permission_classes = (ProgressDetailViewPermission,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Progress.objects.filter(project=self.kwargs.get("project"))
