from django.db import models
from django.conf import settings
from suppliers.models import Supplier
from products.models import Product


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name="purchase_orders"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    order_date = models.DateField()
    expected_delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return f"PO #{self.po_number} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    po = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="po_items"
    )
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity_ordered} x {self.product.name} @ {self.unit_cost}"


class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("sale", "Sale"),
        ("purchase", "Purchase"),
        ("adjustment", "Adjustment"),
        ("return", "Return"),
        ("waste", "Waste"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="transactions"
    )
    quantity_change = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reference_id = models.IntegerField(
        blank=True, null=True
    )  # Could be sale_id, po_id, etc.
    notes = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    transaction_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.quantity_change} units of {self.product.name}"
