import django_filters
from shop.models import Product


class ProductFilter(django_filters.rest_framework.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Минимальная цена"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Максимальная цена"
    )

    class Meta:
        model = Product
        fields = [
            "enabled",
            "shop_id",
            "brands_id",
            "category_id",
            "quantity",
            "price",
        ]
