# Generated by Django 4.2.6 on 2023-10-11 05:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='count',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
