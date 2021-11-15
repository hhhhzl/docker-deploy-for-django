from rest_framework.serializers import ModelSerializer

from .models import Organization
from ..junctions.serializers import ProjectOrganizationSerializer


class OrganizationSerializer(ModelSerializer):
    project = ProjectOrganizationSerializer(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = "__all__"
