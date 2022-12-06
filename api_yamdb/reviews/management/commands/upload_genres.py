from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Genres

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Загрузка Genres'

    def handle(self, *args, **kwargs):
        if Genres.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading childrens data")

        for row in DictReader(
            open('static/data/genre.csv', encoding="utf8")
        ):
            child = Genres(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            child.save()
