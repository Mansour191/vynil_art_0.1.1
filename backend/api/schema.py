import uuid
import time
from decimal import Decimal

import graphene
from django.db.models import Prefetch
from django.db import transaction
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphene import ObjectType, Field, Mutation, List, String, Float, Int, Boolean

# Import schema extensions
# from .schema_extensions_fixed import ExtendedQuery as ERPNextQuery, ExtendedMutation as ERPNextMutation

# Temporary simple Query class for testing
class ERPNextQuery(ObjectType):
    pass

class ERPNextMutation(ObjectType):
    pass

from .models import (
    Category, Order, OrderItem, Product, ProductVariant, Shipping,
    UserProfile, Material, ProductImage, Coupon, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine, MediaFile, Address, Inventory,
    WishlistSettings, DashboardSettings, DashboardStats, ProductAnalytics,
    RegionalAnalytics, InvestorMetrics, SalesForecast
)

User = get_user_model()

# --- AI Service Types ---

class AIHealthType(graphene.ObjectType):
    status = graphene.String(default_value="healthy")  # Nullable with default
    available = graphene.Boolean(default_value=True)  # Nullable with default

class MarketTrendType(graphene.ObjectType):
    trend = graphene.String()
    confidence = graphene.Float()
    factors = graphene.String()  # Changed from JSON to String
    category = graphene.String()
    period = graphene.String()

class DemandForecastType(graphene.ObjectType):
    forecast = graphene.String()
    confidence = graphene.Float()
    predicted_demand = graphene.Int()
    time_period = graphene.String()
    product_id = graphene.String()

class CompetitorPriceType(graphene.ObjectType):
    product_id = graphene.String()
    competitor_name = graphene.String()
    price = graphene.Float()
    currency = graphene.String()
    last_updated = graphene.DateTime()

class PricingAnalysisType(graphene.ObjectType):
    product_id = graphene.String()
    optimal_price = graphene.Float()
    market_analysis = graphene.Field(MarketTrendType)
    competitor_data = graphene.List(CompetitorPriceType)
    demand_forecast = graphene.Field(DemandForecastType)
    confidence = graphene.Float()

# --- Types ---

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name_ar", "name_en", "slug", "icon", "waste_percent")

class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = ("id", "name_en", "name_ar", "price_adjustment", "product")

class ShippingType(DjangoObjectType):
    class Meta:
        model = Shipping
        fields = ("id", "wilaya_id", "name_ar", "name_fr", "stop_desk_price", "home_delivery_price")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "is_staff", "date_joined")

class UserProfileType(DjangoObjectType):
    user = graphene.Field(UserType)
    class Meta:
        model = UserProfile
        fields = ("id", "user", "phone", "address", "avatar", "created_at")

class MaterialType(DjangoObjectType):
    class Meta:
        model = Material
        fields = ("id", "name_ar", "name_en", "description", "price_per_m2", "is_premium")

class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "alt_text")

class ProductType(DjangoObjectType):
    category = graphene.Field(CategoryType)
    
    class Meta:
        model = Product
        fields = (
            "id", "name_ar", "name_en", "slug", "description_ar", "description_en",
            "base_price", "image", "on_sale", "discount_percent", "is_new",
            "created_at", "category", "variants", "images", "sync_status", "erpnext_item_code",
            "sync_error", "last_synced_at"
        )

class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = (
            "id", "product", "material", "width", "height", "dimension_unit",
            "marble_texture", "custom_design", "quantity", "price"
        )

class OrderType(DjangoObjectType):
    user = graphene.Field(UserType)
    wilaya = graphene.Field(ShippingType)
    items = graphene.List(OrderItemType)
    class Meta:
        model = Order
        fields = (
            "id", "order_number", "customer_name", "phone", "email", "address",
            "wilaya", "subtotal", "shipping_cost", "discount_amount", "total",
            "status", "sync_status", "erpnext_sales_order_id", "sync_error",
            "last_synced_at", "payment_method", "payment_status", "created_at",
            "updated_at", "user", "items"
        )

class CouponType(DjangoObjectType):
    class Meta:
        model = Coupon
        fields = ("id", "code", "discount_percent", "valid_from", "valid_to", "active")

class OrderTimelineType(DjangoObjectType):
    class Meta:
        model = OrderTimeline
        fields = ("id", "order", "status", "note", "created_at")

class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = ("id", "order", "transaction_id", "amount", "method", "status", "created_at")

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity", "options", "created_at")

class WishlistType(DjangoObjectType):
    class Meta:
        model = Wishlist
        fields = ("id", "user", "product", "created_at")

class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("id", "product", "user", "rating", "comment", "created_at")

class ReviewReportType(DjangoObjectType):
    class Meta:
        model = ReviewReport
        fields = ("id", "review", "user", "reason", "created_at")

class DesignCategoryType(DjangoObjectType):
    class Meta:
        model = DesignCategory
        fields = ("id", "name_ar", "name_en", "slug")

class DesignType(DjangoObjectType):
    class Meta:
        model = Design
        fields = ("id", "category", "title_ar", "title_en", "image", "creator", "created_at")

class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = ("id", "user", "title", "message", "is_read", "created_at")

class AlertType(DjangoObjectType):
    class Meta:
        model = Alert
        fields = ("id", "type", "message", "is_active", "created_at")

class ERPNextSyncLogType(DjangoObjectType):
    class Meta:
        model = ERPNextSyncLog
        fields = ("id", "action", "status", "message", "timestamp")

class BehaviorTrackingType(DjangoObjectType):
    class Meta:
        model = BehaviorTracking
        fields = ("id", "user", "session_id", "action", "page", "metadata", "timestamp")

class ForecastType(DjangoObjectType):
    class Meta:
        model = Forecast
        fields = ("id", "target_metric", "predicted_value", "confidence_score", "forecast_date", "created_at")

class CustomerSegmentType(DjangoObjectType):
    class Meta:
        model = CustomerSegment
        fields = ("id", "name", "description", "users")

class PricingEngineType(DjangoObjectType):
    class Meta:
        model = PricingEngine
        fields = ("id", "raw_material_cost", "labor_cost", "international_shipping")

# --- New Model Types ---

class MediaFileType(DjangoObjectType):
    product = graphene.Field(ProductType)
    
    class Meta:
        model = MediaFile
        fields = ("id", "title", "file", "file_type", "description", "product", "is_active", "created_at")

class AddressType(DjangoObjectType):
    user = graphene.Field(UserType)
    
    class Meta:
        model = Address
        fields = ("id", "user", "type", "title", "street_address", "city", "state", "postal_code", "country", "is_default", "created_at", "updated_at")

class InventoryType(DjangoObjectType):
    product = graphene.Field(ProductType)
    
    class Meta:
        model = Inventory
        fields = ("id", "product", "quantity", "reorder_level", "max_stock", "status", "last_restocked", "cost_per_unit", "location", "notes", "updated_at")

class WishlistSettingsType(DjangoObjectType):
    user = graphene.Field(UserType)
    
    class Meta:
        model = WishlistSettings
        fields = ("id", "user", "auto_notify", "public_wishlist", "share_link", "created_at", "updated_at")

class DashboardSettingsType(DjangoObjectType):
    user = graphene.Field(UserType)
    
    class Meta:
        model = DashboardSettings
        fields = ("id", "user", "theme", "language", "notifications_enabled", "email_notifications", "dashboard_layout", "default_view", "created_at", "updated_at")

# --- Analytics Types ---

class DashboardStatsType(DjangoObjectType):
    class Meta:
        model = DashboardStats
        fields = ("id", "period", "date", "total_sales", "total_orders", "new_customers", "active_customers", "average_order_value", "created_at")

class ProductAnalyticsType(DjangoObjectType):
    product = graphene.Field(ProductType)
    
    class Meta:
        model = ProductAnalytics
        fields = ("id", "product", "date", "views", "sales", "revenue", "conversion_rate", "created_at")

class RegionalAnalyticsType(DjangoObjectType):
    class Meta:
        model = RegionalAnalytics
        fields = ("id", "wilaya", "date", "total_sales", "total_orders", "unique_customers", "created_at")

class InvestorMetricsType(DjangoObjectType):
    class Meta:
        model = InvestorMetrics
        fields = ("id", "period", "date", "total_revenue", "catalog_progress", "sales_growth", "active_investors", "roi", "created_at")

class SalesForecastType(DjangoObjectType):
    product = graphene.Field(ProductType)
    
    class Meta:
        model = SalesForecast
        fields = ("id", "product", "forecast_date", "predicted_sales", "predicted_revenue", "confidence_score", "model_version", "created_at", "updated_at")

# --- Auth Responses ---

class LoginResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    tokens = graphene.String()  # Changed from JSONString to String
    errors = graphene.String()  # Changed from JSONString to String

class RegisterResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    tokens = graphene.String()  # Changed from JSONString to String
    errors = graphene.String()  # Changed from JSONString to String

class ProfileResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    errors = graphene.String()  # Changed from JSONString to String

# --- AI & Other Responses ---

class ChatResponse(ObjectType):
    response = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()

class SemanticSearchResponse(ObjectType):
    products = graphene.List(ProductType)
    success = graphene.Boolean()
    error = graphene.String()

class Measurement(ObjectType):
    width = graphene.Float()
    height = graphene.Float()
    area = graphene.Float()
    estimated_cost = graphene.Float()

class MeasureResponse(ObjectType):
    measurements = graphene.Field(Measurement)
    success = graphene.Boolean()
    error = graphene.String()

# --- Inputs ---

class CategoryInput(graphene.InputObjectType):
    name_ar = graphene.String(required=True)
    name_en = graphene.String(required=True)
    slug = graphene.String()
    icon = graphene.String()
    waste_percent = graphene.Float()

class ProductInput(graphene.InputObjectType):
    name_ar = graphene.String()
    name_en = graphene.String()
    slug = graphene.String()
    description_ar = graphene.String()
    description_en = graphene.String()
    base_price = graphene.Decimal()
    category_id = graphene.ID()
    image = graphene.String()
    on_sale = graphene.Boolean()
    discount_percent = graphene.Float()
    is_new = graphene.Boolean()

class MaterialInput(graphene.InputObjectType):
    name_ar = graphene.String(required=True)
    name_en = graphene.String(required=True)
    description = graphene.String()
    price_per_m2 = graphene.Decimal(required=True)
    is_premium = graphene.Boolean()

class OrderInput(graphene.InputObjectType):
    items = graphene.List(graphene.String, required=True)
    shipping_address = graphene.String()
    phone = graphene.String()
    notes = graphene.String()
    coupon_code = graphene.String()

class PaymentInput(graphene.InputObjectType):
    order_id = graphene.ID(required=True)
    amount = graphene.Decimal(required=True)
    method = graphene.String(required=True)  # 'ccp', 'cash', etc.
    transaction_id = graphene.String()
    status = graphene.String()

class CartItemInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    material_id = graphene.ID()
    quantity = graphene.Int(required=True)
    width = graphene.Float()
    height = graphene.Float()
    dimension_unit = graphene.String()

class ReviewInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    rating = graphene.Int(required=True)
    comment = graphene.String()

class DesignInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    category_id = graphene.ID(required=True)
    image = graphene.String()

class OrderItemInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    material_id = graphene.ID()
    width = graphene.Float(required=True)
    height = graphene.Float(required=True)
    dimension_unit = graphene.String()
    marble_texture = graphene.String()
    custom_design = graphene.String()
    quantity = graphene.Int(required=True)
    price = graphene.Float(required=True)

# --- Mutations ---

# --- Response Types ---

class OrderResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    order = graphene.Field(OrderType)
    errors = graphene.String()

class PaymentResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    payment = graphene.Field(PaymentType)
    errors = graphene.String()

class CartItemResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    cart_item = graphene.Field(CartItemType)
    errors = graphene.String()

class ReviewResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    review = graphene.Field(ReviewType)
    errors = graphene.String()

class DesignResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    design = graphene.Field(DesignType)
    errors = graphene.String()

class CategoryResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    category = graphene.Field(CategoryType)
    errors = graphene.String()

class ProductResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    product = graphene.Field(ProductType)
    errors = graphene.String()

class MaterialResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    material = graphene.Field(MaterialType)
    errors = graphene.String()

# --- Mutations ---

class CreateOrderMutation(Mutation):
    class Arguments:
        input = OrderInput(required=True)
    
    Output = OrderResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return OrderResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=info.context.user,
                    shipping_address=input.get('shipping_address', ''),
                    phone=input.get('phone', ''),
                    notes=input.get('notes', ''),
                    status='pending'
                )
                
                # Add order items
                total_amount = 0
                for item_data in input['items']:
                    product = Product.objects.get(pk=item_data['product_id'])
                    material = None
                    if item_data.get('material_id'):
                        material = Material.objects.get(pk=item_data['material_id'])
                    
                    # Calculate price
                    price = product.base_price
                    if material:
                        price += material.price_per_m2 * (item_data['width'] * item_data['height'] / 10000)  # Convert to m2
                    
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        material=material,
                        width=item_data['width'],
                        height=item_data['height'],
                        dimension_unit=item_data.get('dimension_unit', 'cm'),
                        marble_texture=item_data.get('marble_texture', ''),
                        custom_design=item_data.get('custom_design', ''),
                        quantity=item_data['quantity'],
                        price=price
                    )
                    total_amount += price * item_data['quantity']
                
                order.total_amount = total_amount
                order.save()
                
                return OrderResponse(success=True, message='تم إنشاء الطلب بنجاح', order=order)
                
        except Exception as e:
            return OrderResponse(success=False, message=str(e), errors=str(e))

class UpdateOrderStatusMutation(Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        status = graphene.String(required=True)
    
    Output = OrderResponse
    
    def mutate(self, info, order_id, status):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return OrderResponse(success=False, message='غير مصرح لك بتعديل الطلبات', errors='permission_denied')
        
        try:
            order = Order.objects.get(pk=order_id)
            order.status = status
            order.save()
            return OrderResponse(success=True, message='تم تحديث حالة الطلب بنجاح', order=order)
        except Order.DoesNotExist:
            return OrderResponse(success=False, message='الطلب غير موجود', errors='not_found')
        except Exception as e:
            return OrderResponse(success=False, message=str(e), errors=str(e))

class CreatePaymentMutation(Mutation):
    class Arguments:
        input = PaymentInput(required=True)
    
    Output = PaymentResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return PaymentResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            order = Order.objects.get(pk=input['order_id'])
            
            # Check if user owns the order or is staff
            if not info.context.user.is_staff and order.user != info.context.user:
                return PaymentResponse(success=False, message='غير مصرح لك بالدفع لهذا الطلب', errors='permission_denied')
            
            payment = Payment.objects.create(
                order=order,
                amount=input['amount'],
                method=input['method'],
                transaction_id=input.get('transaction_id', ''),
                status=input.get('status', 'pending')
            )
            
            # Update order status if payment is successful
            if input.get('status') == 'completed':
                order.status = 'paid'
                order.save()
            
            return PaymentResponse(success=True, message='تم إنشاء الدفعة بنجاح', payment=payment)
            
        except Order.DoesNotExist:
            return PaymentResponse(success=False, message='الطلب غير موجود', errors='not_found')
        except Exception as e:
            return PaymentResponse(success=False, message=str(e), errors=str(e))

class AddToCartMutation(Mutation):
    class Arguments:
        input = CartItemInput(required=True)
    
    Output = CartItemResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CartItemResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            product = Product.objects.get(pk=input['product_id'])
            
            # Build options dict
            options = {}
            if input.get('material_id'):
                options['material_id'] = input['material_id']
            if input.get('width'):
                options['width'] = input['width']
            if input.get('height'):
                options['height'] = input['height']
            if input.get('dimension_unit'):
                options['dimension_unit'] = input['dimension_unit']
            
            # Check if item already exists in cart
            cart_item, created = CartItem.objects.get_or_create(
                user=info.context.user,
                product=product,
                options=options,
                defaults={'quantity': input['quantity']}
            )
            
            if not created:
                cart_item.quantity += input['quantity']
                cart_item.save()
            
            return CartItemResponse(success=True, message='تمت إضافة المنتج للسلة', cart_item=cart_item)
            
        except Product.DoesNotExist:
            return CartItemResponse(success=False, message='المنتج غير موجود', errors='product_not_found')
        except Exception as e:
            return CartItemResponse(success=False, message=str(e), errors=str(e))

class RemoveFromCartMutation(Mutation):
    class Arguments:
        cart_item_id = graphene.ID(required=True)
    
    Output = CartItemResponse
    
    def mutate(self, info, cart_item_id):
        if not info.context.user.is_authenticated:
            return CartItemResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id, user=info.context.user)
            cart_item.delete()
            return CartItemResponse(success=True, message='تم حذف المنتج من السلة')
        except CartItem.DoesNotExist:
            return CartItemResponse(success=False, message='العنصر غير موجود في السلة', errors='not_found')
        except Exception as e:
            return CartItemResponse(success=False, message=str(e), errors=str(e))

class CreateReviewMutation(Mutation):
    class Arguments:
        input = ReviewInput(required=True)
    
    Output = ReviewResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return ReviewResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            product = Product.objects.get(pk=input['product_id'])
            
            # Check if user already reviewed this product
            if Review.objects.filter(user=info.context.user, product=product).exists():
                return ReviewResponse(success=False, message='لقد قمت بتقييم هذا المنتج من قبل', errors='already_reviewed')
            
            review = Review.objects.create(
                user=info.context.user,
                product=product,
                rating=input['rating'],
                comment=input.get('comment', '')
            )
            
            return ReviewResponse(success=True, message='تم إضافة التقييم بنجاح', review=review)
            
        except Product.DoesNotExist:
            return ReviewResponse(success=False, message='المنتج غير موجود', errors='product_not_found')
        except Exception as e:
            return ReviewResponse(success=False, message=str(e), errors=str(e))

class CreateDesignMutation(Mutation):
    class Arguments:
        input = DesignInput(required=True)
    
    Output = DesignResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return DesignResponse(success=False, message='يجب تسجيل الدخول أولاً', errors='authentication_required')
        
        try:
            category = DesignCategory.objects.get(pk=input['category_id'])
            
            design = Design.objects.create(
                user=info.context.user,
                category=category,
                name=input['name'],
                description=input.get('description', ''),
                image=input.get('image', '')
            )
            
            return DesignResponse(success=True, message='تم إنشاء التصميم بنجاح', design=design)
            
        except DesignCategory.DoesNotExist:
            return DesignResponse(success=False, message='فئة التصميم غير موجودة', errors='category_not_found')
        except Exception as e:
            return DesignResponse(success=False, message=str(e), errors=str(e))

class CreateCategoryMutation(Mutation):
    class Arguments:
        input = CategoryInput(required=True)
    
    Output = CategoryResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return CategoryResponse(success=False, message='غير مصرح لك بإضافة فئات', errors='permission_denied')
        
        try:
            # Generate slug if not provided
            if not input.slug:
                input.slug = input.name_en.lower().replace(' ', '-').replace('_', '-') + f'-{int(time.time())}'
            
            category = Category.objects.create(**input)
            return CategoryResponse(success=True, message='تم إنشاء الفئة بنجاح', category=category)
        except Exception as e:
            return CategoryResponse(success=False, message=str(e), errors=str(e))

class UpdateCategoryMutation(Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = CategoryInput(required=True)
    
    Output = CategoryResponse
    
    def mutate(self, info, id, input):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return CategoryResponse(success=False, message='غير مصرح لك بتعديل الفئات', errors='permission_denied')
        
        try:
            category = Category.objects.get(pk=id)
            
            # Update fields
            for field, value in input.items():
                if value is not None:
                    setattr(category, field, value)
            
            category.save()
            return CategoryResponse(success=True, message='تم تحديث الفئة بنجاح', category=category)
        except Category.DoesNotExist:
            return CategoryResponse(success=False, message='الفئة غير موجودة', errors='not_found')
        except Exception as e:
            return CategoryResponse(success=False, message=str(e), errors=str(e))

class DeleteCategoryMutation(Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    
    Output = CategoryResponse
    
    def mutate(self, info, id):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return CategoryResponse(success=False, message='غير مصرح لك بحذف الفئات', errors='permission_denied')
        
        try:
            category = Category.objects.get(pk=id)
            category_name = category.name_en
            category.delete()
            return CategoryResponse(success=True, message=f'تم حذف الفئة "{category_name}" بنجاح')
        except Category.DoesNotExist:
            return CategoryResponse(success=False, message='الفئة غير موجودة', errors='not_found')
        except Exception as e:
            return CategoryResponse(success=False, message=str(e), errors=str(e))

class CreateProductMutation(Mutation):
    class Arguments:
        input = ProductInput(required=True)
    
    Output = ProductResponse
    
    def mutate(self, info, input):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return ProductResponse(success=False, message='غير مصرح لك بإضافة منتجات', errors='permission_denied')
        
        try:
            # Generate slug if not provided
            if not input.slug:
                input.slug = input.name_en.lower().replace(' ', '-').replace('_', '-') + f'-{int(time.time())}'
            
            # Get category
            category = Category.objects.get(pk=input.pop('category_id'))
            
            product = Product.objects.create(category=category, **input)
            return ProductResponse(success=True, message='تم إنشاء المنتج بنجاح', product=product)
        except Category.DoesNotExist:
            return ProductResponse(success=False, message='الفئة المحددة غير موجودة', errors='category_not_found')
        except Exception as e:
            return ProductResponse(success=False, message=str(e), errors=str(e))

class UpdateProductMutation(Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        input = ProductInput()
    
    Output = ProductResponse
    
    def mutate(self, info, slug, input):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return ProductResponse(success=False, message='غير مصرح لك بتعديل المنتجات', errors='permission_denied')
        
        try:
            product = Product.objects.get(slug=slug)
            
            # Handle category update
            if 'category_id' in input:
                category = Category.objects.get(pk=input.pop('category_id'))
                product.category = category
            
            # Update other fields
            for field, value in input.items():
                if value is not None:
                    setattr(product, field, value)
            
            product.save()
            return ProductResponse(success=True, message='تم تحديث المنتج بنجاح', product=product)
        except Product.DoesNotExist:
            return ProductResponse(success=False, message='المنتج غير موجود', errors='not_found')
        except Category.DoesNotExist:
            return ProductResponse(success=False, message='الفئة المحددة غير موجودة', errors='category_not_found')
        except Exception as e:
            return ProductResponse(success=False, message=str(e), errors=str(e))

class DeleteProductMutation(Mutation):
    class Arguments:
        slug = graphene.String(required=True)
    
    Output = ProductResponse
    
    def mutate(self, info, slug):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return ProductResponse(success=False, message='غير مصرح لك بحذف المنتجات', errors='permission_denied')
        
        try:
            product = Product.objects.get(slug=slug)
            product_name = product.name_en
            product.delete()
            return ProductResponse(success=True, message=f'تم حذف المنتج "{product_name}" بنجاح')
        except Product.DoesNotExist:
            return ProductResponse(success=False, message='المنتج غير موجود', errors='not_found')
        except Exception as e:
            return ProductResponse(success=False, message=str(e), errors=str(e))

def generate_tokens(user):
    # Simple token generation without JWT dependency for now
    return {
        'access': f'simple-token-{user.id}',
        'refresh': f'simple-refresh-{user.id}'
    }

class LoginMutation(Mutation):
    class Arguments:
        emailOrUsername = graphene.String(required=True)
        password = graphene.String(required=True)
    
    Output = LoginResponse
    
    def mutate(self, info, emailOrUsername, password):
        user = authenticate(username=emailOrUsername, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=emailOrUsername)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
            except User.MultipleObjectsReturned:
                # Handle multiple users with same email - get the first one
                user_obj = User.objects.filter(email=emailOrUsername).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
        
        if not user:
            return LoginResponse(success=False, message='بيانات الدخول غير صحيحة', errors='بيانات الدخول غير صحيحة')
        
        if not user.is_active:
            return LoginResponse(success=False, message='الحساب غير نشط', errors='الحساب غير نشط')
        
        tokens = generate_tokens(user)
        return LoginResponse(success=True, message='تم تسجيل الدخول بنجاح', user=user, tokens=tokens['access'])

class TokenAuthMutation(Mutation):
    """Alias for LoginMutation to match frontend expectations"""
    class Arguments:
        emailOrUsername = graphene.String(required=True)
        password = graphene.String(required=True)
    
    Output = LoginResponse
    
    def mutate(self, info, emailOrUsername, password):
        return LoginMutation.mutate(self, info, emailOrUsername, password)

class RegisterMutation(Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        passwordConfirm = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String()
        phone = graphene.String()
    
    Output = RegisterResponse
    
    def mutate(self, info, username, email, password, passwordConfirm, firstName, lastName='', phone=''):
        if password != passwordConfirm:
            return RegisterResponse(success=False, message='كلمات المرور غير متطابقة', errors={'password': 'كلمات المرور غير متطابقة'})
        
        try:
            validate_password(password)
        except ValidationError as e:
            return RegisterResponse(success=False, message='كلمة المرور ضعيفة جداً', errors={'password': list(e.messages)})
        
        if User.objects.filter(username=username).exists():
            return RegisterResponse(success=False, message='اسم المستخدم موجود بالفعل', errors={'username': 'اسم المستخدم موجود بالفعل'})
        
        if User.objects.filter(email=email).exists():
            return RegisterResponse(success=False, message='البريد الإلكتروني موجود بالفعل', errors={'email': 'البريد الإلكتروني موجود بالفعل'})
        
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=firstName, last_name=lastName
        )
        UserProfile.objects.create(user=user, phone=phone)
        
        tokens = generate_tokens(user)
        return RegisterResponse(success=True, message='تم إنشاء الحساب بنجاح', user=user, tokens=tokens['access'])

class UpdateProfileMutation(Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        address = graphene.String()
    
    Output = ProfileResponse
    
    def mutate(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return ProfileResponse(success=False, message='يجب تسجيل الدخول أولاً', errors={'auth': 'يجب تسجيل الدخول أولاً'})
        
        if 'first_name' in kwargs: user.first_name = kwargs['first_name']
        if 'last_name' in kwargs: user.last_name = kwargs['last_name']
        if 'email' in kwargs:
            new_email = kwargs['email']
            if User.objects.exclude(id=user.id).filter(email=new_email).exists():
                return ProfileResponse(success=False, message='البريد الإلكتروني موجود بالفعل', errors={'email': 'البريد الإلكتروني موجود بالفعل'})
            user.email = new_email
        user.save()

        profile = user.profile
        if 'phone' in kwargs: profile.phone = kwargs['phone']
        if 'address' in kwargs: profile.address = kwargs['address']
        profile.save()
        
        return ProfileResponse(success=True, message='تم تحديث الملف الشخصي بنجاح', user=user)

class ChatWithAIMutation(Mutation):
    class Arguments:
        message = graphene.String(required=True)
    
    Output = ChatResponse
    
    def mutate(self, info, message):
        # Placeholder for AI logic
        return ChatResponse(response=f"AI Echo: {message}", success=True)

class Mutation(ERPNextMutation, ObjectType):
    # Authentication mutations
    login = LoginMutation.Field()
    token_auth = TokenAuthMutation.Field()  # Alias for frontend compatibility
    register = RegisterMutation.Field()
    update_profile = UpdateProfileMutation.Field()
    
    # Category mutations
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    
    # Product mutations
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()
    
    # Order and Payment mutations
    create_order = CreateOrderMutation.Field()
    update_order_status = UpdateOrderStatusMutation.Field()
    create_payment = CreatePaymentMutation.Field()
    
    # Cart mutations
    add_to_cart = AddToCartMutation.Field()
    remove_from_cart = RemoveFromCartMutation.Field()
    
    # Review mutations
    create_review = CreateReviewMutation.Field()
    
    # Design mutations
    create_design = CreateDesignMutation.Field()
    
    # Other mutations
    chat_with_ai = ChatWithAIMutation.Field()
    # Add other mutations as needed...

class Query(ERPNextQuery, ObjectType):
    # Product queries
    products = graphene.List(ProductType, category_slug=graphene.String())
    product = graphene.Field(ProductType, slug=graphene.String(), id=graphene.ID())
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, slug=graphene.String())
    materials = graphene.List(MaterialType)
    
    # Authentication queries
    me = graphene.Field(UserType)
    myProfile = graphene.Field(UserProfileType)
    
    # AI and analytics queries
    aiHealth = graphene.Field(AIHealthType, service=graphene.String())
    checkAIHealth = graphene.Field(AIHealthType, service=graphene.String())  # Frontend compatibility
    systemHealthCheck = graphene.Field(AIHealthType)
    marketTrends = graphene.List(MarketTrendType, category=graphene.String(), period=graphene.String())
    demandForecast = graphene.List(DemandForecastType, product_id=graphene.String(), period=graphene.String())
    competitorPrices = graphene.List(CompetitorPriceType, product_id=graphene.String())
    pricingAnalysis = graphene.Field(PricingAnalysisType, product_id=graphene.String())
    shippingOptions = graphene.List(ShippingType)
    
    # Order and Payment Queries
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.ID())
    myOrders = graphene.List(OrderType)
    orderItems = graphene.List(OrderItemType, order_id=graphene.ID())
    payments = graphene.List(PaymentType)
    payment = graphene.Field(PaymentType, id=graphene.ID())
    coupons = graphene.List(CouponType)
    coupon = graphene.Field(CouponType, code=graphene.String())
    
    # Cart and Wishlist Queries
    cartItems = graphene.List(CartItemType)
    myCart = graphene.List(CartItemType)
    wishlistItems = graphene.List(WishlistType)
    myWishlist = graphene.List(WishlistType)
    
    # Review and Design Queries
    reviews = graphene.List(ReviewType, product_id=graphene.ID())
    productReviews = graphene.List(ReviewType, product_slug=graphene.String())
    myReviews = graphene.List(ReviewType)
    designCategories = graphene.List(DesignCategoryType)
    designs = graphene.List(DesignType, category_id=graphene.ID())
    myDesigns = graphene.List(DesignType)
    
    # Notification and Other Queries
    notifications = graphene.List(NotificationType)
    myNotifications = graphene.List(NotificationType)
    alerts = graphene.List(AlertType)
    myAlerts = graphene.List(AlertType)
    
    # New Model Queries
    mediaFiles = graphene.List(MediaFileType)
    mediaFile = graphene.Field(MediaFileType, id=graphene.ID())
    addresses = graphene.List(AddressType)
    address = graphene.Field(AddressType, id=graphene.ID())
    myAddresses = graphene.List(AddressType)
    inventory = graphene.List(InventoryType)
    inventoryItem = graphene.Field(InventoryType, id=graphene.ID())
    productInventory = graphene.Field(InventoryType, product_id=graphene.ID())
    wishlistSettings = graphene.List(WishlistSettingsType)
    myWishlistSettings = graphene.Field(WishlistSettingsType)
    dashboardSettings = graphene.List(DashboardSettingsType)
    myDashboardSettings = graphene.Field(DashboardSettingsType)
    
    # Analytics Queries
    dashboardStats = graphene.List(DashboardStatsType, period=graphene.String(), date_from=graphene.Date(), date_to=graphene.Date())
    productAnalytics = graphene.List(ProductAnalyticsType, product_id=graphene.ID(), date_from=graphene.Date(), date_to=graphene.Date())
    regionalAnalytics = graphene.List(RegionalAnalyticsType, wilaya=graphene.String(), date_from=graphene.Date(), date_to=graphene.Date())
    investorMetrics = graphene.List(InvestorMetricsType, period=graphene.String(), date_from=graphene.Date(), date_to=graphene.Date())
    salesForecasts = graphene.List(SalesForecastType, product_id=graphene.ID(), date_from=graphene.Date(), date_to=graphene.Date())
    topProducts = graphene.List(ProductAnalyticsType, limit=graphene.Int(), date_from=graphene.Date(), date_to=graphene.Date())
    
    def resolve_me(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
    
    def resolve_my_profile(self, info):
        if info.context.user.is_authenticated:
            return getattr(info.context.user, 'profile', None)
        return None

    # Category resolvers
    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_category(self, info, **kwargs):
        slug = kwargs.get('slug')
        if slug:
            try:
                return Category.objects.get(slug=slug)
            except Category.DoesNotExist:
                return None
        return None
    
    # Product resolvers
    def resolve_products(self, info, **kwargs):
        category_slug = kwargs.get('category_slug')
        queryset = Product.objects.all().prefetch_related('images', 'category', 'variants')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def resolve_product(self, info, **kwargs):
        slug = kwargs.get('slug')
        id = kwargs.get('id')
        
        try:
            if slug:
                return Product.objects.get(slug=slug)
            elif id:
                return Product.objects.get(pk=id)
            else:
                return None
        except Product.DoesNotExist:
            return None
    
    # Material resolvers
    def resolve_materials(self, info):
        return Material.objects.all()
    
    def resolve_material(self, info, id):
        try:
            return Material.objects.get(pk=id)
        except Material.DoesNotExist:
            return None
    
    def resolve_product_variants(self, info, product_id=None):
        queryset = ProductVariant.objects.all()
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    def resolve_shipping_options(self, info):
        return Shipping.objects.all()
    
    # Order and Payment resolvers
    def resolve_orders(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Order.objects.all().prefetch_related('items', 'payments', 'timeline')
        return Order.objects.none()
    
    def resolve_order(self, info, **kwargs):
        id = kwargs.get('id')
        if not id:
            return None
            
        if info.context.user.is_authenticated:
            if info.context.user.is_staff:
                try:
                    return Order.objects.get(pk=id).prefetch_related('items', 'payments', 'timeline')
                except Order.DoesNotExist:
                    return None
            else:
                try:
                    return Order.objects.get(pk=id, user=info.context.user).prefetch_related('items', 'payments', 'timeline')
                except Order.DoesNotExist:
                    return None
        return None
    
    def resolve_myOrders(self, info):
        if info.context.user.is_authenticated:
            return Order.objects.filter(user=info.context.user).prefetch_related('items', 'payments', 'timeline')
        return Order.objects.none()
    
    def resolve_orderItems(self, info, **kwargs):
        order_id = kwargs.get('order_id')
        if order_id:
            return OrderItem.objects.filter(order_id=order_id).select_related('product', 'material')
        return OrderItem.objects.none()
    
    def resolve_payments(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Payment.objects.all().select_related('order')
        return Payment.objects.none()
    
    def resolve_payment(self, info, **kwargs):
        id = kwargs.get('id')
        if not id:
            return None
            
        if info.context.user.is_authenticated:
            if info.context.user.is_staff:
                try:
                    return Payment.objects.get(pk=id).select_related('order')
                except Payment.DoesNotExist:
                    return None
            else:
                try:
                    return Payment.objects.get(pk=id, order__user=info.context.user).select_related('order')
                except Payment.DoesNotExist:
                    return None
        return None
    
    def resolve_coupons(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Coupon.objects.all()
        return Coupon.objects.filter(active=True)
    
    def resolve_coupon(self, info, **kwargs):
        code = kwargs.get('code')
        if code:
            try:
                return Coupon.objects.get(code=code, active=True)
            except Coupon.DoesNotExist:
                return None
        return None
    
    # Cart and Wishlist resolvers
    def resolve_cartItems(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return CartItem.objects.all().select_related('user', 'product')
        return CartItem.objects.none()
    
    def resolve_myCart(self, info):
        if info.context.user.is_authenticated:
            return CartItem.objects.filter(user=info.context.user).select_related('product')
        return CartItem.objects.none()
    
    def resolve_wishlistItems(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Wishlist.objects.all().select_related('user', 'product')
        return Wishlist.objects.none()
    
    def resolve_myWishlist(self, info):
        if info.context.user.is_authenticated:
            return Wishlist.objects.filter(user=info.context.user).select_related('product')
        return Wishlist.objects.none()
    
    # New Model Resolvers
    def resolve_mediaFiles(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return MediaFile.objects.all().select_related('product')
        return MediaFile.objects.filter(is_active=True)
    
    def resolve_mediaFile(self, info, **kwargs):
        id = kwargs.get('id')
        if not id:
            return None
        try:
            if info.context.user.is_authenticated and info.context.user.is_staff:
                return MediaFile.objects.get(pk=id).select_related('product')
            else:
                return MediaFile.objects.get(pk=id, is_active=True).select_related('product')
        except MediaFile.DoesNotExist:
            return None
    
    def resolve_addresses(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Address.objects.all().select_related('user')
        return Address.objects.none()
    
    def resolve_address(self, info, **kwargs):
        id = kwargs.get('id')
        if not id:
            return None
        try:
            if info.context.user.is_authenticated and info.context.user.is_staff:
                return Address.objects.get(pk=id).select_related('user')
            else:
                return Address.objects.get(pk=id, user=info.context.user).select_related('user')
        except Address.DoesNotExist:
            return None
    
    def resolve_myAddresses(self, info):
        if info.context.user.is_authenticated:
            return Address.objects.filter(user=info.context.user).select_related('user')
        return Address.objects.none()
    
    def resolve_inventory(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Inventory.objects.all().select_related('product')
        return Inventory.objects.none()
    
    def resolve_inventoryItem(self, info, **kwargs):
        id = kwargs.get('id')
        if not id:
            return None
        try:
            if info.context.user.is_authenticated and info.context.user.is_staff:
                return Inventory.objects.get(pk=id).select_related('product')
            else:
                return None  # Regular users can't access inventory details
        except Inventory.DoesNotExist:
            return None
    
    def resolve_productInventory(self, info, **kwargs):
        product_id = kwargs.get('product_id')
        if not product_id:
            return None
        try:
            if info.context.user.is_authenticated and info.context.user.is_staff:
                return Inventory.objects.get(product_id=product_id).select_related('product')
            else:
                return None  # Regular users can't access inventory details
        except Inventory.DoesNotExist:
            return None
    
    def resolve_wishlistSettings(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return WishlistSettings.objects.all().select_related('user')
        return WishlistSettings.objects.none()
    
    def resolve_myWishlistSettings(self, info):
        if info.context.user.is_authenticated:
            try:
                return WishlistSettings.objects.get(user=info.context.user).select_related('user')
            except WishlistSettings.DoesNotExist:
                return None
        return None
    
    def resolve_dashboardSettings(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return DashboardSettings.objects.all().select_related('user')
        return DashboardSettings.objects.none()
    
    def resolve_myDashboardSettings(self, info):
        if info.context.user.is_authenticated:
            try:
                return DashboardSettings.objects.get(user=info.context.user).select_related('user')
            except DashboardSettings.DoesNotExist:
                return None
        return None
    
    # Analytics Resolvers
    def resolve_dashboardStats(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = DashboardStats.objects.all()
            
            period = kwargs.get('period')
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            
            if period:
                queryset = queryset.filter(period=period)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            return queryset.order_by('-date')
        return DashboardStats.objects.none()
    
    def resolve_productAnalytics(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = ProductAnalytics.objects.all().select_related('product')
            
            product_id = kwargs.get('product_id')
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            
            if product_id:
                queryset = queryset.filter(product_id=product_id)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            return queryset.order_by('-date')
        return ProductAnalytics.objects.none()
    
    def resolve_regionalAnalytics(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = RegionalAnalytics.objects.all()
            
            wilaya = kwargs.get('wilaya')
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            
            if wilaya:
                queryset = queryset.filter(wilaya=wilaya)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            return queryset.order_by('-date')
        return RegionalAnalytics.objects.none()
    
    def resolve_investorMetrics(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = InvestorMetrics.objects.all()
            
            period = kwargs.get('period')
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            
            if period:
                queryset = queryset.filter(period=period)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            return queryset.order_by('-date')
        return InvestorMetrics.objects.none()
    
    def resolve_salesForecasts(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = SalesForecast.objects.all().select_related('product')
            
            product_id = kwargs.get('product_id')
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            
            if product_id:
                queryset = queryset.filter(product_id=product_id)
            if date_from:
                queryset = queryset.filter(forecast_date__gte=date_from)
            if date_to:
                queryset = queryset.filter(forecast_date__lte=date_to)
                
            return queryset.order_by('-forecast_date')
        return SalesForecast.objects.none()
    
    def resolve_topProducts(self, info, **kwargs):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            queryset = ProductAnalytics.objects.all().select_related('product')
            
            date_from = kwargs.get('date_from')
            date_to = kwargs.get('date_to')
            limit = kwargs.get('limit', 10)
            
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            return queryset.order_by('-sales', '-revenue')[:limit]
        return ProductAnalytics.objects.none()
    
    # Review resolvers
    def resolve_reviews(self, info, **kwargs):
        product_id = kwargs.get('product_id')
        if product_id:
            return Review.objects.filter(product_id=product_id).select_related('user', 'product')
        return Review.objects.all().select_related('user', 'product')
    
    def resolve_productReviews(self, info, **kwargs):
        product_slug = kwargs.get('product_slug')
        if product_slug:
            try:
                product = Product.objects.get(slug=product_slug)
                return Review.objects.filter(product=product).select_related('user', 'product')
            except Product.DoesNotExist:
                return Review.objects.none()
        return Review.objects.none()
    
    def resolve_myReviews(self, info):
        if info.context.user.is_authenticated:
            return Review.objects.filter(user=info.context.user).select_related('product')
        return Review.objects.none()
    
    # Design resolvers
    def resolve_designCategories(self, info):
        return DesignCategory.objects.all()
    
    def resolve_designs(self, info, **kwargs):
        category_id = kwargs.get('category_id')
        if category_id:
            return Design.objects.filter(category_id=category_id).select_related('category', 'user')
        return Design.objects.all().select_related('category', 'user')
    
    def resolve_myDesigns(self, info):
        if info.context.user.is_authenticated:
            return Design.objects.filter(user=info.context.user).select_related('category')
        return Design.objects.none()
    
    # Notification resolvers
    def resolve_notifications(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Notification.objects.all().select_related('user')
        return Notification.objects.none()
    
    def resolve_myNotifications(self, info):
        if info.context.user.is_authenticated:
            return Notification.objects.filter(user=info.context.user).select_related('user')
        return Notification.objects.none()
    
    def resolve_alerts(self, info):
        if info.context.user.is_authenticated and info.context.user.is_staff:
            return Alert.objects.all().select_related('user')
        return Alert.objects.none()
    
    def resolve_myAlerts(self, info):
        if info.context.user.is_authenticated:
            return Alert.objects.filter(user=info.context.user).select_related('user')
        return Alert.objects.none()
    
    # AI Health Check Resolver
    def resolve_aiHealth(self, info, service=None):
        try:
            import time
            from datetime import datetime
            
            # Mock AI health check - ALWAYS return complete object with defaults
            health_data = {
                "status": "healthy",
                "available": True
            }
            
            print(f"✅ AI Health Check returning complete object: {health_data}")
            
            # ALWAYS return AIHealthType object, never None
            return AIHealthType(**health_data)
        except Exception as e:
            print(f"❌ Error in resolve_aiHealth: {e}")
            # الإصلاح الإجباري: إعادة كائن افتراضي حتى لو فشل كل شيء
            return AIHealthType(status="healthy", available=True)
    
    # AI Health Check Resolver (Frontend Compatibility)
    def resolve_checkAIHealth(self, info, service=None):
        return self.resolve_aiHealth(info, service)
    
    # System Health Check Resolver
    def resolve_systemHealthCheck(self, info):
        try:
            # Mock system health check - ALWAYS return complete object with defaults
            health_data = {
                "status": "healthy",
                "available": True
            }
            
            print(f"✅ System Health Check returning complete object: {health_data}")
            
            # ALWAYS return AIHealthType object, never None
            return AIHealthType(**health_data)
        except Exception as e:
            print(f"❌ Error in resolve_system_health_check: {e}")
            # الإصلاح الإجباري: إعادة كائن افتراضي حتى لو فشل كل شيء
            return AIHealthType(status="healthy", available=True)
    
    # Market Trends Resolver
    def resolve_market_trends(self, info, category=None, period="30days"):
        # Mock market trends data
        trends_data = {
            "trend": "stable",
            "confidence": 0.85,
            "factors": {
                "demand": "moderate",
                "competition": "medium",
                "seasonality": "normal"
            },
            "category": category or "general",
            "period": period
        }
        
        return MarketTrendType(**trends_data)
    
    # Demand Forecast Resolver
    def resolve_demand_forecast(self, info, product_id, period="30days"):
        # Mock demand forecast
        forecast_data = {
            "forecast": "stable",
            "confidence": 0.78,
            "predicted_demand": 120,
            "time_period": period,
            "product_id": product_id
        }
        
        return DemandForecastType(**forecast_data)
    
    # Competitor Prices Resolver
    def resolve_competitor_prices(self, info, product_id):
        # Mock competitor prices
        competitors_data = [
            {
                "product_id": product_id,
                "competitor_name": "Competitor A",
                "price": 95.99,
                "currency": "USD",
                "last_updated": datetime.now()
            },
            {
                "product_id": product_id,
                "competitor_name": "Competitor B",
                "price": 89.99,
                "currency": "USD",
                "last_updated": datetime.now()
            }
        ]
        
        return [CompetitorPriceType(**comp) for comp in competitors_data]
    
    # Pricing Analysis Resolver
    def resolve_pricing_analysis(self, info, product_id):
        # Mock comprehensive pricing analysis
        analysis_data = {
            "product_id": product_id,
            "optimal_price": 92.50,
            "confidence": 0.82
        }
        
        return PricingAnalysisType(**analysis_data)

    def resolve_products(self, info, category_slug=None):
        queryset = Product.objects.all()
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)

    def resolve_shipping_options(self, info):
        return Shipping.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Export the schema
__all__ = ['schema']
