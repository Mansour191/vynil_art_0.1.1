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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=50) # page_view, add_to_cart, search
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

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
