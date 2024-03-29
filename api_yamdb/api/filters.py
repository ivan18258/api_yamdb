from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitlesFilter(filters.FilterSet):
    """ Фильтр для полей модели 'Произведения'"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in'
    )
    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
