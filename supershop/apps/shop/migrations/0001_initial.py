# Generated by Django 3.2 on 2021-05-13 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_amount', models.PositiveIntegerField(default=0, verbose_name='Количество продуктов')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Итоговая сумма')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
                'db_table': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Categoty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'product_categories',
            },
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('inn', models.CharField(max_length=10, verbose_name='ИНН')),
            ],
            options={
                'verbose_name': 'Произодитель',
                'verbose_name_plural': 'Производители',
                'db_table': 'factories',
            },
        ),
        migrations.CreateModel(
            name='Storage_Conditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Температура')),
                ('humidity', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='Влажность воздуха')),
            ],
            options={
                'verbose_name': 'Условия хранения',
                'verbose_name_plural': 'Условия хранения',
                'db_table': 'storage_conditions',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('slug', models.SlugField(unique=True)),
                ('best_before', models.DateField(verbose_name='Срок годности')),
                ('export_date', models.DateField(verbose_name='Дата производства')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена товара')),
                ('desciption', models.TextField(verbose_name='Описание товара')),
                ('image', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.categoty')),
                ('factory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.factory')),
                ('storage_conditions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.storage_conditions')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес доставки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Cart_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Итоговая сумма')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='shop.cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукты в корзине',
                'db_table': 'cart_products',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='shop.Cart_Product'),
        ),
    ]