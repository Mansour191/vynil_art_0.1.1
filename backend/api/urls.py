from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, RegisterView, CustomTokenObtainPairView,
    CategoryViewSet, MaterialViewSet,
    ProductViewSet, ProductVariantViewSet, ShippingViewSet, OrderViewSet,
    PaymentViewSet, CartItemViewSet, WishlistViewSet, ReviewViewSet,
    ReviewReportViewSet, DesignCategoryViewSet, DesignViewSet,
    NotificationViewSet, AlertViewSet, ERPNextSyncLogViewSet,
    BehaviorTrackingViewSet, ForecastViewSet, CustomerSegmentViewSet,
    calculate_price, validate_coupon
)
from .ai_endpoints import measure_surface, chat_service, semantic_product_search

router = DefaultRouter()
# 1. Users
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'register', RegisterView, basename='register')

# 2. Products
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'variants', ProductVariantViewSet)

# 3. Orders
router.register(r'shipping', ShippingViewSet)
router.register(r'orders', OrderViewSet)
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

# 8. ERPNext
router.register(r'erpnext-logs', ERPNextSyncLogViewSet)

# 9. Analytics
router.register(r'tracking', BehaviorTrackingViewSet)
router.register(r'forecasts', ForecastViewSet)
router.register(r'segments', CustomerSegmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('calculate-price/', calculate_price, name='calculate-price'),
    path('validate-coupon/', validate_coupon, name='validate-coupon'),
    path('v1/measure/', measure_surface, name='measure-surface'),
    path('v1/chat/', chat_service, name='chat-service'),
    path('v1/semantic-search/', semantic_product_search, name='semantic-product-search'),
]
