from django.apps import apps
from rest_framework import generics
from rest_framework.permissions import BasePermission

from .models import Questionnaire, Indicator
from .serializers import QuestionnaireSerializer, IndicatorSerializer
from ..utils import make_filter_kwargs

ProjectOrganization = apps.get_model("junctions", "ProjectOrganization")


# ====================  Questionnaire  ==================== #


class QuestionnaireViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # see QuestionnaireView.get_queryset()
            return True
        elif request.method == 'POST':
            # admin
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class QuestionnaireView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    permission_classes = (QuestionnaireViewPermission,)
    filterset_fields = ["project"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        # admins - all, others - self
        qs = super().get_queryset()
        user = self.request.user
        filter_fields = ["project"]
        filter_kwargs = make_filter_kwargs(self.request.query_params, filter_fields)

        if user.user_type not in ('A',):
            filter_kwargs.update(**{"project__in": [
                item.project for item in ProjectOrganization.objects.filter(org=user.org)
            ]})

        return qs.filter(**filter_kwargs)


# ==================== Questionnaire Detail ==================== #


class QuestionnaireDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # see has_object_permission()
            return True
        elif request.method in ('PUT', 'PATCH'):
            # admins only
            return request.user.user_type in ('A',)
        elif request.method == 'DELETE':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            # admins - all, others - self
            return request.user.user_type in ('A',) or \
                   ProjectOrganization.objects.filter(project=obj.project, org=request.user.org).exists()
        elif request.method in ('PUT', 'PATCH'):
            # project must not be published
            return obj.project.status == '1'
        elif request.method == 'DELETE':
            # project must not be published
            return obj.project.status == '1'
        else:
            return True


class QuestionnaireDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = "id"
    permission_classes = (QuestionnaireDetailViewPermission,)


# ====================  Indicator  ==================== #


class IndicatorViewPermission(BasePermission):

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


class IndicatorView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = (IndicatorViewPermission,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(self.kwargs.get("qnaire"))


# ==================== Indicator Detail ==================== #


class IndicatorDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins only
            return request.user.user_type in ('A',)
        elif request.method in ('PUT', 'PATCH'):
            # admins only
            return request.user.user_type in ('A',)
        elif request.method == 'DELETE':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH'):
            # project must be active
            return obj.questionnaire.project.status != '4'
        elif request.method == 'DELETE':
            # project must be active
            return obj.questionnaire.project.status != '4'
        else:
            return True


class IndicatorDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    lookup_field = "id"
    permission_classes = (IndicatorDetailViewPermission,)
