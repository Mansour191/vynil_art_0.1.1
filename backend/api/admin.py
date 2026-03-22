from django.contrib import admin
from .models import (
    UserProfile, Category, Material, Product, ProductImage, ProductVariant,
    Shipping, Coupon, Order, OrderItem, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine
)

# 1. Users & Auth
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')

# 2. Products
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'slug', 'waste_percent')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'price_per_m2', 'is_premium')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'category', 'base_price', 'sync_status', 'erpnext_item_code', 'on_sale', 'is_new')
    list_filter = ('category', 'on_sale', 'is_new')
    search_fields = ('name_en', 'name_ar')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [ProductImageInline, ProductVariantInline]

# 3. Orders
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'material', 'width', 'height', 'quantity', 'price')

class OrderTimelineInline(admin.TabularInline):
    model = OrderTimeline
    extra = 1

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('wilaya_id', 'name_fr', 'name_ar', 'stop_desk_price', 'home_delivery_price')
    search_fields = ('name_fr', 'name_ar', 'wilaya_id')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_to', 'active')
    list_filter = ('active',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer_name',
        'phone',
        'wilaya',
        'total',
        'status',
        'sync_status',
        'erpnext_sales_order_id',
        'created_at',
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'customer_name', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline, OrderTimelineInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'transaction_id', 'amount', 'status', 'created_at')

# 4. Cart & Wishlist
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')

# 5. Reviews
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_at')

# 6. Designs
@admin.register(DesignCategory)
class DesignCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'category', 'creator', 'created_at')

# 7. Notifications & Alerts
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('type', 'message', 'is_active', 'created_at')

# 8. ERPNext Integration
@admin.register(ERPNextSyncLog)
class ERPNextSyncLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'timestamp')

# 9. Analytics & AI
@admin.register(BehaviorTracking)
class BehaviorTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'timestamp')

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('target_metric', 'predicted_value', 'confidence_score', 'forecast_date')

@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PricingEngine)
class PricingEngineAdmin(admin.ModelAdmin):
    list_display = ('raw_material_cost', 'labor_cost', 'international_shipping')
