from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    def __str__(self):
        return self.name

class Titles(models.Model):
    name = models.CharField('Текст поста', max_length=200)
    year = models.DateTimeField(db_index=True,)

    categories = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='title'
    )

    genres = models.ManyToManyField(
        Genres,
        through='genre_title',
        on_delete=models.SET_NULL,
        related_name='title'
        
    )
    
    class Meta:
        ordering = ("year",)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.text[:15]
    

    