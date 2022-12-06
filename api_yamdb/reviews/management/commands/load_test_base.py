from django.core.management.base import BaseCommand
import os
from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Загрузка базы данных'

    def handle(self, *args, **kwargs):
        os.system('E:/Dev/aaa/api_yamdb/api_yamdb/reviews/management/commands/upload_user.py')
        # os.open(BASE_DIR, 'reviews/management/commands/upload_user.py')
        # os.path.join(BASE_DIR, 'reviews/management/commands/upload_user.py')