from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


SCORE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
)


# Пока создал пустые шаблоны моделей
class Category(models.Model):
    pass

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    pass

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        'Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст отзыва',
        blank=False,
        null=False,
        help_text='Напишите свой отзыв.'
    )
    author = models.ForeignKey(
        User,
        'Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        blank=False,
        null=False,
        choices=SCORE_CHOICES,
        help_text='Дайте оценку произведению.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
