from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
# from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    TitlesSerializer,
    CategoriesSerializer,
    GenresSerializer,
    SingUpSerializer,
    TokenSerializer,
    CustomUserSerializer,
    CustomUserEditSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    AuthorAdminModeratorOrReadOnly,
    AuthorAdminModeratorOrReadOnly
)

from reviews.models import(
  Categories,
  Genres,
  Titles,
  CustomUser,
  Review,
  Comment,
)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'category', 'genre', 'name')
    pagination_class = LimitOffsetPagination


    

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

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
    permission_classes = (IsAdmin,)

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        serializer_class=CustomUserEditSerializer,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def profile(self, request):
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



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title'))
        return title.reviews.all()

    def calculate_average_rating():
        score = Review.objects.filter(score=True)
        sum_of_raiting = 0
        count = 0
        for score in score.reviews.all():
            count += score.count()
            sum_of_raiting += score
        if count > 0:
            raiting = round(sum_of_raiting / count)
            return raiting
        else:
            return None


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review'))
        return review.comments.all()

