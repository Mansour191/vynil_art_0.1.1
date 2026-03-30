from django.db import models
from django.contrib.auth.models import User

# 1. Users & Auth
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# 2. Products
class Category(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    waste_percent = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name_en

class Material(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name_en

class Product(models.Model):
    SYNC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]

    name_ar = models.CharField(max_length=255, verbose_name="Name (Arabic)")
    name_en = models.CharField(max_length=255, verbose_name="Name (English)")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description_ar = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base rate per m2")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Production cost per m2")
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    on_sale = models.BooleanField(default=False)
    discount_percent = models.PositiveIntegerField(default=0)
    is_new = models.BooleanField(default=True)
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default='pending')
    erpnext_item_code = models.CharField(max_length=120, blank=True, default='')
    sync_error = models.TextField(blank=True, default='')
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_en

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name_en = models.CharField(max_length=100) # e.g. "Matte Finish", "High-Res"
    name_ar = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.product.name_en} - {self.name_en}"

# 3. Orders
class Shipping(models.Model):
    wilaya_id = models.CharField(max_length=2, unique=True)
    name_ar = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100)
    stop_desk_price = models.DecimalField(max_digits=10, decimal_places=2, default=400)
    home_delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=700)

    def __str__(self):
        return f"{self.wilaya_id} - {self.name_fr}"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

# 4. Blog
class BlogCategory(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name_en

class BlogPost(models.Model):
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    content_ar = models.TextField()
    content_en = models.TextField()
    summary_ar = models.TextField(blank=True)
    summary_en = models.TextField(blank=True)
    image = models.ImageField(upload_to='blog/')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")

    def __str__(self):
        return self.title_en

# 5. Orders Continued (Original)
class Order(models.Model):
    SYNC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('synced', 'Synced'),
        ('failed', 'Failed'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Online Payment'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    wilaya = models.ForeignKey(Shipping, on_delete=models.PROTECT)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.BooleanField(default=False)
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS_CHOICES, default='pending')
    erpnext_sales_order_id = models.CharField(max_length=120, blank=True, default='')
    sync_error = models.TextField(blank=True, default='')
    last_synced_at = models.DateTimeField(null=True, blank=True)
    
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    dimension_unit = models.CharField(max_length=10, default='cm')
    marble_texture = models.CharField(max_length=120, blank=True, default='')
    custom_design = models.CharField(max_length=255, blank=True, default='')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name_en} x {self.quantity}"

class OrderTimeline(models.Model):
    order = models.ForeignKey(Order, related_name='timeline', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50) # e.g. "Edahabia", "CIB"
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

# 4. Cart & Wishlist
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    options = models.JSONField(default=dict, blank=True) # width, height, etc.
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

# 5. Reviews
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name_en} ({self.rating})"

class ReviewReport(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 6. Designs
class DesignCategory(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name_en

class Design(models.Model):
    category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE, related_name='designs')
    title_ar = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to='designs/')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 7. Notifications & Alerts
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    TYPE_CHOICES = [('info', 'Info'), ('warning', 'Warning'), ('error', 'Error'), ('success', 'Success')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 8. ERPNext Integration
class ERPNextSyncLog(models.Model):
    action = models.CharField(max_length=100) # e.g. "Sync Products", "Push Order"
    status = models.CharField(max_length=20) # Success/Fail
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# 9. Analytics & AI
class BehaviorTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=100, default='page_view')
    page = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class ConversationHistory(models.Model):
    session_id = models.CharField(max_length=255, db_index=True)
    role = models.CharField(max_length=20)  # 'user' or 'assistant'
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    source = models.CharField(max_length=50, default='unknown')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.session_id} - {self.role} - {self.created_at}"

class Forecast(models.Model):
    target_metric = models.CharField(max_length=50) # sales, inventory
    predicted_value = models.DecimalField(max_digits=15, decimal_places=2)
    confidence_score = models.FloatField()
    forecast_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerSegment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='segments')

# Global Pricing (Already existing requirements)
class PricingEngine(models.Model):
    raw_material_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    international_shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Pricing Engine"

# 6. Media Files Management
class MediaFile(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media_files/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='image')
    description = models.TextField(blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media_files', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Media Files"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

# 7. Addresses Management
class Address(models.Model):
    ADDRESS_TYPES = [
        ('shipping', 'Shipping Address'),
        ('billing', 'Billing Address'),
        ('both', 'Both'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='shipping')
    title = models.CharField(max_length=100, help_text="e.g., Home, Office")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.street_address}"

# 8. Inventory/Stock Management
class Inventory(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10, help_text="Alert when stock reaches this level")
    max_stock = models.PositiveIntegerField(default=1000, help_text="Maximum stock capacity")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_stock')
    last_restocked = models.DateTimeField(null=True, blank=True)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.CharField(max_length=100, blank=True, help_text="Warehouse location")
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Inventory"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.product.name_en} - {self.quantity} units"
    
    def is_low_stock(self):
        return self.quantity <= self.reorder_level

# 9. Settings/Config Models
class WishlistSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist_settings')
    auto_notify = models.BooleanField(default=True, help_text="Notify when wishlist items go on sale")
    public_wishlist = models.BooleanField(default=False, help_text="Make wishlist publicly visible")
    share_link = models.CharField(max_length=255, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Wishlist Settings"
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist Settings"

class DashboardSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_settings')
    theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ], default='auto')
    language = models.CharField(max_length=5, default='en')
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    dashboard_layout = models.JSONField(default=dict, help_text="Custom dashboard layout configuration")
    default_view = models.CharField(max_length=20, choices=[
        ('overview', 'Overview'),
        ('products', 'Products'),
        ('orders', 'Orders'),
        ('analytics', 'Analytics'),
    ], default='overview')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dashboard Settings"
    
    def __str__(self):
        return f"{self.user.username}'s Dashboard Settings"

# 10. Analytics and Dashboard Models
class DashboardStats(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    new_customers = models.PositiveIntegerField(default=0)
    active_customers = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Dashboard Statistics"
        unique_together = ['period', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.period} stats for {self.date}"

class ProductAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    conversion_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Analytics"
        unique_together = ['product', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.product.name_en} - {self.date}"

class RegionalAnalytics(models.Model):
    WILAYA_CHOICES = [
        ('adrar', 'أدرار'),
        ('chlef', 'الشلف'),
        ('laghouat', 'الأغواط'),
        ('oum_bouaghi', 'أم البواقي'),
        ('batna', 'باتنة'),
        ('bejaia', 'بجاية'),
        ('biskra', 'بسكرة'),
        ('bechar', 'بشار'),
        ('blida', 'البليدة'),
        ('bouira', 'البويرة'),
        ('tamanrasset', 'تمنراست'),
        ('tebessa', 'تبسة'),
        ('tlemcen', 'تلمسان'),
        ('tiaret', 'تيارت'),
        ('tizi_ouzou', 'تيزي وزو'),
        ('algiers', 'الجزائر'),
        ('djelfa', 'الجلفة'),
        ('jiel', 'جيجل'),
        ('setif', 'سطيف'),
        ('saida', 'سعيدة'),
        ('skikda', 'سكيكدة'),
        ('sidi_bel_abbes', 'سيدي بلعباس'),
        ('annaba', 'عنابة'),
        ('guelma', 'قالمة'),
        ('constantine', 'قسنطينة'),
        ('medea', 'المديية'),
        ('mostaganem', 'مستغانم'),
        ('msila', 'المسيلة'),
        ('mascara', 'معسكر'),
        ('ouargla', 'ورقلة'),
        ('oran', 'وهران'),
        ('el_bayadh', 'البيض'),
        ('illizi', 'إليزي'),
        ('bordj_bou_arreridj', 'برج بوعريريج'),
        ('boumerdes', 'بومرداس'),
        ('el_tarf', 'الطارف'),
        ('tindouf', 'تندوف'),
        ('tissemsilt', 'تيسمسيلت'),
        ('el_oued', 'الوادي'),
        ('khenchela', 'خنشلة'),
        ('souk_ahras', 'سوق أهراس'),
        ('tipaza', 'تيبازة'),
        ('mila', 'ميلة'),
        ('ain_defla', 'عين الدفلى'),
        ('naama', 'النعامة'),
        ('ain_temouchent', 'عين تموشنت'),
        ('ghardaia', 'غرداية'),
        ('relizane', 'غليزان'),
        ('timimoun', 'تيميمون'),
        (' Bordj_Badji_Mokhtar', 'برج باجي مختار'),
        ('ouled_djellal', 'أولاد جلال'),
        ('beni_mellal', 'بني ملال'),
        ('in_sal', 'عين صالح'),
        ('in_guezzam', 'عين قزام'),
        ('touggourt', 'تقرت'),
        ('djanet', 'جانت'),
        ('el_mghair', 'المغير'),
        ('el_menia', 'المنيعة'),
    ]
    
    wilaya = models.CharField(max_length=50, choices=WILAYA_CHOICES)
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    unique_customers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Regional Analytics"
        unique_together = ['wilaya', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_wilaya_display()} - {self.date}"

class InvestorMetrics(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]
    
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    catalog_progress = models.FloatField(default=0.0, help_text="Percentage of catalog completion")
    sales_growth = models.FloatField(default=0.0, help_text="Sales growth percentage")
    active_investors = models.PositiveIntegerField(default=0)
    roi = models.FloatField(default=0.0, help_text="Return on Investment percentage")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Investor Metrics"
        unique_together = ['period', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.period} investor metrics for {self.date}"

class SalesForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecasts', null=True, blank=True)
    forecast_date = models.DateField()
    predicted_sales = models.PositiveIntegerField(default=0)
    predicted_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    confidence_score = models.FloatField(default=0.0, help_text="Confidence level 0-1")
    model_version = models.CharField(max_length=50, default='v1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Sales Forecasts"
        unique_together = ['product', 'forecast_date']
        ordering = ['-forecast_date']
    
    def __str__(self):
        if self.product:
            return f"Forecast for {self.product.name_en} - {self.forecast_date}"
        return f"Overall forecast - {self.forecast_date}"
