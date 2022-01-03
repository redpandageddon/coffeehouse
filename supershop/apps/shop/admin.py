from django.contrib import admin
from .models import *
from django.forms import ModelForm
from django.utils.safestring import mark_safe

class ProductAdminForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            """<span style = "color: red; font-size: 12px; ">При загрузке изображения больше {} x {} оно будет обрезано!</span>""".format( 
            *Product.max_resolution
        ))


class ProductAdminModel(admin.ModelAdmin):

    form = ProductAdminForm

# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdminModel)
admin.site.register(Factory)
admin.site.register(Storage_Conditions)
admin.site.register(Customer)
admin.site.register(Cart_Product)
admin.site.register(Cart)
admin.site.register(Order)