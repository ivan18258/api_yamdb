from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Review, Title, CustomUser

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Загрузка Review'

    def handle(self, *args, **kwargs):
        if Review.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading childrens data")

        for row in DictReader(open('static/data/review.csv', encoding="utf8")):
            child = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=CustomUser.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            child.save()
