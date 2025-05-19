from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer
from django.http import HttpResponse


# Public homepage with a basic HTML interface for API overviewdef api_home(request):
def api_home(request):
    return HttpResponse("""
        <html>
        <head>
            <title>Order Manager API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 2rem;
                    background: #f4f4f4;
                }
                .container {
                    width: 100%;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                h1 {
                    color: #41737a;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 1rem 0;
                    font-size: 1.2rem;
                }
                a {
                    text-decoration: none;
                    color: #0d6efd;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Order Manager API</h1>
                <p>Welcome! Below you will find the main endpoints:</p>
                <ul>
                    <li><a href="/admin">Admin Area</a></li>
                    <li><a href="/api/docs">Swagger UI (documentation)</a></li>
                    <li><a href="/api/schema">Api Schema Json(jwt required)</a></li>
                </ul>   
            </div>
        </body>
        </html>
    """)

"""
Provides full CRUD API for managing Orders.
Includes filtering by date and search on name/description.
"""
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-date')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['date']

"""
Provides full CRUD API for managing Products.
Overrides the delete behavior to perform a soft delete (is_active = False).
"""
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
    
    """
    Soft delete the product by setting is_active = False
    instead of removing the record from the database.
    """
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
