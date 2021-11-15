from rest_framework.serializers import ModelSerializer

from .models import Score


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"
        extra_kwargs = {
            "question": {"read_only": True},
            "org": {"read_only": True},
            "expert": {"read_only": True},
            "score": {"required": True, "allow_null": False}
        }
