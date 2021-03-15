from django.db import models

from .services import generate_unique_room_code


class Room(models.Model):
    code = models.CharField(
        max_length=8, default=generate_unique_room_code, unique=True)
    host = models.CharField(max_length=64, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip_song = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'room'

    def __str__(self):
        return self.code