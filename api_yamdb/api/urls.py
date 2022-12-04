from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitlesViewSet,
    CategoriesViewSet,
    GenresViewSet
    )


routerV1 = DefaultRouter()
routerV1.register('titles', TitlesViewSet, basename='titles')
routerV1.register('categories', CategoriesViewSet, basename='categories')
routerV1.register('genres', GenresViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(routerV1.urls)),
    path('v1/', include('djoser.urls.jwt')),

]
