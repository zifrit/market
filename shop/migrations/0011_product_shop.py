# Generated by Django 5.1.7 on 2025-04-08 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_product_category_remove_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop', verbose_name='магазин'),
        ),
    ]
