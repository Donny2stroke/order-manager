from django.contrib import admin
from django.urls import path, include
from orders.views import api_home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    # Root route: basic HTML homepage for API navigation
    path('', api_home),
    # Django admin panel
    path('admin/', admin.site.urls),
    # Include all API routes defined in the orders app
    path('api/', include('orders.urls')),
    # JWT token authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # OpenAPI schema and Swagger documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

