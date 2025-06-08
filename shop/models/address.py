from django.db import models

from context.models import TimeStampMixin, CreatorMixin


class Address(TimeStampMixin, CreatorMixin):
    address = models.CharField(
        verbose_name="Адрес", blank=True, null=True, max_length=255
    )
    coordinate = models.JSONField(verbose_name="Координаты", blank=True, null=True)

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address
