from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitlesViewSet,
    CategoriesViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

routerV1 = DefaultRouter()
routerV1.register('titles', TitlesViewSet, basename='titles')
routerV1.register('categories', CategoriesViewSet, basename='categories')
routerV1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewViewSet,
    basename='reviews'
)
routerV1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('api/v1/', include(routerV1.urls)),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
