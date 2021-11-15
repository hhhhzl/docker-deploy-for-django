from rest_framework.serializers import ModelSerializer

from .models import Project, Progress
from ..junctions.serializers import ProjectOrganizationSerializer


class ProjectSerializer(ModelSerializer):
    org = ProjectOrganizationSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = "__all__"
        extra_kwargs = {
            "admin": {"read_only": True}
        }


class ProgressSerializer(ModelSerializer):
    class Meta:
        model = Progress
        fields = "__all__"
