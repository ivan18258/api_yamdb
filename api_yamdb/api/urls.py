from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitlesViewSet, CategoriesViewSet, RegisterView, ReceivingJWTToken, CustomUserViewSet


routerV1 = DefaultRouter()
routerV1.register('titles', TitlesViewSet, basename='titles')
routerV1.register('categories', CategoriesViewSet, basename='categories')
routerV1.register('users', CustomUserViewSet)
# routerV1.register('groups', GroupViewSet, basename='groups')
# vrouterV1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(routerV1.urls)),
    path('v1/auth/singup/', RegisterView.as_view()),
    path('v1/auth/token/', ReceivingJWTToken.as_view()),
    # path('v1/', include('djoser.urls.jwt')),
]
