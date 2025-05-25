from django.conf import settings
from django.db import models

from context.models import CreateUpdateTimeMixin


class CustomUserFavoriteProduct(CreateUpdateTimeMixin):
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Продукт",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_custom_user_favorite_product"
        verbose_name = "CustomUserFavoriteProduct"
        verbose_name_plural = "CustomUserFavoriteProducts"
