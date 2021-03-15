import random
import string

from . import models


def generate_unique_room_code(length: int=4) -> str:
    while True:
        code = ''.join(random.choices(string.ascii_letters, k=length))
        if models.Room.objects.filter(code=code).count() == 0:
            break
    return code