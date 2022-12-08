from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet,
    CategoriesViewSet,
    GenresViewSet,
    RegisterView,
    ReceivingJWTToken,
    CustomUserViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

routerV1 = DefaultRouter()
routerV1.register(r'titles', TitleViewSet, basename='titles')
routerV1.register('categories', CategoriesViewSet, basename='categories')
routerV1.register('genres', GenresViewSet, basename='genres')
routerV1.register('users', CustomUserViewSet)
routerV1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments',
    CommentViewSet,
    basename='comments'
)
routerV1.register(
    r'titles/(?P<title_id>[1-9]\d*)/reviews',
    ReviewViewSet,
    basename='reviews'
)
auth = [
    path('signup/', RegisterView.as_view()),
    path('token/', ReceivingJWTToken.as_view()),
]

urlpatterns = [
    path('v1/', include(routerV1.urls)),
    path('v1/auth/', include(auth))
]
