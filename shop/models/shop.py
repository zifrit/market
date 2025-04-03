from django.db import models

from context.models import TimeStampMixin, CreatorMixin


class Shop(TimeStampMixin, CreatorMixin):

    class ShopStatus(models.TextChoices):
        WORK = 'WORK'
        NOT_WORK = 'NOT_WORK'

    name = models.CharField(verbose_name='Название', blank=True, null=True, max_length=255)
    is_active = models.BooleanField(default=True, verbose_name='Активность магазина')
    status = models.CharField(max_length=50, choices=ShopStatus.choices, default=ShopStatus.WORK)


    class Meta:
        ordering = ['created_at', 'id']
        db_table = 'clo_shop'
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    @classmethod
    def get_active_shops(cls):
        return cls.objects.filter(is_active=True)