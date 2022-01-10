from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.urls.base import reverse
from .services.category_services import CategoryManager
from io import BytesIO
from django.utils import timezone
import sys



# Получение модели для пользователя
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        reverse('shop:customer__detail', kwargs= {'username' : self.user.username})

    class Meta:
        verbose_name = 'Покупатели'
        verbose_name_plural = 'Покупатели'
        db_table = 'customer_profiles'

# Модель для категории товара
class Category(models.Model):

    name = models.CharField('Название категории', max_length = 100)
    slug = models.SlugField(unique = True)
    description = models.TextField('Описание', blank=True, null=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category__detail', kwargs = { 'slug' : self.slug })

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'product_categories'


# Модель для товара
class Product(models.Model):

    min_resolution = (400, 400)
    max_resolution = (1000, 1000)
    max_image_size = 3145728

    name = models.CharField('Название продукта', max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField('Цена товара', decimal_places=2, max_digits=8)
    description = models.TextField('Описание товара', null=True, blank=True)
    image = models.ImageField()
    to_sell = models.BooleanField('Продвигать', default=False)

    # Получение url для продукта
    def get_absolute_url(self):
        return reverse('shop:product', kwargs = {'slug' : self.slug})

    def get_five_altest_products(self=None):
        return Product.objects.all().order_by('-id')[:5]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'products'

    # Работа с изображением продукта (сохранение в нужной директории, ограничение размеров)
    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        new_img = new_img.resize((self.max_resolution))
        filestream = BytesIO()
        new_img.save(filestream, 'JPEG', quality = 90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None)
        super().save(*args, **kwargs)


    def get_model_name(self):
        return self.__class__._meta.model_name


# Модель для пользователя
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    address = models.CharField('Адрес доставки', max_length = 255, null = True)
    orders = models.ManyToManyField('Order', verbose_name = 'Заказы покупателя', related_name = 'related_customer')

    def __str__(self):
        return 'Покупатель {} {}'.format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        db_table = 'customers'  


# Модель для товара в корзине
class Cart_Product(models.Model):

    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, related_name = 'related_products')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    amount = models.PositiveIntegerField('Количество', default = 1)
    final_price = models.DecimalField('Итоговая сумма', default = 0, max_digits = 8, decimal_places = 2)

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
        db_table = 'cart_products'

    def save(self, *args, **kwargs):
        self.final_price = self.amount * self.product.price
        super().save(*args, **kwargs)


# Модель для корзины
class Cart(models.Model):
    
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
    products = models.ManyToManyField(Cart_Product, blank = True, related_name = 'related_cart')
    product_amount = models.PositiveIntegerField('Количество продуктов', default = 0)
    final_price = models.DecimalField('Итоговая сумма', default = 0, max_digits = 8, decimal_places = 2)
    in_order = models.BooleanField(default = False)
    for_anonymous_user = models.BooleanField(default = False)

    def __str__(self):
        return 'Корзина для покупателя: {}'.format(self.customer)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        db_table = 'carts'

    def save(self, *args, **kwargs):
        if self.id:
            cart_data = self.products.aggregate(models.Sum('final_price'), models.Sum('amount'))
            if cart_data.get('final_price__sum'):
                self.final_price = cart_data['final_price__sum']
            else:
                self.final_price = 0
            if cart_data.get('amount__sum'):
                self.product_amount = cart_data['amount__sum']
            else:
                self.product_amount = 0
        super().save(*args, **kwargs)


# Модель для заказа
class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOISES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ завершен')
    )

    order_at = models.DateTimeField(auto_now = True)
    order_date = models.DateField('Дата заказа', default = timezone.now)
    status = models.CharField(max_length = 255, verbose_name = 'Статус заказа', choices = STATUS_CHOISES, default = STATUS_NEW)
    cart = models.ForeignKey('Cart', null = True, blank = True, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE, related_name = 'related_orders')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders'
