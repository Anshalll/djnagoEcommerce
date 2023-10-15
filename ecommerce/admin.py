from django.contrib import admin
from .models import Product, ProductCat, Users, Cart




admin.site.register(Product)
admin.site.register(ProductCat)
admin.site.register(Users)
admin.site.register(Cart)