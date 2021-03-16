from django.db import models
from django.utils.crypto import get_random_string


def generate_unique_room_code(length: int=4) -> str:
    while True:
        code = get_random_string(length=length)
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_room_code, unique=True)
    host = models.CharField(max_length=64, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip_song = models.PositiveIntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room'

    def __str__(self):
        return self.code
    


