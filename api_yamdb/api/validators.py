import re

from rest_framework import serializers


def validate_username(value):
    """ Валидатор имени пользователя. """
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
