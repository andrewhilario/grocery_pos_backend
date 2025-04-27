from rest_framework import serializers

from suppliers.serializers import SupplierSerializer
from .models import Category, Product, Inventory
from django.db.models import Sum

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']  

class CategoryByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']  

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'barcode', 'description', 'category', 'price', 'cost', 'tax_rate', 'image_url']

class ProductByIdSerializer(serializers.ModelSerializer):
    stocks_available = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'barcode', 'description', 'category', 'price', 'cost', 'tax_rate', 'image_url', 'stocks_available']

    def get_stocks_available(self, obj):
        """Retrieve the total stock available for the product."""
        return Inventory.objects.filter(product=obj).aggregate(total_stock=Sum('quantity'))['total_stock'] or 0
    
    def get_category(self, obj):
        """Retrieve the category of the product."""
        if obj.category:
            return CategoryByIdSerializer(obj.category).data
        return None

class ProductSerializer(serializers.ModelSerializer):
    stocks_available = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'barcode', 'description', 'category', 'price', 'cost', 'tax_rate', 'image_url', 'stocks_available']

    def get_stocks_available(self, obj):
        """Retrieve the total stock available for the product."""
        return Inventory.objects.filter(product=obj).aggregate(total_stock=Sum('quantity'))['total_stock'] or 0
    
    def get_category(self, obj):
        """Retrieve the category of the product."""
        if obj.category:
            return CategoryByIdSerializer(obj.category).data
        return None

class InventorySerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    product = ProductSerializer(read_only=True)
    needs_restock = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id',
            'product',
            'quantity',
            'reorder_level',
            'last_restock_date',
            'created_at',
            'updated_at',
            'needs_restock',
            'supplier',   
            'category',   
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_needs_restock(self, obj):
        """Calculate if the inventory needs restocking."""
        return obj.quantity <= obj.reorder_level
    
    def get_supplier(self, obj):
        product_suppliers = obj.product.suppliers.select_related('supplier').all()
        return SupplierSerializer([ps.supplier for ps in product_suppliers], many=True).data

    def get_category(self, obj):
        if obj.product.category:
            return CategoryByIdSerializer(obj.product.category).data
        return None
    
    def validate_quantity(self, value):
        """Ensure quantity is not negative."""
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
    
    def validate_reorder_level(self, value):
        """Ensure reorder level is not negative."""
        if value < 0:
            raise serializers.ValidationError("Reorder level cannot be negative.")
        return value
