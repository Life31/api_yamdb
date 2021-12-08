from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from enum import Enum

from titles.models import Title
from users.models import MyUser as User


class Review(models.Model):

    class MARKS(Enum):
        ONE = (1, '1 балл')
        TWO = (2, '2 балла')
        THREE = (3, '3 балла')
        FOUR = (4, '4 балла')
        FIVE = (5, '5 баллов')
        SIX = (6, '6 баллов')
        SEVEN = (7, '7 баллов')
        EIGHT = (8, '8 баллов')
        NINE = (9, '9 баллов')
        TEN = (10, '10 баллов')

        @classmethod
        def list(cls):
            return list(map(lambda c: c.value, cls))

    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва')
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва')
    score = models.CharField(
        max_length=1,
        choices=MARKS.list(),
        verbose_name='Оценка произведения',
        validators=(
            MaxValueValidator(
                10, 'Оценка не может быть более 10.'),
            MinValueValidator(
                1, 'Оценка не может быть менее 1.'),
        ),
        null=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-title', '-id')
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'),)

    def __str__(self):
        return f'{self.author}: {self.text[:40]}'


class Comment(models.Model):
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(
        verbose_name='Комментарий')
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментирования')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-review', '-id',)

    def __str__(self):
        return f'{self.author}: {self.text[:40]}'
