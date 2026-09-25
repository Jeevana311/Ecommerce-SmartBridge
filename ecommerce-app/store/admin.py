from django.contrib import admin
from .models import Category, Product, Order, OrderItem, OrderRequest


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderRequest)