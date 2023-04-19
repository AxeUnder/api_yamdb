import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from users.models import User

from reviews.models import Category, Comment, Genre, Review, Title

Models = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Импорт данных из csv файлов'

    def handle(self, *args, **options):
        pass
