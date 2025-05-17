from django.db import models
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    products = models.ManyToManyField(Product, through='OrderProduct', related_name='orders')

    def __str__(self):
        return f"{self.name} - {self.date}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')
