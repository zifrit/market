from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from context.models import TimeStampMixin, CreatorMixin


class Product(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )
    price = models.PositiveIntegerField(verbose_name="Цена", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    enabled = models.BooleanField(verbose_name="Включен", default=True)
    quantity = models.PositiveIntegerField(
        verbose_name="Количество", blank=True, null=True
    )
    external_id = models.CharField(
        verbose_name="Артикул товара", max_length=10, unique=True, db_index=True
    )
    color = models.ManyToManyField("Colors", verbose_name="Цвет", blank=True)
    brands = models.ForeignKey(
        "Brands",
        verbose_name="Бренды",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        "Categories",
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    sizes = models.ManyToManyField("Sizes", verbose_name="Размеры", blank=True)
    shop = models.ForeignKey(
        "shop.Shop",
        verbose_name="магазин",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    additional_data = models.JSONField(
        "Дополнительная информация", blank=True, null=True
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Colors(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )
    hex_color = models.CharField(
        verbose_name="Цвет", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_colors"
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return f"{self.name} {self.hex_color}"


class Brands(TimeStampMixin, CreatorMixin):
    key = models.CharField(blank=True, null=True, max_length=255)
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return f"{self.name} {self.key}"


class Categories(TimeStampMixin, CreatorMixin):
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Sizes(TimeStampMixin, CreatorMixin):
    class GenderType(models.TextChoices):
        MALE = "MALE", "Мужчина"
        FEMALE = "FEMALE", "Женщина"

    gender = models.CharField(
        max_length=10, choices=GenderType.choices, blank=True, null=True
    )
    name = models.CharField(
        verbose_name="Название", blank=True, null=True, max_length=255
    )

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_sizes"
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return f"{self.name} {self.gender}"


class ProductRating(TimeStampMixin, CreatorMixin):
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="ratings",
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка"
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_product_rating"
        verbose_name = "ProductRating"
        verbose_name_plural = "ProductRating"


class ProductHumanImages(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    human_image = models.ForeignKey("shop.HumanImage", on_delete=models.CASCADE)
    product_color = models.ForeignKey("shop.Colors", on_delete=models.CASCADE)
    product_image = models.ForeignKey("shop.ProductImages", on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        db_table = "clo_product_human_images"
        verbose_name = "ProductHumanImage"
        verbose_name_plural = "ProductHumanImages"


class HumanImage(TimeStampMixin, CreatorMixin):
    products = models.ManyToManyField(
        "shop.Product",
        related_name="human_image",
        verbose_name="Продукты",
        through="ProductHumanImages",
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    name = models.CharField(
        verbose_name="Название образа", blank=True, null=True, max_length=255
    )
    price = models.PositiveIntegerField(verbose_name="цена", blank=True, null=True)

    class Meta:
        ordering = ["created_at", "id"]
        db_table = "clo_human_images"
        verbose_name = "HumanImage"
        verbose_name_plural = "HumanImages"

    def __str__(self):
        return self.name
