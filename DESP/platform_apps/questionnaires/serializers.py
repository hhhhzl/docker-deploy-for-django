from rest_framework.serializers import ModelSerializer

from .models import Questionnaire, Indicator


class QuestionnaireSerializer(ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = "__all__"


class IndicatorSerializer(ModelSerializer):
    class Meta:
        model = Indicator
        fields = "__all__"
