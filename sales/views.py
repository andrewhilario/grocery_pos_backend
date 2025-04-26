# views.py
from django.forms import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Sale, SaleItem, Receipt, Customer
from .serializers import (
    ProductSerializer, 
    SaleSerializer, 
    ReceiptSerializer,
    CustomerSerializer
)
from products.models import Inventory, Product
from django.shortcuts import get_object_or_404
from django.db import transaction
import random
import string
from datetime import datetime

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        barcode = self.request.query_params.get('barcode', None)
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if barcode:
            queryset = queryset.filter(barcode=barcode)
        
        return queryset

class CreateSaleView(generics.CreateAPIView):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    
    def generate_invoice_number(self):
        date_str = datetime.now().strftime("%Y%m%d")
        rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"INV-{date_str}-{rand_str}"
    
    @transaction.atomic
    def perform_create(self, serializer):
        # Generate invoice number
        invoice_number = self.generate_invoice_number()
        
        # Save the sale with the generated invoice number
        sale = serializer.save(
            invoice_number=invoice_number,
            payment_status='paid'
        )
        
        # Update inventory quantities
        for item in sale.items.all():
            product = item.product
            try:
                inventory = product.inventory
                inventory.quantity -= item.quantity
                if inventory.quantity < 0:
                    raise ValidationError(f"Insufficient stock for {product.name}")
                inventory.save()
            except Inventory.DoesNotExist:
                raise ValidationError(f"No inventory record found for {product.name}")
        
        # Create receipt
        receipt_content = self.generate_receipt_content(sale)
        Receipt.objects.create(
            sale=sale,
            receipt_number=f"RCPT-{invoice_number}",
            receipt_content=receipt_content
        )
    
    def generate_receipt_content(self, sale):
        items = []
        for item in sale.items.all():
            items.append({
                'name': item.product.name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'total': float(item.total_price)
            })
        
        receipt_data = {
            'invoice_number': sale.invoice_number,
            'date': sale.sale_date.strftime("%Y-%m-%d %H:%M:%S"),
            'cashier': sale.user.get_full_name() or sale.user.username,
            'customer': sale.customer.name if sale.customer else "Walk-in Customer",
            'items': items,
            'subtotal': float(sale.subtotal),
            'tax_amount': float(sale.tax_amount),
            'total_amount': float(sale.total_amount),
            'payment_method': sale.get_payment_method_display(),
        }
        
        return str(receipt_data)
class ReceiptDetailView(generics.RetrieveAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'sale_id'
    lookup_url_kwarg = 'sale_id'
    
    def get_object(self):
        sale_id = self.kwargs.get('sale_id')
        return get_object_or_404(Receipt, sale__id=sale_id)

class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]