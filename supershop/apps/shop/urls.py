from django.urls import path, re_path, include
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)


app_name = 'shop'
urlpatterns = [
    path('', views.BaseView.as_view(), name = 'base'),
    path('products/<str:ct_model>/<str:slug>/', views.ProductDetailView.as_view(), name = 'product__detail'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('registration/', views.RegistrationView.as_view(), name = 'registration'),
    path('logout/', LogoutView.as_view(next_page = '/shop/'), name = 'logout'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name = 'category__detail'),
    re_path(r'^products/product/(?P<slug>[\w\d\-\_]+)/$', views.ProductDetailView.as_view(), name = 'product'),
    path('cart/', views.CartView.as_view(), name = 'cart'), 
    path('add_to_cart/<str:ct_model>/<str:slug>/', views.AddToCartView.as_view(), name = 'add_to_cart'),
    path('remove_from_cart/<str:ct_model>/<str:slug>/', views.DeleteFromCartView.as_view(), name = 'remove_from_cart'), 
    path('change_amount/<str:ct_model>/<str:slug>/', views.ChangeAmountView.as_view(), name = 'change_amount'),
    path('checkout/', views.CheckoutView.as_view(), name = 'checkout'),
    path('make_order/', views.MakeOrderView.as_view(), name = 'make_order'),
    path('manager/', views.ManagerBaseView.as_view(), name='manager'),
    re_path(r'^customers/customer/(?P<pk>[\w\d\-\_]+)/$', views.CustomerDetailView.as_view(), name = 'customer'),
    path('api/', include(router.urls))
]