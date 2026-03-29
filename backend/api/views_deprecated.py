# DEPRECATED - MIGRATED TO GRAPHQL
# This file contains all Django REST Framework views that have been migrated to GraphQL.
# These views are no longer used in the application but are kept for reference.

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    UserProfile, Category, Material, Product, ProductVariant, Shipping,
    Order, OrderItem, Payment, CartItem, Wishlist, Review, ReviewReport,
    DesignCategory, Design, Notification, Alert, ERPNextSyncLog,
    BehaviorTracking, Forecast, CustomerSegment, BlogCategory, BlogPost
)

from .serializers_deprecated import (
    UserSerializer, UserProfileSerializer, RegisterSerializer, CustomTokenObtainPairSerializer,
    CategorySerializer, MaterialSerializer, ProductSerializer, ProductVariantSerializer,
    ShippingSerializer, OrderItemSerializer, OrderSerializer, PaymentSerializer,
    CartItemSerializer, WishlistSerializer, ReviewSerializer, ReviewReportSerializer,
    DesignCategorySerializer, DesignSerializer, NotificationSerializer, AlertSerializer,
    ERPNextSyncLogSerializer, BehaviorTrackingSerializer, ForecastSerializer,
    CustomerSegmentSerializer, BlogCategorySerializer, BlogPostSerializer
)

User = get_user_model()

# Authentication Views (DEPRECATED - Use GraphQL mutations instead)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_fields = ['is_staff', 'is_active']
    ordering_fields = ['date_joined', 'username', 'email']

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

# Product ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name_ar', 'name_en']
    filterset_fields = ['is_active']
    ordering_fields = ['name_ar', 'name_en', 'created_at']

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name_ar', 'name_en']
    filterset_fields = ['is_premium']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en']
    filterset_fields = ['category', 'on_sale', 'is_new', 'is_active']
    ordering_fields = ['name_ar', 'name_en', 'base_price', 'created_at']

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

# Order ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['order_number', 'user__username', 'user__email']
    filterset_fields = ['status', 'payment_status', 'payment_method']
    ordering_fields = ['created_at', 'total_amount']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product', 'material']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['transaction_id', 'order__order_number']
    filterset_fields = ['status', 'method']
    ordering_fields = ['created_at', 'amount']

# Cart and Wishlist ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'product', 'material']

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'product']

# Review ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['comment', 'user__username']
    filterset_fields = ['product', 'rating', 'is_verified']
    ordering_fields = ['created_at', 'rating']

class ReviewReportViewSet(viewsets.ModelViewSet):
    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review', 'user']

# Design ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class DesignCategoryViewSet(viewsets.ModelViewSet):
    queryset = DesignCategory.objects.all()
    serializer_class = DesignCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name_ar', 'name_en']
    filterset_fields = ['is_active']

class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'tags']
    filterset_fields = ['category', 'is_featured', 'is_active']
    ordering_fields = ['created_at', 'likes', 'downloads']

# Notification and Alert ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'message']
    filterset_fields = ['user', 'type', 'is_read']
    ordering_fields = ['created_at']

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['message']
    filterset_fields = ['user', 'type', 'is_active']

# AI and Analytics ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class ERPNextSyncLogViewSet(viewsets.ModelViewSet):
    queryset = ERPNextSyncLog.objects.all()
    serializer_class = ERPNextSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['sync_type', 'error_message']
    filterset_fields = ['status', 'sync_type']
    ordering_fields = ['sync_time']

class BehaviorTrackingViewSet(viewsets.ModelViewSet):
    queryset = BehaviorTracking.objects.all()
    serializer_class = BehaviorTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['action', 'target_type']
    filterset_fields = ['user', 'action', 'target_type']
    ordering_fields = ['created_at']

class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['forecast_type']
    filterset_fields = ['product', 'forecast_type', 'period']
    ordering_fields = ['created_at']

class CustomerSegmentViewSet(viewsets.ModelViewSet):
    queryset = CustomerSegment.objects.all()
    serializer_class = CustomerSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['customer_count', 'name']

# Blog ViewSets (DEPRECATED - Use GraphQL queries/mutations instead)
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name_ar', 'name_en']

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title_ar', 'title_en', 'content_ar', 'content_en']
    filterset_fields = ['category', 'is_published']
    ordering_fields = ['published_at', 'created_at']

# API Views (DEPRECATED - Use GraphQL queries/mutations instead)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def calculate_price(request):
    """Calculate price based on dimensions and materials"""
    try:
        # This logic is now handled in GraphQL mutations
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL mutations instead.',
            'graphql_mutation': 'calculatePrice'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def validate_coupon(request):
    """Validate coupon code"""
    try:
        # This logic is now handled in GraphQL queries
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL queries instead.',
            'graphql_query': 'validateCoupon'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def ai_health(request):
    """AI service health check"""
    try:
        # This logic is now handled in GraphQL queries
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL queries instead.',
            'graphql_query': 'aiHealth'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def erpnext_health(request):
    """ERPNext service health check"""
    try:
        # This logic is now handled in GraphQL queries
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL queries instead.',
            'graphql_query': 'erpnextHealth'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def pricing_competitors(request):
    """Get competitor pricing"""
    try:
        # This logic is now handled in GraphQL queries
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL queries instead.',
            'graphql_query': 'competitorPrices'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def pricing_batch_update(request):
    """Batch update pricing"""
    try:
        # This logic is now handled in GraphQL mutations
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL mutations instead.',
            'graphql_mutation': 'bulkUpdateProducts'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def mock_ai_service(request):
    """Mock AI service endpoint"""
    try:
        # This logic is now handled in GraphQL mutations
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL mutations instead.',
            'graphql_mutation': 'chatWithAi'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def mock_erpnext_service(request):
    """Mock ERPNext service endpoint"""
    try:
        # This logic is now handled in GraphQL mutations
        return Response({
            'message': 'This endpoint is deprecated. Use GraphQL mutations instead.',
            'graphql_mutation': 'syncWithERPNext'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

print("⚠️  All views have been migrated to GraphQL")
print("📁 Original views backed up in backup/rest_api/views.py")
print("🔄 Use GraphQL mutations and queries instead")
