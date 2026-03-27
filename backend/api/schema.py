import uuid
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
from graphene import ObjectType, Field, Mutation

from .models import (
    Category, Order, OrderItem, Product, ProductVariant, Shipping,
    UserProfile, Material, ProductImage, Coupon, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine
)

User = get_user_model()

# --- Types ---

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name_ar", "name_en", "slug", "icon", "waste_percent")

class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = ("id", "name_en", "name_ar", "price_adjustment")

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
    variants = graphene.List(ProductVariantType)
    class Meta:
        model = Product
        fields = (
            "id", "name_ar", "name_en", "slug", "description_ar", "description_en",
            "base_price", "image", "on_sale", "discount_percent", "is_new",
            "created_at", "category", "variants", "sync_status", "erpnext_item_code",
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
        fields = ("id", "user", "session_id", "event_type", "metadata", "timestamp")

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

# --- Auth Responses ---

class LoginResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = Field(UserType)
    tokens = graphene.JSONString()
    errors = graphene.JSONString()

class RegisterResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = Field(UserType)
    tokens = graphene.JSONString()
    errors = graphene.JSONString()

class ProfileResponse(ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    user = Field(UserType)
    errors = graphene.JSONString()

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
    measurements = Field(Measurement)
    success = graphene.Boolean()
    error = graphene.String()

# --- Inputs ---

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

def generate_tokens(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginMutation(Mutation):
    class Arguments:
        email_or_username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    Output = LoginResponse
    
    def mutate(self, info, email_or_username, password):
        user = authenticate(username=email_or_username, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=email_or_username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if not user:
            return LoginResponse(success=False, message='بيانات الدخول غير صحيحة', errors={'credentials': 'بيانات الدخول غير صحيحة'})
        
        if not user.is_active:
            return LoginResponse(success=False, message='الحساب غير نشط', errors={'account': 'الحساب غير نشط'})
        
        tokens = generate_tokens(user)
        return LoginResponse(success=True, message='تم تسجيل الدخول بنجاح', user=user, tokens=tokens)

class RegisterMutation(Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirm = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String()
        phone = graphene.String()
    
    Output = RegisterResponse
    
    def mutate(self, info, username, email, password, password_confirm, first_name, last_name='', phone=''):
        if password != password_confirm:
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
            first_name=first_name, last_name=last_name
        )
        UserProfile.objects.create(user=user, phone=phone)
        
        tokens = generate_tokens(user)
        return RegisterResponse(success=True, message='تم إنشاء الحساب بنجاح', user=user, tokens=tokens)

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

class CreateOrderMutation(Mutation):
    class Arguments:
        customer_name = graphene.String(required=True)
        phone = graphene.String(required=True)
        email = graphene.String(required=True)
        address = graphene.String(required=True)
        wilaya_id = graphene.ID(required=True)
        subtotal = graphene.Float(required=True)
        shipping_cost = graphene.Float(required=True)
        total = graphene.Float(required=True)
        payment_method = graphene.String(required=True)
        items = graphene.List(OrderItemInput, required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, **kwargs):
        items_data = kwargs.pop('items')
        wilaya = Shipping.objects.get(pk=kwargs.pop('wilaya_id'))
        
        with transaction.atomic():
            order = Order.objects.create(
                user=info.context.user if info.context.user.is_authenticated else None,
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                wilaya=wilaya,
                **kwargs
            )
            for item in items_data:
                product = Product.objects.get(pk=item.pop('product_id'))
                OrderItem.objects.create(order=order, product=product, **item)
        
        return CreateOrderMutation(order=order)

class Mutation(ObjectType):
    login = LoginMutation.Field()
    register = RegisterMutation.Field()
    update_profile = UpdateProfileMutation.Field()
    chat_with_ai = ChatWithAIMutation.Field()
    create_order = CreateOrderMutation.Field()
    # Add other mutations as needed...

class Query(ObjectType):
    me = Field(UserType)
    categories = graphene.List(CategoryType)
    products = graphene.List(ProductType, category_slug=graphene.String())
    product = Field(ProductType, id=graphene.ID())
    shipping_options = graphene.List(ShippingType)
    
    def resolve_me(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_categories(self, info):
        return Category.objects.all()

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
