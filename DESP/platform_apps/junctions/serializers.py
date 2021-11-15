from django.apps import apps
from rest_framework.serializers import ModelSerializer

from .models import ProjectOrganization, QuestionExpert

Project = apps.get_model("projects", "Project")
Organization = apps.get_model("organizations", "Organization")


class ProjectOrganizationSerializer(ModelSerializer):

    def to_representation(self, instance):
        if isinstance(instance, (Project, Organization)):
            # m2m representation in Project & Organization serializers
            return instance.id
        return super().to_representation(instance)

    class Meta:
        model = ProjectOrganization
        exclude = ["id"]


class QuestionExpertSerializer(ModelSerializer):
    class Meta:
        model = QuestionExpert
        exclude = ["id"]
