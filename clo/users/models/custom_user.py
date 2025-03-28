from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from context.models import TimeStampMixin, CreatorMixin


class CustomUserManager(UserManager):

    def create_user(self, phone_number, password=None, **kwargs):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def all(self):
        return self.filter(is_superuser=False)

    def active(self):
        return self.filter(is_active=True, is_superuser=False)


class CustomUser(AbstractUser, TimeStampMixin):
    """Расширенный базовый пользователь"""

    first_name = models.CharField(max_length=255, verbose_name='Фамилия', blank=True)
    last_name = models.CharField(max_length=255, verbose_name='Имя', blank=True)
    middle_name = models.CharField(max_length=255, verbose_name='Отчество', blank=True)
    fio = models.CharField(max_length=255, verbose_name='ФИО', blank=True)
    email = models.EmailField(verbose_name='Майл', unique=True)
    phone = models.CharField(max_length=18, unique=True, verbose_name='Номер телефона')

    objects = CustomUserManager()

    class Meta:
        ordering = ['id']
        db_table = 'custom_user'
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.middle_name)
        return full_name.strip()

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username
