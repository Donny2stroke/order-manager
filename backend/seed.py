from orders.models import Product, Order, OrderProduct
from datetime import date

# Create products
p1 = Product.objects.create(name="Samsung Galaxy S25 Edge", price=1299.00)
p3 = Product.objects.create(name="Samsung Galaxy A56 5G", price=399.00)
p2 = Product.objects.create(name="Apple iPhone 16 Pro Max", price=1120.80)
p2 = Product.objects.create(name="Apple iPhone 15 Pro", price=939.20)

# Create orders
o1 = Order.objects.create(name="Mario Rossi Order", description="Firs order for Mario Rossi", date=date.today())
o2 = Order.objects.create(name="Giuseppe Verdi Order", description="Firs order for Giuseppe Verdi", date=date.today())

# Link products to orders with quantities
OrderProduct.objects.create(order=o1, product=p1, quantity=1)
OrderProduct.objects.create(order=o1, product=p2, quantity=2)

OrderProduct.objects.create(order=o2, product=p2, quantity=1)
OrderProduct.objects.create(order=o2, product=p3, quantity=1)

print("Seed completed: products and orders created.")
