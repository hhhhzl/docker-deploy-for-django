from rest_framework.serializers import ModelSerializer

from .models import Submission


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        extra_kwargs = {
            "last_updated_by": {"read_only": True},
        }
