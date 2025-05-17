from django.contrib import admin
from .models import Product, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
