from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product, Customer, Cart_Product, User, UserProfile
from .forms import LoginForm, RegistrationForm, OrderForm
from .models import Category
from .mixins import CartMixin, CategoryDetailMixin
from .services.product_services import get_to_sell_products
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProductSerializer, CategorySerializer


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect('/shop/login')

        latest_products = get_to_sell_products()
        categories = Category.objects.get_categories_for_sidebar()
        context = {
            'categories' : categories,
            'latest_products' : latest_products,
            'cart' : self.cart
        }
        return render(request, 'base.html', context)


class ManagerBaseView(View):

    def get(self, request, *args, **kwargs):
        customers = User.objects.filter(is_staff = False)
        context = {
            'customers' : customers
        }
        return render(request, 'manager.html', context)


class CustomerDetailView(DetailView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    context_object_name = 'user'
    template_name = 'customer__detail.html'
    slug_url_kwarg = 'slug'


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    
    CT_MODEL_MODEL_CLASS = {
        'product' : Product,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    model = None
    queryset = None
    context_object_name = 'product'
    template_name = 'product__detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


# Представление для авторизации
class LoginView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = { 'form' : form, 
                    'categories' : categories,
                    'cart' : self.cart
                } 
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/shop')
        context = {

                    'form' : form
                }
        return render(request, 'login.html', context)


# Представление для регистрации
class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwasrgs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'form' : form,
            'categories' : categories,
            'cart' : self.cart
        }
        return render(request,'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            c = Customer.objects.create(
                user = new_user,
                address = form.cleaned_data['address']
            )
            c.save()
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/shop')

        context = {
            'form' : form
        }

        return render(request, 'registration.html', context)


# Представление для деталей категории
class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category__detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


# Представление для корзины
class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_sidebar()
        context = {
            'cart' : self.cart,
            'categories' : categories
        }
        return render(request, 'cart.html', context)


# Представление для добавления товара в корзину
class AddToCartView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        product = Product.objects.get(slug = product_slug)

        cart_product, created  = Cart_Product.objects.get_or_create(
            customer = self.cart.customer,
            cart = self.cart,
            product = product
        )
        if(created):
            self.cart.products.add(cart_product)
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        return HttpResponseRedirect('/shop/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        product = Product.objects.get(slug = product_slug)
        cart_product  = Cart_Product.objects.get(
            customer = self.cart.customer,
            cart = self.cart,
            product = product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect('/shop/cart/')


class ChangeAmountView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        product = Product.objects.get(slug = product_slug)
        cart_product  = Cart_Product.objects.get(
            customer = self.cart.customer,
            cart = self.cart,
            product = product
        )
        cart_product.amount = int(request.POST.get('amount'))
        cart_product.save()
        self.cart.save()
        messages.add_message(request, messages.INFO, 'Количество товара успешно изменено')
        return HttpResponseRedirect('/shop/cart/')


# Представление для оформления заказа
class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart' : self.cart,
            'categories' : categories,
            'form' : form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user = request.user)
        if form.is_valid():
            new_order = form.save(commit = False)
            new_order.customer = customer
            new_order.order_date = form.cleaned_data['order_date']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ')
            return HttpResponseRedirect('/shop/')
        return HttpResponseRedirect('/shop/checkout/')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer