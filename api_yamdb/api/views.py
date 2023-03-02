from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)
from django.db.models.functions import Round
from rest_framework import filters
from django.conf import settings

from .serializers import (
    TitleSerializer,
    CategoriesSerializer,
    GenresSerializer,
    SingUpSerializer,
    TokenSerializer,
    CustomUserSerializer,
    CustomUserEditSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleGETSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    AuthorAdminModeratorOrReadOnly,
)
from reviews.models import (
    Categories,
    Genres,
    Title,
    CustomUser,
    Review
)
from .filters import TitlesFilter

from django.db import IntegrityError
from rest_framework import serializers


class TitleViewSet(viewsets.ModelViewSet):
    """ Произведения. Рейтинг вычисляется на 'лету'.
    Досттуп для изменения - админ. Доступ для чтения - все"""
    queryset = Title.objects.annotate(
        rating=Round(Avg('reviews__score')))
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter
    search_fields = ('name', 'genre', 'category')
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    """ Категории. Досттуп для изменения - админ
     Доступ для чтения - все. """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(viewsets.ModelViewSet):
    """ Жанры. Досттуп для изменения - админ
     Доступ для чтения - все. """
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class WrongUsernameOrEmail(Exception):
    """Email или username уже заняты."""

    pass


class RegisterView(APIView):
    """ Самостоятельная регистрация пользователя. """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = CustomUser.objects.get_or_create(
                **serializer.validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'Не верный адрес или логин'
            )

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceivingJWTToken(APIView):
    """ Авторизация по токену. """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser,
            username=serializer.validated_data['username']
        )

        if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    """ Пользователи, доступ для админа. """
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path="me",
        serializer_class=CustomUserEditSerializer,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def profile(self, request):
        """ Выбор типа запроса. """
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """ Отзывы. Доступ на изменение - автор, администратор,
    модератор. Чтение - все. """
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """ Выбор создания или изменения. """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        """ Данные при GET запросе. """
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """ Коментарии. Доступ на изменение - автор, администратор,
    модератор. Чтение - все. """
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """ Выбор создания или изменения. """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        """ Данные при GET запросе. """
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
