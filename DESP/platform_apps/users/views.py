from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DESPUser
from .serializers import DESPUserSerializer, RegistrationSerializer, TokenProfileSerializer


# ====================  DESPUser  ==================== #


class DESPUserViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class DESPUserView(generics.ListAPIView, generics.GenericAPIView):
    queryset = DESPUser.objects.all()
    serializer_class = DESPUserSerializer
    permission_classes = (DESPUserViewPermission,)
    filterset_fields = ["org", "user_type"]


# ====================  DESPUser Detail  ==================== #


class DESPUserDetailViewPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'GET':
            # supervisors or self
            return request.user.user_type in ('S',) or (request.user.id == view.kwargs.get('id'))
        elif request.method in ('PUT', 'PATCH'):
            # supervisors or self
            return request.user.user_type in ('S',) or (request.user.id == view.kwargs.get('id'))
        else:
            return request.method in ('HEAD', 'OPTIONS')


class DESPUserDetailView(generics.RetrieveUpdateAPIView, generics.GenericAPIView):
    queryset = DESPUser.objects.all()
    serializer_class = DESPUserSerializer
    lookup_field = "id"
    permission_classes = (DESPUserDetailViewPermission,)


# ====================  Authentication  ==================== #


def refresh_token(user, token):
    delta = (timezone.now() - token.created).total_seconds()
    if delta > 60 * 60 * 48:  # expires after 48 hours
        token.delete()
        return Token.objects.create(user=user)
    return token


class RegistrationPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.method == 'POST':
            # supervisors only
            return request.user.user_type in ('S',)
        else:
            return request.method in ('HEAD', 'OPTIONS')


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = (RegistrationPermission,)

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={status.HTTP_201_CREATED: TokenProfileSerializer}
    )
    def post(self, request):
        # create user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # create token
        token, _ = Token.objects.get_or_create(user=user)
        # response
        res_data = TokenProfileSerializer(instance={
            "profile": user,
            "token": token.key
        }).data
        return Response(res_data, status=status.HTTP_201_CREATED)


class LoginPermission(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class LoginView(ObtainAuthToken):
    permission_classes = (LoginPermission,)

    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        responses={status.HTTP_200_OK: TokenProfileSerializer}
    )
    def post(self, request, *args, **kwargs):
        # get user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        # get token
        token, _ = Token.objects.get_or_create(user=user)
        token = refresh_token(user, token)
        # response
        res_data = TokenProfileSerializer(instance={
            "profile": user,
            "token": token.key
        }).data
        return Response(res_data)


class TokenProfilePermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated


class TokenProfileView(APIView):
    permission_classes = (TokenProfilePermission,)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        token_key = request.META.get("HTTP_AUTHORIZATION", "")[6:]
        token = Token.objects.get(key=token_key)
        res_data = TokenProfileSerializer(instance={
            "profile": token.user,
            "token": token.key
        }).data
        return Response(res_data)
