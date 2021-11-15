from django.apps import apps
from rest_framework import generics
from rest_framework.permissions import BasePermission

from .models import Submission
from .serializers import SubmissionSerializer

Question = apps.get_model("questions", "Question")


# ====================  Submission  ==================== #


class SubmissionViewPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == "GET":
            # admins, managers and users
            return request.user.user_type in ("A", "M", "U")
        elif request.method == "POST":
            # admins only
            return request.user.user_type in ("A",)
        else:
            return request.method in ("HEAD", "OPTIONS")


class SubmissionView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (SubmissionViewPermission,)
    filterset_fields = ["question", "org", "question__qnaire"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        req_user = self.request.user
        if req_user.user_type in ("A",):
            # admins - all
            return super().get_queryset()
        else:
            # managers and users - self
            return Submission.objects.filter(org=req_user.org)

    def perform_create(self, serializer):
        request = serializer.context.get("request")
        serializer.save(
            **{
                "last_updated_by": request.user,
            }
        )


# ==================== Submission Detail ==================== #


class SubmissionDetailViewPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == "GET":
            # admins, managers and users
            return request.user.user_type in ("A", "M", "U")
        elif request.method in ("PUT", "PATCH"):
            # admins, managers and users
            return request.user.user_type in ("A", "M", "U")
        else:
            return request.method in ("HEAD", "OPTIONS")

    def has_object_permission(self, request, view, obj):
        if request.user.user_type in ("A",):
            # admins - all
            return True
        else:
            # managers and users - self
            return request.user.org == obj.org


class SubmissionDetailView(
    generics.RetrieveUpdateAPIView, generics.GenericAPIView
):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    lookup_field = "id"  # "org"
    permission_classes = (SubmissionDetailViewPermission,)

    def perform_update(self, serializer):
        request = serializer.context.get("request")
        serializer.save(
            **{
                "last_updated_by": request.user,
            }
        )

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(question=self.kwargs.get("question"))
