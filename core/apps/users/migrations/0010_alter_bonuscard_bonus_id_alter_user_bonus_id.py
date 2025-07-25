# Generated by Django 5.2.3 on 2025-07-17 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_bonuscard_bonus_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonuscard',
            name='bonus_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.bonusid', verbose_name='Уникальный номер карты'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bonus_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_bonus', to='users.bonuscard'),
        ),
    ]
