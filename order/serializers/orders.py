from django.db.models import fields
from rest_framework import serializers
from order.serializers.products import ProductSerializer
from order.models.orders import OrderItems, Order
from user_auth.models.cpf import Cpf

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)   

    class Meta:
        model = OrderItems
        fields = ('id', 'order', 'product', 'quantity', 'changes')  

class OrderItemsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'      

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_internal_value(self, data):
        if 'cpf' in data:
            cpf_value = data['cpf']
            cpf_instance, created = Cpf.get_or_create_cpf(cpf_value)
            data['cpf'] = cpf_instance

        return super().to_internal_value(data)
  

class OrderInlineItemsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()  # Use SerializerMethodField for custom serialization
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'session_token',
            'cpf',
            'status',
            'created_at',
            'updated_at',
            'item'
        ]

    def get_item(self, obj):
        # Define custom method to serialize related CartItem objects
        order_items = OrderItems.objects.filter(order=obj)  # Fetch related CartItem objects
        serializer = OrderItemsSerializer(order_items, many=True)  # Serialize related CartItem objects
        return serializer.data  # Return serialized data