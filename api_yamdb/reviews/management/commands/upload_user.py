from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import CustomUser

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Загрузка User'

    def handle(self, *args, **kwargs):
        if CustomUser.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading childrens data")

        for row in DictReader(open('static/data/users.csv')):
            child = CustomUser(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role']
            )
            child.save()
