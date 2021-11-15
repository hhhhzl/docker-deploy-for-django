from rest_framework import generics
from rest_framework.permissions import BasePermission

from .models import Score
from .serializers import ScoreSerializer


# ====================  Score  ==================== #


class ScoreViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins only
            return request.user.user_type in ('A',)
        elif request.method == 'POST':
            # TODO: delete?
            return request.user.user_type in ('E',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ScoreView(generics.ListCreateAPIView, generics.GenericAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = (ScoreViewPermission,)
    filterset_fields = ["question", "org", "expert"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(question=self.kwargs.get("question"), org=self.kwargs.get("org"))

    # def perform_create(self, serializer):
    #     request = serializer.context.get("request")
    #     org_model = apps.get_model("organizations.Organization")
    #     serializer.save(**{
    #         "question": Question.objects.get(id=self.kwargs.get("question")),
    #         "org": org_model.objects.get(id=self.kwargs.get("org")),
    #         "expert": request.user,
    #     })


# ==================== Score Detail ==================== #


class ScoreDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # admins - all, experts - self
            return request.user.user_type in ('A',) or \
                   (request.user.user_type in ('E',) and request.user.id == view.kwargs.get('expert'))
        elif request.method in ('PUT', 'PATCH'):
            # admins - all, experts - self
            return request.user.user_type in ('A',) or \
                   (request.user.user_type in ('E',) and request.user.id == view.kwargs.get('expert'))
        else:
            return request.method in ('HEAD', 'OPTIONS')


class ScoreDetailView(generics.RetrieveUpdateAPIView, generics.GenericAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = "id"  # "expert"
    permission_classes = (ScoreDetailViewPermission,)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(question=self.kwargs.get("question"), org=self.kwargs.get("org"))
