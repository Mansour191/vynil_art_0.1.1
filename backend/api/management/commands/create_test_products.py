from django.core.management.base import BaseCommand
from api.models import Product, Category, Material
import random

class Command(BaseCommand):
    help = 'Create missing products expected by the frontend'

    def handle(self, *args, **kwargs):
        # Ensure category exists
        cat, _ = Category.objects.get_or_create(
            name='Test Category',
            slug='test-category',
            defaults={'description': 'For testing purposes'}
        )
        
        # Ensure material exists
        mat, _ = Material.objects.get_or_create(
            name='Standard Vinyl',
            slug='standard-vinyl',
            defaults={'price_per_m2': 1500}
        )

        missing_slugs = ['test', 'WAL-001', 'CAR-003']
        
        for slug in missing_slugs:
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': f'Product {slug}',
                    'sku': slug,
                    'description': f'A test product with slug {slug}',
                    'category': cat,
                    'base_price': 2500,
                    'stock': 100,
                    'active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {slug}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {slug}'))
