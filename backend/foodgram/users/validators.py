from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Никнейм "me" запрещён.'
        )
    return value