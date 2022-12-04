from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidato

from reviews.models import Categories, Genres, Titles, CustomUser


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True, read_only=True)
    category = SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category',)
        model = Titles


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")


class CustomUserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        read_only_fields = ('role')
