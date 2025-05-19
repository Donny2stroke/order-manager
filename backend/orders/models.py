from django.db import models

# Represents a product that can be ordered    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True) # Used for soft delete logic

    def __str__(self):
        return self.name

# Represents a customer's order
class Order(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    # Many-to-many relationship with Product using an intermediate model
    products = models.ManyToManyField(Product, through='OrderProduct', related_name='orders')

    def __str__(self):
        return f"{self.name} - {self.date}"

# Intermediate model linking orders and products, with additional quantity field
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product') # Prevent duplicate product entries per order
