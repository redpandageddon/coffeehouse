from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Category, Cart, Customer, Product

class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        if isinstance(self.get_object(), Category):
            current_category = Category.objects.get(slug = self.get_object().slug)
            context['category_products'] = Product.objects.filter(category = current_category)
            context['categories'] = Category.objects.get_categories_for_sidebar()
        else:
            context['categories'] = Category.objects.get_categories_for_sidebar()
        return context

class CartMixin(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user = request.user).first()
            if not customer:
                customer = Customer.objects.create(user = request.user)
                customer.save()
            cart = Cart.objects.filter(customer = customer, in_order = False).first()
            if not cart:
                cart = Cart(product_amount = 0, final_price = 0, in_order = False)
                cart.save()
                cart.customer = customer
                cart.save()

        else:
            cart = Cart.objects.filter(for_anonymous_user = True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user = True)
                cart.save()
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)