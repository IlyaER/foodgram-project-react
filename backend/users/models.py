from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    subscriptions = models.ManyToManyField(
        'User',
        through='recipes.Subscribe',
        symmetrical=False
    )

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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    @property
    def is_admin(self):
        return self.access == self.ADMIN

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
