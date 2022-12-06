from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Title, Categories

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Загрузка Title'

    def handle(self, *args, **kwargs):
        if Title.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading childrens data")

        for row in DictReader(open('static/data/titles.csv', encoding="utf8")):
            child = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Categories.objects.get(id=row['category'])
            )
            child.save()
