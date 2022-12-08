import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    now = datetime.datetime.now()
    now_year = now.year
    if value > int(now_year):
        raise ValidationError(
            ('Это произведение из будущего? Нет, не пойдет))'),
            params={'value': value},
        )
