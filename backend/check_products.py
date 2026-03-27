#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paclos_backend.settings')
django.setup()

from api.models import Product

# Check products
products = Product.objects.all()[:5]
print("Available products:")
for p in products:
    print(f"ID: {p.id}, Slug: {p.slug}, Name: {p.name_en}")

# Check if 'test' exists
try:
    test_product = Product.objects.get(slug='test')
    print(f"Found product with slug 'test': {test_product.name_en}")
except Product.DoesNotExist:
    print("Product with slug 'test' does not exist")
    
# Check if 'test' exists as ID
try:
    test_product = Product.objects.get(id='test')
    print(f"Found product with ID 'test': {test_product.name_en}")
except (Product.DoesNotExist, ValueError):
    print("Product with ID 'test' does not exist")

# Get first product ID for testing
first_product = Product.objects.first()
if first_product:
    print(f"First product for testing: ID={first_product.id}, Slug={first_product.slug}")
