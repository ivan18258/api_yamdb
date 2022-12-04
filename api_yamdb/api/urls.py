from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitlesViewSet,
    CategoriesViewSet,

    GenresViewSet
    RegisterView,
    ReceivingJWTToken,
    CustomUserViewSet
)

routerV1 = DefaultRouter()
routerV1.register('titles', TitlesViewSet, basename='titles')
routerV1.register('categories', CategoriesViewSet, basename='categories')
routerV1.register('genres', GenresViewSet, basename='genres')
routerV1.register('users', CustomUserViewSet)
# routerV1.register('groups', GroupViewSet, basename='groups')
# routerV1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(routerV1.urls)),
    path('v1/auth/signup/', RegisterView.as_view()),
    path('v1/auth/token/', ReceivingJWTToken.as_view()),


]
