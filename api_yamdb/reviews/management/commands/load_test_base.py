from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загрузка базы данных'

    def handle(self, *args, **kwargs):
        call_command('upload_user')
        call_command('upload_category')
        call_command('upload_genres')
        call_command('upload_titles')
        call_command('upload_review')
        call_command('upload_comments')
