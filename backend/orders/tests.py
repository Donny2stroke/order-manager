from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Product, Order, OrderProduct
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

"""
Tests for Order API endpoints, covering:
- Authentication
- Order creation with valid and invalid inputs
- Order update and retrieval
"""
class ExtendedOrderAPITestCase(APITestCase):

    """
    Common setup for all test cases:
    - Creates a test user and generates a JWT token.
    - Creates two example products in the database.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin123")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.product1 = Product.objects.create(name="Prodotto 1", price=10.50)
        self.product2 = Product.objects.create(name="Prodotto 2", price=5.00)

    """
    Test updating an existing order's products:
    - Create an order with product1
    - Update the order replacing it with product2
    - Verify product relation is updated
    """
    def test_update_order_products(self):
        #create an order with a single product
        url = reverse('order-list')
        create_data = {
            "name": "Ordine modificabile",
            "description": "da aggiornare",
            "date": str(date.today()),
            "products_data": [
                {"product_id": self.product1.id, "quantity": 1}
            ]
        }
        create_response = self.client.post(url, create_data, format='json', **self.auth_header)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        order_id = create_response.data["id"]

        # update order with another product
        update_url = reverse('order-detail', kwargs={"pk": order_id})
        update_data = {
            "name": "Ordine aggiornato",
            "description": "con prodotti diversi",
            "date": str(date.today()),
            "products_data": [
                {"product_id": self.product2.id, "quantity": 3}
            ]
        }
        update_response = self.client.put(update_url, update_data, format='json', **self.auth_header)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderProduct.objects.filter(order_id=order_id).count(), 1)
        self.assertEqual(OrderProduct.objects.get(order_id=order_id).product_id, self.product2.id)

    """
    Test creating an order referencing a non-existing product.
    Should fail with 400 BAD REQUEST.
    """
    def test_create_order_with_invalid_product(self):
        url = reverse('order-list')
        data = {
            "name": "Ordine errato",
            "description": "prodotto inesistente",
            "date": str(date.today()),
            "products_data": [
                {"product_id": 999, "quantity": 1}
            ]
        }
        response = self.client.post(url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test creating an order with a negative quantity.
    Should fail with 400 BAD REQUEST.
    """
    def test_create_order_with_invalid_quantity(self):
        url = reverse('order-list')
        data = {
            "name": "Ordine errato",
            "description": "quantità negativa",
            "date": str(date.today()),
            "products_data": [
                {"product_id": self.product1.id, "quantity": -1}
            ]
        }
        response = self.client.post(url, data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test retrieving an order detail with related products:
    - Creates an order linked to product1
    - Retrieves the order and validates that products are included
    """
    def test_get_order_details_returns_products(self):
        order = Order.objects.create(name="Dettaglio", description="test", date=date.today())
        OrderProduct.objects.create(order=order, product=self.product1, quantity=2)

        url = reverse('order-detail', kwargs={"pk": order.id})
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("products", response.data)
        self.assertEqual(len(response.data["products"]), 1)
        self.assertEqual(response.data["products"][0]["product"]["id"], self.product1.id)