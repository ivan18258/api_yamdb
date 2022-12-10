import re
from django.core.validators import validate_email

from rest_framework import serializers


def validate_username(value):
    regex = r'^[\w.@+-]+$'
    if re.match(regex, value) is None:
        raise serializers.ValidationError(
            "Вы использовали запрещенные символы!"
        )
    if value.lower() == 'me':
        raise serializers.ValidationError(
            "Username 'me' использовать нельзя"
        )
    return value


def validate_emailll(value):
    """Проверка email на валидность."""
    try:
        validate_email(value)
    except serializers.ValidationError as error:
        raise serializers.ValidationError(
            f'Email не валидно: {error}'
        )
    return value
