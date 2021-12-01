from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from datetime import datetime


def max_value_this_year(value):
    return MaxValueValidator(
        datetime.now().year,
        'Нельзя добавить с такой датой.'
    )


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год издания',
        validators=[
            max_value_this_year,
            MinValueValidator(
                1,
                'Нельзя добавить с такой датой.'
            ),
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )
    description = models.TextField('Описание', blank=True,)

    class Meta:
        verbose_name = 'Произвдение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name
