#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paclos_backend.settings')
django.setup()

from api.models import Product, Category, Material

# Get or create a category
category, created = Category.objects.get_or_create(
    slug='test-category',
    defaults={
        'name_ar': 'فئة اختبار',
        'name_en': 'Test Category',
        'icon': 'fas fa-test',
        'waste_percent': 10.00
    }
)

# Get or create a material
material, created = Material.objects.get_or_create(
    name_en='Test Material',
    defaults={
        'name_ar': 'مادة اختبار',
        'description': 'Material for testing',
        'price_per_m2': 100.00,
        'is_premium': False
    }
)

# Create test product
product, created = Product.objects.get_or_create(
    slug='test',
    defaults={
        'name_ar': 'منتج اختبار',
        'name_en': 'Test Product',
        'category': category,
        'description_ar': 'وصف اختبار',
        'description_en': 'Test description',
        'base_price': 1500.00,
        'cost': 1000.00,
        'stock': 50,
        'on_sale': False,
        'discount_percent': 0,
        'is_new': True,
        'sync_status': 'synced'
    }
)

if created:
    print(f"Created test product: {product.name_en} (ID: {product.id})")
else:
    print(f"Test product already exists: {product.name_en} (ID: {product.id})")
