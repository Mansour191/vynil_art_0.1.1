from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Material, Product, ProductImage, ProductVariant,
    Shipping, Coupon, Order, OrderItem, OrderTimeline, Payment,
    CartItem, Wishlist, Review, ReviewReport, DesignCategory, Design,
    Notification, Alert, ERPNextSyncLog, BehaviorTracking, Forecast,
    CustomerSegment, PricingEngine
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, 
    UserProfileSerializer, CategorySerializer, MaterialSerializer,
    ProductSerializer, ProductVariantSerializer, ShippingSerializer, CouponSerializer,
    OrderSerializer, PaymentSerializer, CartItemSerializer, WishlistSerializer,
    ReviewSerializer, ReviewReportSerializer, DesignCategorySerializer, DesignSerializer,
    NotificationSerializer, AlertSerializer, ERPNextSyncLogSerializer,
    BehaviorTrackingSerializer, ForecastSerializer, CustomerSegmentSerializer,
    PricingEngineSerializer
)
from decimal import Decimal

# 1. Users & Auth
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

# 2. Products
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related('images', 'category', 'variants')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]

# 3. Orders
class ShippingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items', 'timeline', 'payment')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='by-phone/(?P<phone>[^/.]+)')
    def by_phone(self, request, phone=None):
        orders = self.get_queryset().filter(phone=phone).order_by('-created_at')
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

# 4. Cart & Wishlist
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# 5. Reviews
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

class ReviewReportViewSet(viewsets.ModelViewSet):
    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]

# 6. Designs
class DesignCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DesignCategory.objects.all()
    serializer_class = DesignCategorySerializer
    permission_classes = [AllowAny]

class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer
    permission_classes = [AllowAny]

# 7. Notifications & Alerts
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.filter(is_active=True)
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]

# 8. ERPNext Integration
class ERPNextSyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ERPNextSyncLog.objects.all().order_by('-timestamp')
    serializer_class = ERPNextSyncLogSerializer
    permission_classes = [IsAuthenticated]

# 9. Analytics & AI
class BehaviorTrackingViewSet(viewsets.ModelViewSet):
    queryset = BehaviorTracking.objects.all()
    serializer_class = BehaviorTrackingSerializer
    permission_classes = [AllowAny]

class ForecastViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

class CustomerSegmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerSegment.objects.all()
    serializer_class = CustomerSegmentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_price(request):
    try:
        width = Decimal(str(request.data.get('width', 0)))
        height = Decimal(str(request.data.get('height', 0)))
        category_slug = request.data.get('category_slug')
        product_id = request.data.get('product_id')
        material_id = request.data.get('material_id')
        quantity = int(request.data.get('quantity', 1))
        
        area = (width / Decimal('100')) * (height / Decimal('100'))
        
        try:
            category = Category.objects.get(slug=category_slug)
            waste_percent = category.waste_percent
        except Category.DoesNotExist:
            waste_percent = Decimal('10')

        pricing = PricingEngine.objects.first()
        if not pricing:
            pricing = PricingEngine.objects.create(raw_material_cost=Decimal('500'), labor_cost=Decimal('300'), international_shipping=Decimal('200'))

        waste_factor = Decimal('1') + (waste_percent / Decimal('100'))
        area_with_waste = area * waste_factor
        
        product_price = Decimal('0')
        if product_id:
            try:
                product_price = Product.objects.get(id=product_id).base_price
            except Product.DoesNotExist: pass

        material_price = Decimal('0')
        if material_id:
            try:
                material_price = Material.objects.get(id=material_id).price_per_m2
            except Material.DoesNotExist: pass

        cost_per_m2 = pricing.raw_material_cost + pricing.international_shipping + product_price + material_price
        total_price = (area_with_waste * cost_per_m2 * quantity) + pricing.labor_cost
        
        return Response({
            'area_m2': round(area, 2),
            'waste_percent': waste_percent,
            'total_price': round(total_price, 2),
            'currency': 'DZD'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_coupon(request):
    code = request.data.get('code')
    try:
        from django.utils import timezone
        coupon = Coupon.objects.get(code=code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        return Response({'valid': True, 'discount_percent': coupon.discount_percent})
    except Coupon.DoesNotExist:
        return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

@csrf_exempt
@require_http_methods(["GET"])
def api_root(request):
    """API Root - GraphQL Only"""
    return JsonResponse({
        "message": "Paclos Full Architect API - GraphQL Only",
        "status": "Running",
        "version": "3.0.0",
        "graphql_endpoint": "/graphql/",
        "graphiql_ui": "/graphql/" if settings.DEBUG else "Disabled",
        "available_queries": [
            "me", "my_profile", "categories", "materials", "products",
            "orders", "my_orders", "cart_items", "wishlist", "reviews",
            "designs", "design_categories", "notifications", "alerts",
            "semantic_search", "forecasts", "customer_segments",
            "pricing_engine", "sync_logs"
        ],
        "available_mutations": [
            "token_auth", "register", "add_to_cart", "remove_from_cart",
            "add_to_wishlist", "remove_from_wishlist", "create_review",
            "report_review", "create_order", "upsert_product",
            "delete_product", "mark_notification_read", "chat_with_ai",
            "measure_surface"
        ]
    })
