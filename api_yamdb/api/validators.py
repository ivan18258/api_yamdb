import re
from django.core.validators import validate_email

from rest_framework import serializers

import reviews.models


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
    if reviews.models.CustomUser.objects.filter(username=value).exists():
        raise serializers.ValidationError(
            'Это имя уже использовано'
        )
    return value


def validate_emaill(value):
    """Проверка email на валидность."""
    if reviews.models.CustomUser.objects.filter(email=value).exists():
        raise serializers.ValidationError(
            'Этот email уже использовано'
        )
    # try:
    #     validate_email(value)
    # except serializers.ValidationError as error:
    #     raise serializers.ValidationError(
    #         f'Email не валидно: {error}'
    #     )
    return value
