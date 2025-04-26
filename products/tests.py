from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from products.models import Category, Product, Inventory

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='admin', name='Test User', email='test@example.com')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Beverages', description='Drinks')
        self.product = Product.objects.create(
            name='Coke', sku='SKU1', barcode='123456', description='Soda',
            category=self.category, price=10, cost=5, tax_rate=5, image_url=''
        )
        self.inventory = Inventory.objects.create(product=self.product, quantity=100, reorder_level=10)

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        url = reverse('category-list')
        data = {'name': 'Snacks', 'description': 'Chips and more'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Pepsi', 'sku': 'SKU2', 'barcode': '654321', 'description': 'Soda',
            'category': self.category.id, 'price': 12, 'cost': 6, 'tax_rate': 5, 'image_url': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_inventory(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)