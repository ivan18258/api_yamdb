import re

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
    return value


def validate_emaill_username(value):
    """Проверка email на валидность."""
    email = value['email']
    username = value['username']
    a = reviews.models.CustomUser.objects.filter(email=email).exists()
    b = reviews.models.CustomUser.objects.filter(
        username=username).exists()
    c = reviews.models.CustomUser.objects.filter(
        username=value['username'], email=value['email']).exists()
    if (a or b) and not c:

        raise serializers.ValidationError(
            f'email {email} или username: {username} уже заняты'
            f', введите корректные данные, или'
            f'зарегистрируйтесь заново'
        )
    return value
