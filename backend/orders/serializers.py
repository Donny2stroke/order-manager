from rest_framework import serializers
from .models import Order, Product, OrderProduct

# Serializer for Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'is_active']


# Serializer for writing OrderProduct entries (used in order creation/update)
class OrderProductWriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

# Serializer for reading OrderProduct entries (used in order detail view)
class OrderProductReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer() # Nested representation of the product

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

# Serializer for Order model including product relationships
class OrderSerializer(serializers.ModelSerializer):
    # Read-only field to list associated products
    products = OrderProductReadSerializer(source='orderproduct_set', many=True, read_only=True)
    # Write-only field used to submit product IDs and quantities
    products_data = OrderProductWriteSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'name', 'description', 'date', 'products', 'products_data']

    # Custom create logic to handle many-to-many relationship through intermediate table
    def create(self, validated_data):
        products_data = validated_data.pop('products_data', [])
        order = Order.objects.create(**validated_data)

        for item in products_data:
            product_id = item['product_id']
            quantity = item['quantity']

            # Validation: quantity must be positive
            if quantity <= 0:
                raise serializers.ValidationError(f"Quantity must be greater than 0 (got {quantity})")
            # Validation: product must exist
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist")
            # Create the relation with quantity
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        return order
    
    # Custom update logic to override existing products in the order
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products_data', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if products_data:
            # Clear old product relations and rebuild them
            instance.orderproduct_set.all().delete()
            for item in products_data:
                product_id = item['product_id']
                quantity = item['quantity']

                if quantity <= 0:
                    raise serializers.ValidationError(f"Quantity must be greater than 0 (got {quantity})")

                try:
                    product = Product.objects.get(pk=product_id)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(f"Product with id {product_id} does not exist")

                OrderProduct.objects.create(order=instance, product=product, quantity=quantity)

        return instance
