# Generated by Django 3.2 on 2022-01-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20220107_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='to_sell',
            field=models.BooleanField(default=False, verbose_name='Продвигать'),
        ),
    ]
