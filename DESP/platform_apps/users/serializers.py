from rest_framework.serializers import Serializer, ModelSerializer, CharField

from .models import DESPUser


class DESPUserSerializer(ModelSerializer):
    org_name = CharField(source='org.name', read_only=True)

    class Meta:
        model = DESPUser
        exclude = ["password", "groups", "user_permissions"]


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = DESPUser
        fields = ["username", "password"] + DESPUser.REQUIRED_FIELDS
        extra_kwargs = {
            "password": {"write_only": True},
            "user_type": {"required": True},
        }

    def save(self, **kwargs):
        if self.validated_data["user_type"] == "S":
            return DESPUser.objects.create_superuser(**self.validated_data)
        else:
            return DESPUser.objects.create_user(**self.validated_data)


class TokenProfileSerializer(Serializer):
    profile = DESPUserSerializer()
    token = CharField()
