from django.apps import apps
from rest_framework import generics
from rest_framework.permissions import BasePermission

from .models import Question
from .serializers import QuestionSerializer

ProjectOrganization = apps.get_model("junctions", "ProjectOrganization")


# ====================  Question  ==================== #


class QuestionViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # see QuestionView.get_queryset()
            return True
        elif request.method == 'POST':
            # admins only
            return request.user.user_type in ('A',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class QuestionView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (QuestionViewPermission,)
    filterset_fields = ["qnaire"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     user = self.request.user
    #     filter_fields = ["qnaire"]
    #     filter_kwargs = make_filter_kwargs(self.request.query_params, filter_fields)
    #     # if user.user_type not in ('A',):
    #     #     filter_kwargs.update(**{"project__in": [
    #     #         item.project for item in ProjectOrganization.objects.filter(org=user.org)
    #     #     ]})
    #     return qs.filter(**filter_kwargs)


# ==================== Question Detail ==================== #


class QuestionDetailViewPermission(BasePermission):

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


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView, generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = "id"
    permission_classes = (QuestionDetailViewPermission,)
