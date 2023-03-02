import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Categories,
    Genres,
    Title,
    CustomUser,
    Comment,
    Review,
)
from .validators import validate_username


class GenresSerializer(serializers.ModelSerializer):
    """ Сериализация жанра. """
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    """ Сериализация категории. """
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Categories


class CategoryField(SlugRelatedField):
    """ Подготовка поля 'Категории' для сериализации"""
    def to_representation(self, value):
        serializer = CategoriesSerializer(value)
        return serializer.data


class GenreField(SlugRelatedField):
    """ Подготовка поля 'Жанр' для сериализации"""
    def to_representation(self, value):
        serializer = GenresSerializer(value)
        return serializer.data


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET запросах."""

    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    def validate_year(self, value):
        """ Валидация года выпуска произведения. """
        now = datetime.datetime.now()
        now_year = now.year
        if value > int(now_year):
            raise serializers.ValidationError(
                ('Это произведение из будущего? Нет, не пойдет))'),
                params={'value': value},
            )
        return value

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class SingUpSerializer(serializers.Serializer):
    """ Валидация полей модели кастомного пользователя"""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username]
    )
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):
    """ Сериализация аутентификации"""
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(max_length=150)


class CustomUserSerializer(serializers.ModelSerializer):
    """ Сериализация кастомного пользователя"""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
            validate_username
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all())
        ]
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class CustomUserEditSerializer(serializers.ModelSerializer):
    """ Сериализация кастомного пользователя (регистрация)"""
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализация отзыва. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        """ Проверка наличия отзыва от данного пользователя. """
        if not self.context['request'].method == 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(
            author=author,
            title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализация коментариев к отзыву. """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'
