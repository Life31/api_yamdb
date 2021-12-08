from django.db.models import Avg
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (
    CurrentUserDefault,
    SerializerMethodField,
    ModelSerializer,
    ValidationError)

from datetime import datetime

from titles.models import Category, Genre, Title
from reviews.models import Comment, Review


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')
        model = Title

    def validate_year(self, year):
        if year > datetime.now().year:
            raise ValidationError(
                'Нельзя добавить с такой датой.')
        return year

    def get_rating(self, obj):
        return obj.reviews.aggregate(average=Avg('score'))['average']


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'pub_date')

    def validate_score(self, score):
        if score < 1 or score > 10:
            return ValidationError('Оценка должна быть от 1 до 10')
        return score

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        author = request.user
        if Review.objects.values(
            'author', 'title').filter(
                author=author, title__id=title_id).exists():
            raise ValidationError('Отзыв уже написан.')
        return data
