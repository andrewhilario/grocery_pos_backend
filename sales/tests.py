from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from products.models import Category, Product, Inventory
from sales.models import Customer

class SalesAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cashier', password='testpass', role='cashier', name='Cashier', email='cashier@example.com')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Snacks', description='Snacks')
        self.product = Product.objects.create(
            name='Lays', sku='SKU3', barcode='789012', description='Chips',
            category=self.category, price=15, cost=7, tax_rate=5, image_url=''
        )
        self.inventory = Inventory.objects.create(product=self.product, quantity=50, reorder_level=5)
        self.customer = Customer.objects.create(name='John Doe', email='john@example.com')

    def test_product_list(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        url = reverse('create-customer')
        data = {'name': 'Jane Doe', 'email': 'jane@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sale(self):
        url = reverse('create-sale')
        data = {
            "customer": {"name": "John Doe", "email": "john@example.com"},
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 2,
                    "unit_price": str(self.product.price),
                    "unit_cost": str(self.product.cost),
                    "tax_rate": str(self.product.tax_rate),      # Use string
                    "discount_percent": "0.00",                  # Use string
                    "total_price": str(self.product.price * 2)
                }
            ],
            "payment_method": "cash",
            "discount_amount": "0.00"  # Add this as string if your serializer/model expects it
        }
        response = self.client.post(url, data, format='json')
        print("SALE CREATE RESPONSE:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_receipt_detail(self):
        sale_url = reverse('create-sale')
        sale_data = {
            "customer": {"name": "John Doe", "email": "john@example.com"},
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity": 1,
                    "unit_price": str(self.product.price),
                    "unit_cost": str(self.product.cost),
                    "tax_rate": str(self.product.tax_rate),      # Use string
                    "discount_percent": "0.00",                  # Use string
                    "total_price": str(self.product.price * 1)
                }
            ],
            "payment_method": "cash",
            "discount_amount": "0.00"  # Add this as string if your serializer/model expects it
        }
        sale_response = self.client.post(sale_url, sale_data, format='json')
        sale_id = sale_response.data['id']
        receipt_url = reverse('sale-receipt', kwargs={'sale_id': sale_id})
        response = self.client.get(receipt_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)