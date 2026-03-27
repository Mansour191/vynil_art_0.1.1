#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paclos_backend.settings')
django.setup()

from api.models import Product, Category, Material

# Get or create categories
categories = {
    'furniture': Category.objects.get_or_create(
        slug='furniture',
        defaults={'name_ar': 'أثاث', 'name_en': 'Furniture', 'icon': 'fas fa-couch', 'waste_percent': 10}
    )[0],
    'doors': Category.objects.get_or_create(
        slug='doors',
        defaults={'name_ar': 'أبواب', 'name_en': 'Doors', 'icon': 'fas fa-door-open', 'waste_percent': 8}
    )[0],
    'kitchen': Category.objects.get_or_create(
        slug='kitchen',
        defaults={'name_ar': 'مطابخ', 'name_en': 'Kitchen', 'icon': 'fas fa-utensils', 'waste_percent': 12}
    )[0],
}

# Test products to create
test_products = [
    {
        'slug': 'KIT-004',
        'name_ar': 'خزانة مطبخ حديثة',
        'name_en': 'Modern Kitchen Cabinet',
        'category': categories['kitchen'],
        'base_price': 2500.00,
        'cost': 1800.00,
        'stock': 15,
        'description_ar': 'خزانة مطبخ عصرية بتصميم ذهبي',
        'description_en': 'Modern kitchen cabinet with golden design'
    },
    {
        'slug': 'DR-002',
        'name_ar': 'باب داخلي أنيق',
        'name_en': 'Elegant Interior Door',
        'category': categories['doors'],
        'base_price': 1800.00,
        'cost': 1200.00,
        'stock': 8,
        'description_ar': 'باب داخلي بتصميم كلاسيكي',
        'description_en': 'Interior door with classic design'
    },
    {
        'slug': 'WAL-001',
        'name_ar': 'جدارية فنية',
        'name_en': 'Artistic Wall Mural',
        'category': categories['furniture'],
        'base_price': 1200.00,
        'cost': 800.00,
        'stock': 25,
        'description_ar': 'جدارية فنية للجدران',
        'description_en': 'Artistic wall mural for walls'
    },
    {
        'slug': 'CAR-003',
        'name_ar': 'ملصق سيارة رياضية',
        'name_en': 'Sports Car Decal',
        'category': categories['furniture'],
        'base_price': 800.00,
        'cost': 500.00,
        'stock': 30,
        'description_ar': 'ملصق سيارة بتصميم رياضي',
        'description_en': 'Sports car decal with sporty design'
    }
]

# Create products
for product_data in test_products:
    product, created = Product.objects.get_or_create(
        slug=product_data['slug'],
        defaults={
            **product_data,
            'on_sale': False,
            'discount_percent': 0,
            'is_new': True,
            'sync_status': 'synced'
        }
    )
    
    if created:
        print(f"Created product: {product.name_en} (Slug: {product.slug})")
    else:
        print(f"Product already exists: {product.name_en} (Slug: {product.slug})")

print("\nAll test products created successfully!")
