from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Переопределена модель User
    Необходимо прописать валидатор
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        _('Логин'),
        max_length=150,
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        unique=False,
        blank=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        unique=False,
        blank=True,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
    )
    role = models.CharField(
        _('Роль пользователя'),
        max_length=150,
        default=USER,
        choices=CHOICES_ROLE,
    )
    confirmation_code = models.CharField(
        max_length=32,
        blank=True,
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('id',)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    def __str__(self) -> str:
        return self.username
