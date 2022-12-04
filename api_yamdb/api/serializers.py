from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidato

from reviews.models import Categories, Comment, Genres, Review, Titles


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


class ReviewSerializer(serializers.ModelSerializer):
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
        if self.context['request'].method != 'POST':
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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
