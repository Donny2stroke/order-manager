from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ProductViewSet
from orders.views import api_home

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
