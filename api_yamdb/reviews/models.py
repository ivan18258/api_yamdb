from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.contrib.auth.models import AbstractUser

from api.validators import validate_username
from .validators import validate_year


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Аутентифицированный пользователь'),
    ]

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        'О себе',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
        )

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField('Категория', max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField('Жанр', max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Произведение', max_length=256)
    year = models.IntegerField(
        db_index=True,
        validators=[validate_year]
    )
    description = models.CharField('Описание', max_length=500, null=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='title',
        blank=True,
        null=True,
    )

    genre = models.ManyToManyField(
        Genres,
        related_name='title_genre',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class BaseReviewComment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['pub_date']

    def __str__(self):
        return self.text


class Review(BaseReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    score = models.IntegerField(
        verbose_name='Оценка',
        null=True,
        validators=[
            MaxValueValidator(
                limit_value=10,
                message='Не более 10'
            ),
            MinValueValidator(
                limit_value=1,
                message='Не менее 1'
            )
        ],
        help_text=(
            'Оставьте оценку произведению в диапазоне от одного до десяти'
        )
    )

    class Meta:
        unique_together = ['title', 'author']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(BaseReviewComment):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
