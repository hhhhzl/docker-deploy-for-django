from django.apps import apps
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from .models import ProjectOrganization, QuestionExpert
from .serializers import ProjectOrganizationSerializer, QuestionExpertSerializer

Organization = apps.get_model("organizations", "Organization")


# ==================== ProjectOrganization ==================== #


class ProjectOrganizationViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors, managers, users - see ProjectOrganizationView.get_queryset()
            return request.user.user_type in ('S', 'M', 'U')
        elif request.method == 'POST':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ProjectOrganizationView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = ProjectOrganization.objects.all()
    serializer_class = ProjectOrganizationSerializer
    permission_classes = (ProjectOrganizationViewPermission,)
    filterset_fields = ["project", "org"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        # supervisors - all, managers and users - self
        qs = super().get_queryset()
        filter_kwargs = {}
        if self.request.user.user_type in ('M', 'U'):
            filter_kwargs.update({"org": self.request.user.org})
        return qs.filter(**filter_kwargs)

    def perform_create(self, serializer):
        has_err = False

        def run_validation(data):
            nonlocal has_err
            err = {}
            if Organization.objects.filter(parent_org=data.get("org")).exists():
                err.update(**{"org": ["The organization must have no children."]})
                has_err = True
            return err

        if isinstance(serializer.validated_data, list):
            errors = [run_validation(data) for data in serializer.validated_data]
        else:
            errors = run_validation(serializer.validated_data)
        if has_err:
            raise ValidationError(errors)

        serializer.save()


# ==================== ProjectOrganization Detail ==================== #


class ProjectOrganizationDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors - all, managers and users - self
            return request.user.user_type in ('S',) or \
                   (request.user.user_type in ('M', 'U') and request.user.org.id == view.kwargs.get('org'))
        elif request.method in ('PUT', 'PATCH'):
            # supervisors - all, managers and users - self
            return request.user.user_type in ('S',) or \
                   (request.user.user_type in ('M', 'U') and request.user.org.id == view.kwargs.get('org'))
        elif request.method == 'DELETE':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ProjectOrganizationDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = ProjectOrganization.objects.all()
    serializer_class = ProjectOrganizationSerializer
    permission_classes = (ProjectOrganizationDetailViewPermission,)

    def get_object(self):
        obj = generics.get_object_or_404(self.queryset, **{
            "project": self.kwargs.get("project"),
            "org": self.kwargs.get("org"),
        })
        self.check_object_permissions(self.request, obj)
        return obj


# ==================== QuestionExpert ==================== #


class QuestionExpertViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins, experts - see QuestionExpertView.get_queryset()
            return request.user.user_type in ('A', 'E')
        elif request.method == 'POST':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class QuestionExpertView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = QuestionExpert.objects.all()
    serializer_class = QuestionExpertSerializer
    permission_classes = (QuestionExpertViewPermission,)
    filterset_fields = ["question", "expert"]

    def get_queryset(self):
        # admins - all, experts - self
        qs = super().get_queryset()
        filter_kwargs = {}
        if self.request.user.user_type in ('E',):
            filter_kwargs.update(**{
                "expert": self.request.user
            })
        return qs.filter(**filter_kwargs)

    def perform_create(self, serializer):
        has_err = False

        def run_validation(data):
            nonlocal has_err
            err = {}
            if data.get("question").rubric != "E":
                err.update(**{"question": ["This question should not be graded by an expert."]})
                has_err = True
            if data.get("expert").user_type != "E":
                err.update(**{"expert": ["This user is not an expert."]})
                has_err = True
            return err

        if isinstance(serializer.validated_data, list):
            errors = [run_validation(data) for data in serializer.validated_data]
        else:
            errors = run_validation(serializer.validated_data)
        if has_err:
            raise ValidationError(errors)

        serializer.save()


# ==================== QuestionExpert Detail ==================== #


class QuestionExpertDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins - all, experts - self
            return request.user.user_type in ('A',) or \
                   (request.user.user_type in ('E',) and request.user.org.id == view.kwargs.get('expert'))
        elif request.method in ('PUT', 'PATCH'):
            # admins - all, experts - self
            return request.user.user_type in ('A',) or \
                   (request.user.user_type in ('E',) and request.user.org.id == view.kwargs.get('expert'))
        elif request.method == 'DELETE':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class QuestionExpertDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = QuestionExpert.objects.all()
    serializer_class = QuestionExpertSerializer
    permission_classes = (QuestionExpertDetailViewPermission,)

    def get_object(self):
        obj = generics.get_object_or_404(self.queryset, **{
            "question": self.kwargs.get("question"),
            "expert": self.kwargs.get("expert"),
        })
        self.check_object_permissions(self.request, obj)
        return obj
