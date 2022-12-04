from rest_framework import viewsets, filters, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TitlesSerializer,
    SingUpSerializer,
    TokenSerializer,
    CustomUserSerializer,
    CustomUserEditSerializer

)
from reviews.models import Categories, Genres, Titles, CustomUser


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'category', 'genre', 'name')


class CategoriesViewSet(viewsets.ViewSetMixin):
    queryset = Categories.objects.all()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            CustomUser,
            username=serializer.validated_data["username"]
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="Confirmation code",
            message=f"Ваш код подтверждения: {confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceivingJWTToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser,
            username=serializer.validated_data["username"]
        )

        if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]
        ):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        serializer_class=CustomUserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
