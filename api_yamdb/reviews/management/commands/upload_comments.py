from django.core.management.base import BaseCommand
from csv import DictReader

from reviews.models import Comment, Review, CustomUser

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    help = 'Загрузка Comment'

    def handle(self, *args, **kwargs):
        if Comment.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading childrens data")

        f = 'static/data/comments.csv'
        for row in DictReader(open(f, encoding="utf8")):
            child = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=CustomUser.objects.get(id=row['author']),
                pub_date=row['pub_date']
            )
            child.save()
