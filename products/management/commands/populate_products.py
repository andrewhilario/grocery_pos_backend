from django.core.management.base import BaseCommand
from products.models import Category, Product, Inventory

class Command(BaseCommand):
    help = 'Populate the database with sample categories, products, and inventory for POS'

    def handle(self, *args, **kwargs):
        # Define POS-relevant categories
        categories_data = [
            {'name': 'Beverages', 'description': 'Drinks and refreshments'},
            {'name': 'Snacks', 'description': 'Chips, biscuits, and munchies'},
            {'name': 'Dairy', 'description': 'Milk, cheese, and yogurt'},
            {'name': 'Bakery', 'description': 'Bread, cakes, and pastries'},
            {'name': 'Produce', 'description': 'Fruits and vegetables'},
            {'name': 'Meat', 'description': 'Fresh and processed meats'},
            {'name': 'Seafood', 'description': 'Fish and seafood'},
            {'name': 'Frozen Foods', 'description': 'Frozen meals and desserts'},
            {'name': 'Pantry', 'description': 'Canned and dry goods'},
            {'name': 'Personal Care', 'description': 'Toiletries and hygiene'},
            {'name': 'Household', 'description': 'Cleaning and home supplies'},
            {'name': 'Confectionery', 'description': 'Sweets and chocolates'},
            {'name': 'Beverages - Alcoholic', 'description': 'Beer, wine, and spirits'},
            {'name': 'Baby Products', 'description': 'Baby food and care'},
            {'name': 'Pet Supplies', 'description': 'Food and accessories for pets'},
        ]
        category_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(name=cat['name'], defaults={'description': cat['description']})
            category_objs[cat['name']] = obj

        # 20 sample products
        products_data = [
            {'name': 'Coca-Cola 500ml', 'sku': 'SKU001', 'barcode': '1000001', 'description': 'Soft drink', 'category': 'Beverages', 'price': 1.5, 'cost': 1.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Pepsi 500ml', 'sku': 'SKU002', 'barcode': '1000002', 'description': 'Soft drink', 'category': 'Beverages', 'price': 1.5, 'cost': 1.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Lays Classic', 'sku': 'SKU003', 'barcode': '1000003', 'description': 'Potato chips', 'category': 'Snacks', 'price': 2.0, 'cost': 1.2, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Oreo Biscuits', 'sku': 'SKU004', 'barcode': '1000004', 'description': 'Chocolate biscuits', 'category': 'Snacks', 'price': 1.8, 'cost': 1.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Whole Milk 1L', 'sku': 'SKU005', 'barcode': '1000005', 'description': 'Fresh milk', 'category': 'Dairy', 'price': 2.5, 'cost': 1.8, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Cheddar Cheese', 'sku': 'SKU006', 'barcode': '1000006', 'description': 'Block cheese', 'category': 'Dairy', 'price': 3.0, 'cost': 2.2, 'tax_rate': 5, 'image_url': ''},
            {'name': 'White Bread', 'sku': 'SKU007', 'barcode': '1000007', 'description': 'Bakery bread', 'category': 'Bakery', 'price': 1.2, 'cost': 0.8, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Chocolate Cake', 'sku': 'SKU008', 'barcode': '1000008', 'description': 'Bakery cake', 'category': 'Bakery', 'price': 5.0, 'cost': 3.5, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Banana', 'sku': 'SKU009', 'barcode': '1000009', 'description': 'Fresh bananas', 'category': 'Produce', 'price': 1.0, 'cost': 0.6, 'tax_rate': 0, 'image_url': ''},
            {'name': 'Tomato', 'sku': 'SKU010', 'barcode': '1000010', 'description': 'Fresh tomatoes', 'category': 'Produce', 'price': 1.2, 'cost': 0.7, 'tax_rate': 0, 'image_url': ''},
            {'name': 'Chicken Breast', 'sku': 'SKU011', 'barcode': '1000011', 'description': 'Fresh chicken', 'category': 'Meat', 'price': 4.0, 'cost': 3.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Salmon Fillet', 'sku': 'SKU012', 'barcode': '1000012', 'description': 'Fresh salmon', 'category': 'Seafood', 'price': 7.0, 'cost': 5.5, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Frozen Pizza', 'sku': 'SKU013', 'barcode': '1000013', 'description': 'Ready to eat', 'category': 'Frozen Foods', 'price': 4.5, 'cost': 3.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Canned Beans', 'sku': 'SKU014', 'barcode': '1000014', 'description': 'Pantry staple', 'category': 'Pantry', 'price': 1.5, 'cost': 1.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Toothpaste', 'sku': 'SKU015', 'barcode': '1000015', 'description': 'Personal care', 'category': 'Personal Care', 'price': 2.0, 'cost': 1.2, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Laundry Detergent', 'sku': 'SKU016', 'barcode': '1000016', 'description': 'Household cleaning', 'category': 'Household', 'price': 6.0, 'cost': 4.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Milk Chocolate Bar', 'sku': 'SKU017', 'barcode': '1000017', 'description': 'Confectionery', 'category': 'Confectionery', 'price': 1.5, 'cost': 1.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Red Wine', 'sku': 'SKU018', 'barcode': '1000018', 'description': 'Alcoholic beverage', 'category': 'Beverages - Alcoholic', 'price': 10.0, 'cost': 7.0, 'tax_rate': 10, 'image_url': ''},
            {'name': 'Baby Diapers', 'sku': 'SKU019', 'barcode': '1000019', 'description': 'Baby care', 'category': 'Baby Products', 'price': 8.0, 'cost': 6.0, 'tax_rate': 5, 'image_url': ''},
            {'name': 'Dog Food', 'sku': 'SKU020', 'barcode': '1000020', 'description': 'Pet food', 'category': 'Pet Supplies', 'price': 5.0, 'cost': 3.5, 'tax_rate': 5, 'image_url': ''},
        ]

        for pdata in products_data:
            product, created = Product.objects.get_or_create(
                sku=pdata['sku'],
                defaults={
                    'name': pdata['name'],
                    'barcode': pdata['barcode'],
                    'description': pdata['description'],
                    'category': category_objs[pdata['category']],
                    'price': pdata['price'],
                    'cost': pdata['cost'],
                    'tax_rate': pdata['tax_rate'],
                    'image_url': pdata['image_url'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))

            # Create inventory for each product
            inventory, inv_created = Inventory.objects.get_or_create(
                product=product,
                defaults={'quantity': 100, 'reorder_level': 10}
            )
            if inv_created:
                self.stdout.write(self.style.SUCCESS(f'Created inventory for: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Inventory already exists for: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Database populated with sample categories, products, and inventory.'))