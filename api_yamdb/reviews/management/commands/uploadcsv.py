from django.core.management.base import BaseCommand
import csv
from reviews.models import (
    Categories,
    Genres,
    Title,
    Review,
    CustomUser,
    Comment,)

from reviews.csv_model import (
    Categories_csv,
    Genres_csv,
    Titles_csv,
    Review_csv,
    CustomUser_csv,
    Comment_csv,
)


class Command(BaseCommand):
    help = 'загрузка бд тестовыми данными'

    """def handle(self, *args, **options):
        
        with open('static/data/comments.csv', 'r') as f:
            reader = csv.reader(f)
            print(reader)
            list=[]
            for row in reader:
                list.append(Comment_csv(row))

            Comment.objects.bulk_create (list)
            print(list)"""

    def handle(self, *args, **options):
        with open('static/data/titles.csv', 'r') as f:
            reader = list(csv.reader(f))
            print(reader)
            reader.pop(0)
            print(reader)
            list1=[]
            for row in reader:
                list.append(Titles_csv(row))
            Title.objects.bulk_create(list1)
            print('обьекты '+list1)
