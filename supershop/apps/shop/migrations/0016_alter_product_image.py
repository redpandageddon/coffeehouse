# Generated by Django 3.2 on 2022-01-13 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_product_to_sell'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
