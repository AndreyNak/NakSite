from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    banned = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.user.username} Profile'
