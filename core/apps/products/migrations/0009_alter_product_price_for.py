# Generated by Django 5.2.1 on 2025-06-08 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_bonus_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_for',
            field=models.CharField(choices=[('кг.', 'кг.'), ('шт.', 'шт.'), ('литр', 'литр'), ('метр', 'метр')], default='шт', max_length=500, verbose_name='Цена за'),
        ),
    ]
