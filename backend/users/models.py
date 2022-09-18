from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USERROLES = [
        (USER, 'User'),
        (ADMIN, 'Admin')
    ]
    access = models.CharField(
        'Доступы',
        max_length=20,
        choices=USERROLES,
        default=USER
    )

    # @property
    # def is_admin(self):
    #     return self.access == self.ADMIN

    class Meta:
        ordering = ('pk',)

