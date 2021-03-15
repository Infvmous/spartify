from typing import NoReturn

from django.utils.crypto import get_random_string

from . import models


def generate_unique_room_code(length: int=4) -> str:
    while True:
        code = get_random_string(length=length)
        if models.Room.objects.filter(code=code).count() == 0:
            break
    return code



