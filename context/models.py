from django.db import models


class CreateUpdateTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    class Meta:
        abstract = True


class DeleteTimeMixin(models.Model):
    delete = models.DateTimeField(verbose_name='Время удаления', blank=True, null=True)

    class Meta:
        abstract = True


class TimeStampMixin(CreateUpdateTimeMixin, DeleteTimeMixin):
    class Meta:
        abstract = True


class CreatorMixin(models.Model):
    creator = models.ForeignKey('users.CustomUser', on_delete=models.PROTECT, verbose_name='Создатель',
                                null=True, blank=True)
    class Meta:
        abstract = True