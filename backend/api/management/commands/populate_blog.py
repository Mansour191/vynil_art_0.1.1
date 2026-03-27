from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import BlogPost, BlogCategory
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate the database with initial blog data'

    def handle(self, *args, **kwargs):
        # 1. Get or create a superuser as author
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            author = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin"'))

        # 2. Create Blog Categories
        categories = [
            {'ar': 'ديكور جدران', 'en': 'Wall Decor', 'slug': 'wall-decor'},
            {'ar': 'ملصقات سيارات', 'en': 'Car Stickers', 'slug': 'car-stickers'},
            {'ar': 'نصائح وأفكار', 'en': 'Tips & Ideas', 'slug': 'tips-and-ideas'},
            {'ar': 'تجديد المطبخ', 'en': 'Kitchen Renovation', 'slug': 'kitchen-renovation'},
        ]

        cat_objs = {}
        for cat in categories:
            obj, created = BlogCategory.objects.get_or_create(
                slug=cat['slug'],
                defaults={
                    'name_ar': cat['ar'],
                    'name_en': cat['en']
                }
            )
            cat_objs[cat['slug']] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat["en"]}'))

        # 3. Create Blog Posts
        posts = [
            {
                'title_ar': 'أفضل 5 تصاميم فينيل لجدران غرف النوم في 2026',
                'title_en': 'Top 5 Vinyl Designs for Bedroom Walls in 2026',
                'slug': 'top-5-vinyl-designs-2026',
                'category': cat_objs['wall-decor'],
                'content_ar': 'هذا هو المحتوى التجريبي للمقالة باللغة العربية...',
                'content_en': 'This is the demo content for the article in English...',
                'summary_ar': 'تعرف على أحدث صيحات الديكور باستخدام ورق الحائط والفينيل المخصص لغرف النوم العصرية...',
                'summary_en': 'Discover the latest decor trends using wallpaper and custom vinyl for modern bedrooms...',
                'tags': 'ديكور, غرف نوم, فينيل, 2026'
            },
            {
                'title_ar': 'كيفية العناية بملصقات السيارات لضمان بقائها سنوات طويلة',
                'title_en': 'How to Care for Car Stickers to Ensure Long Life',
                'slug': 'car-sticker-care-guide',
                'category': cat_objs['car-stickers'],
                'content_ar': 'نصائح احترافية لتنظيف وحماية ملصقات الفينيل على سيارتك...',
                'content_en': 'Professional tips for cleaning and protecting vinyl stickers on your car...',
                'summary_ar': 'نصائح احترافية لتنظيف وحماية ملصقات الفينيل على سيارتك من أشعة الشمس والحرارة العالية...',
                'summary_en': 'Professional tips for cleaning and protecting vinyl stickers on your car from sun and high heat...',
                'tags': 'سيارات, ملصقات, عناية, فينيل'
            },
            {
                'title_ar': 'تجديد المطبخ بأقل التكاليف: سحر الفينيل اللاصق',
                'title_en': 'Kitchen Renovation at Minimum Cost: The Magic of Adhesive Vinyl',
                'slug': 'kitchen-renovation-magic-vinyl',
                'category': cat_objs['kitchen-renovation'],
                'content_ar': 'لا حاجة لتغيير خزائن المطبخ بالكامل، اكتشف كيف يمكن للفينيل أن يحول مطبخك القديم...',
                'content_en': 'No need to change entire kitchen cabinets, discover how vinyl can transform your old kitchen...',
                'summary_ar': 'لا حاجة لتغيير خزائن المطبخ بالكامل، اكتشف كيف يمكن للفينيل أن يحول مطبخك القديم لآخر عصري...',
                'summary_en': 'No need to change entire kitchen cabinets, discover how vinyl can transform your old kitchen to a modern one...',
                'tags': 'مطبخ, تجديد, ديكور, اقتصادي'
            }
        ]

        for post_data in posts:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    'title_ar': post_data['title_ar'],
                    'title_en': post_data['title_en'],
                    'category': post_data['category'],
                    'content_ar': post_data['content_ar'],
                    'content_en': post_data['content_en'],
                    'summary_ar': post_data['summary_ar'],
                    'summary_en': post_data['summary_en'],
                    'author': author,
                    'tags': post_data['tags']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created post: {post_data["title_en"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Post already exists: {post_data["title_en"]}'))
