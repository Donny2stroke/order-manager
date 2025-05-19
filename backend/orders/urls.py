from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet
from orders.views import api_home

# Router configuration for automatic route generation
router = DefaultRouter()

# Register the Order and Product endpoints under the 'orders' and 'products' routes
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
