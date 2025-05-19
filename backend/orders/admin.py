from django.contrib import admin
from .models import Product, Order, OrderProduct

# Inline editing for the intermediate OrderProduct model inside Order admin
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

# Custom admin configuration for Order model
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

# Register Product model with default admin interface
admin.site.register(Product)

# Register Order model with custom admin that includes OrderProduct inlines
admin.site.register(Order, OrderAdmin)
