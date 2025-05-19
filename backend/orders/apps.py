from django.apps import AppConfig

# Configuration class for the "orders" application
class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Defines the name of the Django app
    name = 'orders'
