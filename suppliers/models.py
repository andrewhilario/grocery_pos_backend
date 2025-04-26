from django.db import models
from products.models import Product


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductSupplier(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="suppliers"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="products"
    )
    supplier_sku = models.CharField(max_length=50, blank=True, null=True)
    lead_time_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "supplier")
        verbose_name = "Product Supplier"
        verbose_name_plural = "Product Suppliers"

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"
