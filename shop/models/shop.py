from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from context.models import TimeStampMixin, CreatorMixin


def shop_icon_pth(_, filename):
    return f"shop/icons/{filename}"


class Shop(TimeStampMixin, CreatorMixin):

    class ShopStatus(models.TextChoices):
        WORK = "WORK"
        NOT_WORK = "NOT_WORK"

    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )
    is_active = models.BooleanField(default=True, verbose_name="Активность магазина")
    status = models.CharField(
        max_length=50, choices=ShopStatus.choices, default=ShopStatus.WORK
    )
    address = models.ForeignKey(
        "shop.Address",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Адресс",
    )
    icon = models.ImageField(
        upload_to=shop_icon_pth,  # путь в S3
        storage=S3Boto3Storage(),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_shop"
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    @classmethod
    def get_active_shops(cls):
        return cls.objects.filter(is_active=True)


class ShopReport(TimeStampMixin, CreatorMixin):
    name = models.CharField(verbose_name="Имя", blank=True, null=True, max_length=255)
    shop_name = models.CharField(
        verbose_name="Название магазина", blank=True, null=True, max_length=255
    )
    social_media = models.CharField(
        verbose_name="Социальная сеть", blank=True, null=True, max_length=255
    )
    portfolio = models.CharField(
        verbose_name="Портфолио", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_shop_report"
        verbose_name = "ShopReport"
        verbose_name_plural = "ShopReports"


class ShopWorkSchedules(TimeStampMixin, CreatorMixin):
    work_schedule = models.JSONField(verbose_name="Время работы", blank=True, null=True)

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_shop_work_schedules"
        verbose_name = "ShopWorkSchedules"
        verbose_name_plural = "ShopWorkSchedules"


class ShopRating(TimeStampMixin, CreatorMixin):
    product = models.ForeignKey(
        "shop.Shop",
        on_delete=models.CASCADE,
        verbose_name="Магазин",
        related_name="ratings",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка"
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_shop_rating"
        verbose_name = "ShopRating"
        verbose_name_plural = "ShopRating"
