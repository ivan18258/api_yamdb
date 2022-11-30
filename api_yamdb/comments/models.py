from django.db import models
from users.models import CustomUser
from reviews.models import Titles, Review


class Review(models.Model):
    title_id = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    score = models.IntegerField(
        help_text="Оставьте оценку произведению в диапазоне от одного до десяти")
	
    def __str__(self):
        return self.text

    class Meta:
        unique_together = ["title_id", "author"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
		on_delete=models.CASCADE,
		related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
		on_delete=models.ForeignKey,
		related_name="comments"
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
		auto_now_add=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"