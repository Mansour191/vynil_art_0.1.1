import random
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.base import ContentFile
from api.models import (
    UserProfile, Category, Material, Product, ProductImage, ProductVariant,
    Shipping, Coupon, Order, OrderItem, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine
)
from faker import Faker
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with comprehensive realistic fake data and images'

    def handle(self, *args, **options):
        fake = Faker(['en_US', 'ar_SA'])
        self.stdout.write("Starting comprehensive population...")

        # Utility to get a placeholder image
        def get_fake_image(name="product"):
            try:
                response = requests.get(f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600", timeout=5)
                if response.status_code == 200:
                    return ContentFile(response.content, name=f"{name}_{random.randint(1, 1000)}.jpg")
            except:
                pass
            return None

        # 1. Create Users & Profiles
        users = []
        for i in range(15):
            username = f"tester_{i}"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': fake.email(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name()
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f"05{random.randint(10000000, 99999999)}",
                    'address': fake.address()
                }
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Verified {len(users)} users"))

        # 2. Categories & Materials (Existing)
        categories = list(Category.objects.all())
        materials = list(Material.objects.all())

        # 3. Products & Images & Variants
        vinyl_names = [
            ("Golden Geometric", "هندسي ذهبي", "GEO-001"),
            ("Silver Marble", "رخام فضي", "MAR-002"),
            ("Emerald Wave", "موج زمردي", "CAR-003"),
            ("Dark Walnut", "خشب جوز داكن", "KIT-004"),
            ("Urban Concrete", "خرسانة مدنية", "CON-005"),
            ("Vintage Floral", "زهور عتيقة", "FLO-006"),
            ("Azure Sky", "سماء زرقاء", "SKY-007"),
            ("Ruby Texture", "نسيج ياقوتي", "RUB-008"),
            ("Onyx Black", "عقيق أسود", "ONY-009"),
            ("Ivory Silk", "حرير عاجي", "SIL-010"),
            ("Test Product", "منتج تجريبي", "test")
        ]

        products = []
        for name_en, name_ar, slug in vinyl_names:
            category = random.choice(categories)
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name_en': name_en,
                    'name_ar': name_ar,
                    'category': category,
                    'description_en': fake.paragraph(),
                    'description_ar': "هذا المنتج مصمم بعناية ليناسب أرقى الأذواق الجزائرية، يتميز بجودة عالية وسهولة في التركيب.",
                    'base_price': Decimal(random.randint(2000, 6000)),
                    'cost': Decimal(random.randint(1500, 4000)),
                    'stock': random.randint(0, 200),
                    'on_sale': random.choice([True, False]),
                    'discount_percent': random.randint(10, 30) if random.random() > 0.6 else 0,
                    'is_new': random.choice([True, False])
                }
            )
            
            # Add Main Image if not exists
            if not product.image:
                img = get_fake_image(f"prod_{product.slug}")
                if img:
                    product.image.save(img.name, img)
            
            # Add Gallery Images
            if product.images.count() < 2:
                for j in range(2):
                    img = get_fake_image(f"gallery_{product.slug}")
                    if img:
                        ProductImage.objects.create(product=product, image=img, alt_text=f"Gallery {j}")

            # Add Variants
            ProductVariant.objects.get_or_create(
                product=product,
                name_en="Matte Finish",
                defaults={'name_ar': "مظهر مطفأ", 'price_adjustment': 0}
            )
            ProductVariant.objects.get_or_create(
                product=product,
                name_en="Glossy 4K",
                defaults={'name_ar': "لامع عالي الدقة", 'price_adjustment': 800}
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f"Populated {len(products)} products with images and variants"))

        # 4. Orders & Payments & Timelines
        wilayas = list(Shipping.objects.all())
        for _ in range(20):
            user = random.choice(users)
            wilaya = random.choice(wilayas)
            subtotal = Decimal(random.randint(8000, 45000))
            ship_cost = wilaya.home_delivery_price
            total = subtotal + ship_cost
            
            order = Order.objects.create(
                user=user,
                order_number=f"PAC-{fake.uuid4()[:8].upper()}",
                customer_name=f"{user.first_name} {user.last_name}",
                phone=user.profile.phone,
                email=user.email,
                address=user.profile.address,
                wilaya=wilaya,
                subtotal=subtotal,
                shipping_cost=ship_cost,
                total=total,
                status=random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
                payment_method=random.choice(['cod', 'card']),
                payment_status=random.choice([True, False])
            )
            
            # Payment record
            if order.payment_method == 'card' or order.payment_status:
                Payment.objects.create(
                    order=order,
                    transaction_id=f"TXN-{fake.uuid4()[:12].upper()}",
                    amount=order.total,
                    method="Edahabia" if random.random() > 0.5 else "CIB",
                    status="completed" if order.payment_status else "pending"
                )

            # Order Items
            for _ in range(random.randint(1, 4)):
                p = random.choice(products)
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    material=random.choice(materials),
                    width=Decimal(random.randint(100, 500)),
                    height=Decimal(random.randint(100, 500)),
                    quantity=random.randint(1, 3),
                    price=p.base_price
                )
            
            # Timeline
            OrderTimeline.objects.create(order=order, status='pending', note="تم استلام الطلب")
            if order.status != 'pending':
                OrderTimeline.objects.create(order=order, status=order.status, note=f"تم تحديث الحالة إلى {order.status}")

        # 5. Cart & Wishlist
        for user in users:
            # Cart items
            for _ in range(random.randint(1, 3)):
                p = random.choice(products)
                CartItem.objects.create(
                    user=user,
                    product=p,
                    quantity=random.randint(1, 2),
                    options={'width': 150, 'height': 200, 'variant': 'Matte'}
                )
            # Wishlist
            for p in random.sample(products, random.randint(1, 4)):
                Wishlist.objects.get_or_create(user=user, product=p)

        # 6. Reviews & Reports
        for p in products:
            for _ in range(random.randint(1, 3)):
                rev = Review.objects.create(
                    product=p,
                    user=random.choice(users),
                    rating=random.randint(4, 5),
                    comment=fake.sentence()
                )
                if random.random() > 0.9:
                    ReviewReport.objects.create(review=rev, user=random.choice(users), reason="Spam")

        # 7. Notifications & Alerts
        for user in users:
            for _ in range(3):
                Notification.objects.create(
                    user=user,
                    title="تحديث طلبك",
                    message=f"الطلب PAC-XXXX أصبح الآن {random.choice(['قيد التجهيز', 'تم الشحن'])}",
                    is_read=random.choice([True, False])
                )
        
        Alert.objects.create(type='warning', message="تنبيه: سيتم إغلاق المتجر مؤقتاً للصيانة غداً.")
        Alert.objects.create(type='success', message="وصل حديثاً: تشكيلة الرخام الملكي متوفرة الآن!")

        # 8. Designs
        d_cat = DesignCategory.objects.first()
        for i in range(8):
            d = Design.objects.create(
                category=d_cat,
                title_en=f"Modern Concept {i}",
                title_ar=f"مفهوم عصري {i}",
                creator=random.choice(users)
            )
            img = get_fake_image("design")
            if img:
                d.image.save(img.name, img)

        # 9. ERPNext Logs
        for _ in range(10):
            ERPNextSyncLog.objects.create(
                action=random.choice(["Sync Products", "Push Order", "Update Stock"]),
                status=random.choice(["Success", "Fail"]),
                message=fake.sentence()
            )

        # 10. AI & Analytics
        for _ in range(100):
            BehaviorTracking.objects.create(
                user=random.choice(users + [None]),
                event_type=random.choice(['view_product', 'add_to_cart', 'checkout_start', 'search']),
                metadata={'product_id': random.choice(products).id, 'platform': 'web'}
            )
        
        for i in range(5):
            Forecast.objects.create(
                target_metric="Monthly Sales",
                predicted_value=Decimal(random.randint(500000, 2000000)),
                confidence_score=0.85,
                forecast_date=timezone.now().date() + timezone.timedelta(days=30 * i)
            )

        # Segments
        s1, _ = CustomerSegment.objects.get_or_create(name="VIP High Value", description="Customers with total orders > 100k")
        s2, _ = CustomerSegment.objects.get_or_create(name="New Explorers", description="Users who visited but haven't ordered")
        s1.users.add(*random.sample(users, 3))
        s2.users.add(*random.sample(users, 5))

        self.stdout.write(self.style.SUCCESS("Comprehensive population complete! 23 tables are now full."))
