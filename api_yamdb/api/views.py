from rest_framework import viewsets, filters, mixins
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Categories, Genres, Titles, Review, Comment
from .permissions import AuthorAdminModeratorOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'category', 'genre', 'name')


class CategoriesViewSet(viewsets.ViewSetMixin):
    queryset = Categories.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
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
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
