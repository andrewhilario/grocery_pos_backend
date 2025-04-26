from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sale(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("credit", "Credit Card"),
        ("debit", "Debit Card"),
    ]

    PAYMENT_STATUSES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sales"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUSES, default="paid"
    )
    sale_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.total_amount}"
    
    def calculate_totals(self):
        items = self.items.all()
        self.subtotal = sum(item.total_price for item in items)
        self.tax_amount = sum(item.total_price * (item.tax_rate / Decimal("100")) for item in items)
        self.total_amount = self.subtotal + self.tax_amount - Decimal(self.discount_amount)
        self.save()

    def generate_receipt(self):
        """Generate receipt for the sale"""
        receipt, created = Receipt.objects.get_or_create(
            sale=self,
            defaults={
                'receipt_number': f"RCPT-{self.invoice_number}",
                'receipt_content': self.get_receipt_content()
            }
        )
        return receipt

    def get_receipt_content(self):
        """Generate detailed receipt content"""
        items = []
        for item in self.items.all():
            items.append(f"{item.quantity}x {item.product.name} @ {item.unit_price} = {item.total_price}")
        
        receipt_lines = [
            f"Receipt for Invoice #{self.invoice_number}",
            f"Date: {self.sale_date.strftime('%Y-%m-%d %H:%M:%S')}",
            "----------------------------------------",
            *items,
            "----------------------------------------",
            f"Subtotal: {self.subtotal}",
            f"Tax: {self.tax_amount}",
            f"Discount: {self.discount_amount}",
            f"Total: {self.total_amount}",
            f"Payment Method: {self.get_payment_method_display()}",
            "Thank you for your business!"
        ]
        return "\n".join(receipt_lines)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="sale_items"
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.unit_price}"


class Receipt(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="receipt")
    receipt_number = models.CharField(max_length=50, unique=True)
    receipt_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number} for Sale #{self.sale.invoice_number}"
