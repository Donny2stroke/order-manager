from rest_framework import serializers
from .models import Order, Product, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'is_active']

class OrderProductWriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderProductReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductReadSerializer(source='orderproduct_set', many=True, read_only=True)
    products_data = OrderProductWriteSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'name', 'description', 'date', 'products', 'products_data']

    def create(self, validated_data):
        products_data = validated_data.pop('products_data', [])
        order = Order.objects.create(**validated_data)

        for item in products_data:
            product_id = item['product_id']
            quantity = item['quantity']

            # Validazione esplicita
            if quantity <= 0:
                raise serializers.ValidationError(f"Quantity must be greater than 0 (got {quantity})")

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist")

            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('products_data', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if products_data:
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
