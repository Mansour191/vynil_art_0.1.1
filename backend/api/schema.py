import uuid
from decimal import Decimal

import graphene
from django.db.models import Prefetch
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import (
    Category, Order, OrderItem, Product, ProductVariant, Shipping,
    UserProfile, Material, ProductImage, Coupon, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine
)

User = get_user_model()

# Basic Types - No dependencies
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

# User Types - No dependencies
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "is_staff")


class UserProfileType(DjangoObjectType):
    user = graphene.Field(UserType)
    
    class Meta:
        model = UserProfile
        fields = ("id", "user", "phone", "address", "avatar", "created_at")

# Product Types - Dependencies on Category, ProductVariant
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
            "id",
            "name_ar",
            "name_en",
            "slug",
            "description_ar",
            "description_en",
            "base_price",
            "image",
            "on_sale",
            "discount_percent",
            "is_new",
            "created_at",
            "category",
            "variants",
            "sync_status",
            "erpnext_item_code",
            "sync_error",
            "last_synced_at",
        )

# Order Types - Dependencies on User, Shipping, Product, Material
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "material",
            "width",
            "height",
            "dimension_unit",
            "marble_texture",
            "custom_design",
            "quantity",
            "price",
        )


class OrderType(DjangoObjectType):
    user = graphene.Field(UserType)
    wilaya = graphene.Field(ShippingType)
    items = graphene.List(OrderItemType)
    
    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "customer_name",
            "phone",
            "email",
            "address",
            "wilaya",
            "subtotal",
            "shipping_cost",
            "discount_amount",
            "total",
            "status",
            "sync_status",
            "erpnext_sales_order_id",
            "sync_error",
            "last_synced_at",
            "payment_method",
            "payment_status",
            "created_at",
            "updated_at",
            "user",
            "items",
        )

# Order Related Types
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

# Cart & Wishlist Types
class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "user", "product", "quantity", "options", "created_at")


class WishlistType(DjangoObjectType):
    class Meta:
        model = Wishlist
        fields = ("id", "user", "product", "created_at")

# Review Types
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("id", "product", "user", "rating", "comment", "created_at")


class ReviewReportType(DjangoObjectType):
    class Meta:
        model = ReviewReport
        fields = ("id", "review", "user", "reason", "created_at")

# Design Types
class DesignCategoryType(DjangoObjectType):
    class Meta:
        model = DesignCategory
        fields = ("id", "name_ar", "name_en", "slug")


class DesignType(DjangoObjectType):
    class Meta:
        model = Design
        fields = ("id", "category", "title_ar", "title_en", "image", "creator", "created_at")

# Notification Types
class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = ("id", "user", "title", "message", "is_read", "created_at")


class AlertType(DjangoObjectType):
    class Meta:
        model = Alert
        fields = ("id", "type", "message", "is_active", "created_at")

# System Types
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


class CurrentUserType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    is_staff = graphene.Boolean()


class RegisterError(graphene.ObjectType):
    message = graphene.String()
    field = graphene.String()


class RegisterResponse(graphene.ObjectType):
    success = graphene.Boolean()
    user = graphene.Field(UserType)
    errors = graphene.List(RegisterError)


class TokenAuthResponse(graphene.ObjectType):
    token = graphene.String()
    payload = graphene.String()
    user = graphene.Field(UserType)


class ChatResponse(graphene.ObjectType):
    response = graphene.String()
    success = graphene.Boolean()
    error = graphene.String()


class SemanticSearchResponse(graphene.ObjectType):
    products = graphene.List(ProductType)
    success = graphene.Boolean()
    error = graphene.String()

class Measurement(graphene.ObjectType):
    width = graphene.Float()
    height = graphene.Float()
    area = graphene.Float()
    estimated_cost = graphene.Float()

class MeasureResponse(graphene.ObjectType):
    measurements = graphene.Field(Measurement)
    success = graphene.Boolean()
    error = graphene.String()


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


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'date_joined')

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

class LoginMutation(Mutation):
    class Arguments:
        email_or_username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    Output = LoginResponse
    
    def mutate(self, info, email_or_username, password):
        try:
            # Try to authenticate with username first, then email
            user = None
            try:
                user = authenticate(username=email_or_username, password=password)
            except:
                pass
            
            if not user:
                try:
                    user_obj = User.objects.get(email=email_or_username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                return LoginResponse(
                    success=False,
                    message='بيانات الدخول غير صحيحة',
                    errors={'credentials': 'بيانات الدخول غير صحيحة'}
                )
            
            if not user.is_active:
                return LoginResponse(
                    success=False,
                    message='الحساب غير نشط',
                    errors={'account': 'الحساب غير نشط'}
                )
            
            tokens = generate_tokens(user)
            
            return LoginResponse(
                success=True,
                message='تم تسجيل الدخول بنجاح',
                user=user,
                tokens=tokens
            )
        except Exception as e:
            return LoginResponse(
                success=False,
                message=f'خطأ: {str(e)}',
                errors={'server': str(e)}
            )

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
        try:
            # Validate passwords match
            if password != password_confirm:
                return RegisterResponse(
                    success=False,
                    message='كلمات المرور غير متطابقة',
                    errors={'password': 'كلمات المرور غير متطابقة'}
                )
            
            # Validate password strength
            try:
                validate_password(password)
            except ValidationError as e:
                return RegisterResponse(
                    success=False,
                    message='كلمة المرور ضعيفة جداً',
                    errors={'password': list(e.messages)}
                )
            
            # Check if username exists
            if User.objects.filter(username=username).exists():
                return RegisterResponse(
                    success=False,
                    message='اسم المستخدم موجود بالفعل',
                    errors={'username': 'اسم المستخدم موجود بالفعل'}
                )
            
            # Check if email exists
            if User.objects.filter(email=email).exists():
                return RegisterResponse(
                    success=False,
                    message='البريد الإلكتروني موجود بالفعل',
                    errors={'email': 'البريد الإلكتروني موجود بالفعل'}
                )
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            
            tokens = generate_tokens(user)
            
            return RegisterResponse(
                success=True,
                message='تم إنشاء الحساب بنجاح',
                user=user,
                tokens=tokens
            )
        except Exception as e:
            return RegisterResponse(
                success=False,
                message=f'خطأ: {str(e)}',
                errors={'server': str(e)}
            )

class ChangePasswordMutation(Mutation):
    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        new_password_confirm = graphene.String(required=True)
    
    Output = ProfileResponse
    
    def mutate(self, info, old_password, new_password, new_password_confirm):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return ProfileResponse(
                    success=False,
                    message='يجب تسجيل الدخول أولاً',
                    errors={'auth': 'يجب تسجيل الدخول أولاً'}
                )
            
            # Validate passwords match
            if new_password != new_password_confirm:
                return ProfileResponse(
                    success=False,
                    message='كلمات المرور الجديدة غير متطابقة',
                    errors={'password': 'كلمات المرور الجديدة غير متطابقة'}
                )
            
            # Validate old password
            if not user.check_password(old_password):
                return ProfileResponse(
                    success=False,
                    message='كلمة المرور الحالية غير صحيحة',
                    errors={'old_password': 'كلمة المرور الحالية غير صحيحة'}
                )
            
            # Validate new password strength
            try:
                validate_password(new_password)
            except ValidationError as e:
                return ProfileResponse(
                    success=False,
                    message='كلمة المرور الجديدة ضعيفة جداً',
                    errors={'new_password': list(e.messages)}
                )
            
            # Update password
            user.set_password(new_password)
            user.save()
            
            return ProfileResponse(
                success=True,
                message='تم تغيير كلمة المرور بنجاح',
                user=user
            )
        except Exception as e:
            return ProfileResponse(
                success=False,
                message=f'خطأ: {str(e)}',
                errors={'server': str(e)}
            )

class UpdateProfileMutation(Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
    
    Output = ProfileResponse
    
    def mutate(self, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return ProfileResponse(
                    success=False,
                    message='يجب تسجيل الدخول أولاً',
                    errors={'auth': 'يجب تسجيل الدخول أولاً'}
                )
            
            # Update user fields
            for field, value in kwargs.items():
                if value is not None:
                    if field == 'email' and User.objects.exclude(id=user.id).filter(email=value).exists():
                        return ProfileResponse(
                            success=False,
                            message='البريد الإلكتروني موجود بالفعل',
                            errors={'email': 'البريد الإلكتروني موجود بالفعل'}
                        )
                    setattr(user, field, value)
            
            user.save()
            
            return ProfileResponse(
                success=True,
                message='تم تحديث الملف الشخصي بنجاح',
                user=user
            )
        except Exception as e:
            return ProfileResponse(
                success=False,
                message=f'خطأ: {str(e)}',
                errors={'server': str(e)}
            )

    @classmethod
    def mutate(cls, root, info, message):
        try:
            # Mock AI response - replace with actual AI service
            response = f"AI Response to: {message}"
            return ChatWithAI(
                chat_with_ai=ChatResponse(
                    response=response,
                    success=True
                )
            )
        except Exception as e:
            return ChatWithAI(
                chat_with_ai=ChatResponse(
                    success=False,
                    error=str(e)
                )
            )


class SemanticSearch(graphene.ObjectType):
    semantic_search = graphene.Field(SemanticSearchResponse, query=graphene.String(required=True), options=graphene.JSONString())
    
    def resolve_semantic_search(self, info, query, options=None):
        try:
            # Mock semantic search - replace with actual search service
            products = Product.objects.filter(
                name_ar__icontains=query
            )[:10]
            
            return SemanticSearchResponse(
                products=products,
                success=True
            )
        except Exception as e:
            return SemanticSearchResponse(
                success=False,
                error=str(e)
            )


class MeasureSurface(graphene.Mutation):
    class Arguments:
        image_file = graphene.String(required=True)
        reference_dimension_cm = graphene.Float(required=True)
        price_per_m2 = graphene.Float()

    measure_surface = graphene.Field(MeasureResponse)

    @classmethod
    def mutate(cls, root, info, image_file, reference_dimension_cm, price_per_m2=0):
        try:
            # Mock measurement - replace with actual AI measurement service
            measurements = Measurement(
                width=100.0,
                height=100.0,
                area=10000.0,
                estimated_cost=reference_dimension_cm * price_per_m2
            )
            
            return MeasureSurface(
                measure_surface=MeasureResponse(
                    measurements=measurements,
                    success=True
                )
            )
        except Exception as e:
            return MeasureSurface(
                measure_surface=MeasureResponse(
                    success=False,
                    error=str(e)
                )
            )


class CreateOrder(graphene.Mutation):
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

    @classmethod
    def mutate(
        cls,
        root,
        info,
        customer_name,
        phone,
        email,
        address,
        wilaya_id,
        subtotal,
        shipping_cost,
        total,
        payment_method,
        items,
    ):
        if not items:
            raise GraphQLError("Order must include at least one item.")

        wilaya = Shipping.objects.filter(pk=wilaya_id).first()
        if wilaya is None:
            raise GraphQLError("Invalid wilaya.")

        with transaction.atomic():
            order = Order.objects.create(
                user=info.context.user if info.context.user.is_authenticated else None,
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                customer_name=customer_name,
                phone=phone,
                email=email,
                address=address,
                wilaya=wilaya,
                subtotal=Decimal(str(subtotal)),
                shipping_cost=Decimal(str(shipping_cost)),
                total=Decimal(str(total)),
                payment_method=payment_method,
            )

            for item in items:
                product = Product.objects.filter(pk=item.product_id).first()
                if not product:
                    raise GraphQLError(f"Invalid product_id: {item.product_id}")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    material_id=item.material_id,
                    width=Decimal(str(item.width)),
                    height=Decimal(str(item.height)),
                    dimension_unit=item.dimension_unit or "cm",
                    marble_texture=item.marble_texture or "",
                    custom_design=item.custom_design or "",
                    quantity=item.quantity,
                    price=Decimal(str(item.price)),
                )

        return CreateOrder(order=order)


class UpsertProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name_ar = graphene.String(required=True)
        name_en = graphene.String(required=True)
        slug = graphene.String(required=True)
        category_id = graphene.ID(required=True)
        description_ar = graphene.String()
        description_en = graphene.String()
        base_price = graphene.Float(required=True)
        on_sale = graphene.Boolean()
        discount_percent = graphene.Int()
        is_new = graphene.Boolean()

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        _require_admin(info)
        product_id = kwargs.pop("id", None)
        category_id = kwargs.pop("category_id")

        category = Category.objects.filter(pk=category_id).first()
        if not category:
            raise GraphQLError("Invalid category_id.")

        payload = {
            "name_ar": kwargs["name_ar"],
            "name_en": kwargs["name_en"],
            "slug": kwargs["slug"],
            "category": category,
            "description_ar": kwargs.get("description_ar", ""),
            "description_en": kwargs.get("description_en", ""),
            "base_price": Decimal(str(kwargs["base_price"])),
            "on_sale": kwargs.get("on_sale", False),
            "discount_percent": kwargs.get("discount_percent", 0),
            "is_new": kwargs.get("is_new", True),
        }

        if product_id:
            product = Product.objects.filter(pk=product_id).first()
            if not product:
                raise GraphQLError("Product not found.")
            for key, value in payload.items():
                setattr(product, key, value)
            product.save()
        else:
            if not info.context.FILES.get("image"):
                raise GraphQLError("Image is required when creating a new product.")
            product = Product.objects.create(image=info.context.FILES["image"], **payload)

        return UpsertProduct(product=product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        _require_admin(info)
        product = Product.objects.filter(pk=id).first()
        if not product:
            raise GraphQLError("Product not found.")
        product.delete()
        return DeleteProduct(ok=True)


class Query(graphene.ObjectType):
    me = graphene.Field(CurrentUserType)
    my_profile = graphene.Field(UserProfileType)
    categories = graphene.List(CategoryType)
    materials = graphene.List(MaterialType)
    products = graphene.List(ProductType, category_slug=graphene.String())
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    product_by_slug = graphene.Field(ProductType, slug=graphene.String(required=True))
    orders = graphene.List(OrderType, phone=graphene.String())
    my_orders = graphene.List(OrderType)
    cart_items = graphene.List(CartItemType)
    wishlist = graphene.List(WishlistType)
    reviews = graphene.List(ReviewType, product_id=graphene.ID())
    designs = graphene.List(DesignType, category_slug=graphene.String())
    design_categories = graphene.List(DesignCategoryType)
    notifications = graphene.List(NotificationType)
    alerts = graphene.List(AlertType)
    # AI Services
    semantic_search = graphene.Field(SemanticSearchResponse, query=graphene.String(required=True), options=graphene.JSONString())
    # Analytics
    forecasts = graphene.List(ForecastType, target_metric=graphene.String())
    customer_segments = graphene.List(CustomerSegmentType)
    # System
    pricing_engine = graphene.Field(PricingEngineType)
    sync_logs = graphene.List(ERPNextSyncLogType)

    def resolve_me(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return CurrentUserType(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_staff=user.is_staff,
        )
    
    def resolve_my_profile(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return user.profile
    
    def resolve_materials(self, info):
        return Material.objects.all()
    
    def resolve_my_orders(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(user=user).order_by('-created_at')
    
    def resolve_cart_items(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return CartItem.objects.none()
        return CartItem.objects.filter(user=user)
    
    def resolve_wishlist(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return Wishlist.objects.none()
        return Wishlist.objects.filter(user=user)
    
    def resolve_reviews(self, info, product_id=None):
        queryset = Review.objects.select_related('user', 'product').order_by('-created_at')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    def resolve_designs(self, info, category_slug=None):
        queryset = Design.objects.select_related('category', 'creator').order_by('-created_at')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def resolve_design_categories(self, info):
        return DesignCategory.objects.all()
    
    def resolve_notifications(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(user=user).order_by('-created_at')
    
    def resolve_alerts(self, info):
        return Alert.objects.filter(is_active=True).order_by('-created_at')
    
    def resolve_forecasts(self, info, target_metric=None):
        queryset = Forecast.objects.order_by('-forecast_date')
        if target_metric:
            queryset = queryset.filter(target_metric=target_metric)
        return queryset
    
    def resolve_customer_segments(self, info):
        return CustomerSegment.objects.prefetch_related('users').all()
    
    def resolve_pricing_engine(self, info):
        return PricingEngine.objects.first()
    
    def resolve_sync_logs(self, info):
        user = info.context.user
        if not user.is_authenticated or not user.is_staff:
            return ERPNextSyncLog.objects.none()
        return ERPNextSyncLog.objects.order_by('-timestamp')

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_products(self, info, category_slug=None):
        queryset = Product.objects.select_related("category").prefetch_related(
            Prefetch("variants", queryset=ProductVariant.objects.all())
        )
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def resolve_product(self, info, id):
        return Product.objects.select_related("category").filter(pk=id).first()

    def resolve_product_by_slug(self, info, slug):
        return Product.objects.select_related("category").filter(slug=slug).first()

    def resolve_orders(self, info, phone=None):
        user = info.context.user
        queryset = Order.objects.select_related("wilaya").prefetch_related("items").order_by("-created_at")
        if user.is_authenticated and user.is_staff:
            return queryset
        if phone:
            return queryset.filter(phone=phone)
        if user.is_authenticated:
            return queryset.filter(user=user)
        return Order.objects.none()

    def resolve_semantic_search(self, info, query, options=None):
        try:
            # Mock semantic search - replace with actual search service
            products = Product.objects.filter(
                name_ar__icontains=query
            )[:10]
            
            return SemanticSearchResponse(
                products=products,
                success=True
            )
        except Exception as e:
            return SemanticSearchResponse(
                success=False,
                error=str(e)
            )


class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        options = graphene.JSONString()

    success = graphene.Boolean()
    cart_item = graphene.Field(CartItemType)
    error = graphene.String()

    def mutate(self, info, product_id, quantity, options=None):
        user = info.context.user
        if not user.is_authenticated:
            return AddToCart(success=False, error="Authentication required")
        
        try:
            product = Product.objects.get(pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product,
                defaults={'quantity': quantity, 'options': options or {}}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return AddToCart(success=True, cart_item=cart_item)
        except Product.DoesNotExist:
            return AddToCart(success=False, error="Product not found")
        except Exception as e:
            return AddToCart(success=False, error=str(e))


class RemoveFromCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, product_id):
        user = info.context.user
        if not user.is_authenticated:
            return RemoveFromCart(success=False, error="Authentication required")
        
        try:
            cart_item = CartItem.objects.get(user=user, product_id=product_id)
            cart_item.delete()
            return RemoveFromCart(success=True)
        except CartItem.DoesNotExist:
            return RemoveFromCart(success=False, error="Cart item not found")
        except Exception as e:
            return RemoveFromCart(success=False, error=str(e))


class AddToWishlist(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    success = graphene.Boolean()
    wishlist_item = graphene.Field(WishlistType)
    error = graphene.String()

    def mutate(self, info, product_id):
        user = info.context.user
        if not user.is_authenticated:
            return AddToWishlist(success=False, error="Authentication required")
        
        try:
            product = Product.objects.get(pk=product_id)
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=user,
                product=product
            )
            
            return AddToWishlist(success=True, wishlist_item=wishlist_item)
        except Product.DoesNotExist:
            return AddToWishlist(success=False, error="Product not found")
        except Exception as e:
            return AddToWishlist(success=False, error=str(e))


class RemoveFromWishlist(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, product_id):
        user = info.context.user
        if not user.is_authenticated:
            return RemoveFromWishlist(success=False, error="Authentication required")
        
        try:
            wishlist_item = Wishlist.objects.get(user=user, product_id=product_id)
            wishlist_item.delete()
            return RemoveFromWishlist(success=True)
        except Wishlist.DoesNotExist:
            return RemoveFromWishlist(success=False, error="Wishlist item not found")
        except Exception as e:
            return RemoveFromWishlist(success=False, error=str(e))


class CreateReview(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        comment = graphene.String()

    success = graphene.Boolean()
    review = graphene.Field(ReviewType)
    error = graphene.String()

    def mutate(self, info, product_id, rating, comment=None):
        user = info.context.user
        if not user.is_authenticated:
            return CreateReview(success=False, error="Authentication required")
        
        try:
            product = Product.objects.get(pk=product_id)
            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment
            )
            
            return CreateReview(success=True, review=review)
        except Product.DoesNotExist:
            return CreateReview(success=False, error="Product not found")
        except Exception as e:
            return CreateReview(success=False, error=str(e))


class ReportReview(graphene.Mutation):
    class Arguments:
        review_id = graphene.ID(required=True)
        reason = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, review_id, reason):
        user = info.context.user
        if not user.is_authenticated:
            return ReportReview(success=False, error="Authentication required")
        
        try:
            review = Review.objects.get(pk=review_id)
            ReviewReport.objects.create(
                user=user,
                review=review,
                reason=reason
            )
            
            return ReportReview(success=True)
        except Review.DoesNotExist:
            return ReportReview(success=False, error="Review not found")
        except Exception as e:
            return ReportReview(success=False, error=str(e))


class MarkNotificationRead(graphene.Mutation):
    class Arguments:
        notification_id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, notification_id):
        user = info.context.user
        if not user.is_authenticated:
            return MarkNotificationRead(success=False, error="Authentication required")
        
        try:
            notification = Notification.objects.get(pk=notification_id, user=user)
            notification.is_read = True
            notification.save()
            
            return MarkNotificationRead(success=True)
        except Notification.DoesNotExist:
            return MarkNotificationRead(success=False, error="Notification not found")
        except Exception as e:
            return MarkNotificationRead(success=False, error=str(e))


class Mutation(graphene.ObjectType):
    # Auth
    token_auth = TokenAuth.Field()
    register = Register.Field()
    # Cart & Wishlist
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()
    add_to_wishlist = AddToWishlist.Field()
    remove_from_wishlist = RemoveFromWishlist.Field()
    # Reviews
    create_review = CreateReview.Field()
    report_review = ReportReview.Field()
    # Products
    create_order = CreateOrder.Field()
    upsert_product = UpsertProduct.Field()
    delete_product = DeleteProduct.Field()
    # Notifications
    mark_notification_read = MarkNotificationRead.Field()
    # AI Services
    chat_with_ai = ChatWithAI.Field()
    measure_surface = MeasureSurface.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
