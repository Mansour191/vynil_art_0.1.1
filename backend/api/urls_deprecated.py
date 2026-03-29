# DEPRECATED - MIGRATED TO GRAPHQL
# This file contains all Django REST Framework URLs that have been migrated to GraphQL.
# These URLs are no longer used in the application but are kept for reference.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from .views_deprecated import (
    UserViewSet, UserProfileViewSet, RegisterView, CustomTokenObtainPairView,
    CategoryViewSet, MaterialViewSet,
    ProductViewSet, ProductVariantViewSet, ShippingViewSet, OrderViewSet,
    PaymentViewSet, CartItemViewSet, WishlistViewSet, ReviewViewSet,
    ReviewReportViewSet, DesignCategoryViewSet, DesignViewSet,
    NotificationViewSet, AlertViewSet, ERPNextSyncLogViewSet,
    BehaviorTrackingViewSet, ForecastViewSet, CustomerSegmentViewSet,
    BlogCategoryViewSet, BlogPostViewSet,
    calculate_price, validate_coupon, ai_health, erpnext_health, pricing_competitors, pricing_batch_update,
    mock_ai_service, mock_erpnext_service
)

from .ai_endpoints import measure_surface, chat_service, semantic_product_search, chatbot_message, market_trends

# Create router for ViewSets
router = DefaultRouter()

# 1. Users
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

# 2. Products & Catalog
router.register(r'categories', CategoryViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-variants', ProductVariantViewSet)
router.register(r'shipping', ShippingViewSet)

# 3. Orders & Payments
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'payments', PaymentViewSet)

# 4. Cart & Wishlist
router.register(r'cart', CartItemViewSet)
router.register(r'wishlist', WishlistViewSet)

# 5. Reviews
router.register(r'reviews', ReviewViewSet)
router.register(r'review-reports', ReviewReportViewSet)

# 6. Designs
router.register(r'design-categories', DesignCategoryViewSet)
router.register(r'designs', DesignViewSet)

# 7. Notifications & Alerts
router.register(r'notifications', NotificationViewSet)
router.register(r'alerts', AlertViewSet)

# 8. AI & Analytics
router.register(r'erpnext-sync-logs', ERPNextSyncLogViewSet)
router.register(r'behavior-tracking', BehaviorTrackingViewSet)
router.register(r'forecasts', ForecastViewSet)
router.register(r'customer-segments', CustomerSegmentViewSet)

# 9. Blog
router.register(r'blog-categories', BlogCategoryViewSet)
router.register(r'blog-posts', BlogPostViewSet)

# API Endpoints
urlpatterns = [
    # Authentication
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    
    # ViewSet URLs
    path('', include(router.urls)),
    
    # Custom API Endpoints
    path('calculate-price/', calculate_price, name='calculate_price'),
    path('validate-coupon/', validate_coupon, name='validate_coupon'),
    path('ai/health/', ai_health, name='ai_health'),
    path('erpnext/health/', erpnext_health, name='erpnext_health'),
    path('pricing/competitors/', pricing_competitors, name='pricing_competitors'),
    path('pricing/batch-update/', pricing_batch_update, name='pricing_batch_update'),
    path('mock/ai-service/', mock_ai_service, name='mock_ai_service'),
    path('mock/erpnext-service/', mock_erpnext_service, name='mock_erpnext_service'),
    
    # AI Endpoints
    path('ai/measure-surface/', measure_surface, name='measure_surface'),
    path('ai/chat-service/', chat_service, name='chat_service'),
    path('ai/semantic-search/', semantic_product_search, name='semantic_product_search'),
    path('ai/chatbot/', chatbot_message, name='chatbot_message'),
    path('ai/market-trends/', market_trends, name='market_trends'),
]

print("⚠️  All REST API URLs have been migrated to GraphQL")
print("📁 Original URLs backed up in backup/rest_api/urls.py")
print("🔄 Use GraphQL endpoint: /graphql/")
print("🎮 GraphQL Playground: /graphql/playground/")
