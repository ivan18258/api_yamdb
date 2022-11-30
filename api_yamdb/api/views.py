from rest_framework import viewsets, filters, mixins
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TitlesSerializer
)
from reviews.models import Categories, Genres, Titles


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year', 'category', 'genre', 'name')


class CategoriesViewSet(viewsets.ViewSetMixin):
    queryset = Categories.objects.all()
