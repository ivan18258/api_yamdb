from django.db import models
from django.core.exceptions import ValidationError
import datetime

def validate_year(value):
    now = datetime.datetime.now()
    now_year = now.year
    if value >int(now_year):
        raise ValidationError(
            ('Это произведение из будущего? Нет, не пойдет))'),
            params={'value': value},
        )

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

class Titles(models.Model):
    name = models.CharField('Произведение', max_length=256)
    year = models.PositiveIntegerField(db_index=True,validators=[validate_year])
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
        related_name='title',
        blank=True,
        null=True,
        
    )
    
    class Meta:
        ordering = ("year",)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]
