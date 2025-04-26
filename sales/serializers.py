# serializers.py
from rest_framework import serializers
from .models import Customer, Sale, SaleItem, Receipt
from products.models import Inventory, Product
from django.conf import settings

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'barcode', 'stock_quantity']
    
    def get_stock_quantity(self, obj):
        # Get the quantity from the related Inventory model
        try:
            return obj.inventory.quantity
        except Inventory.DoesNotExist:
            return 0

class SaleItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    
    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 
                 'total_price', 'tax_rate', 'discount_percent']
    
    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        
        try:
            inventory = product.inventory
            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Only {inventory.quantity} available."
                )
        except Inventory.DoesNotExist:
            raise serializers.ValidationError(
                f"No inventory record found for {product.name}"
            )
        
        return data

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    customer = CustomerSerializer(required=False, allow_null=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'invoice_number', 'user', 'customer', 'items', 
                 'subtotal', 'tax_amount', 'discount_amount', 'total_amount',
                 'payment_method', 'payment_status', 'sale_date']
        read_only_fields = ['invoice_number', 'user', 'subtotal', 'tax_amount', 
                          'discount_amount', 'total_amount', 'sale_date']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer_data = validated_data.pop('customer', None)
        
        # Create or update customer if data provided
        customer = None
        if customer_data:
            customer, _ = Customer.objects.get_or_create(
                email=customer_data.get('email'),
                defaults=customer_data
            )
        
        # Create sale
        sale = Sale.objects.create(
            customer=customer,
            user=self.context['request'].user,
            **validated_data
        )
        
        # Create sale items
        for item_data in items_data:
            product = item_data['product']
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.price,
                unit_cost=product.cost,  # <-- Fix here
                tax_rate=item_data.get('tax_rate', 0.0),
                discount_percent=item_data.get('discount_percent', 0.0),
                total_price=product.price * item_data['quantity']
            )
        
        # Calculate totals
        sale.calculate_totals()
        return sale

class ReceiptSerializer(serializers.ModelSerializer):
    sale = SaleSerializer(read_only=True)
    
    class Meta:
        model = Receipt
        fields = ['id', 'sale', 'receipt_number', 'receipt_content', 'created_at']
        read_only_fields = ['receipt_number', 'receipt_content']