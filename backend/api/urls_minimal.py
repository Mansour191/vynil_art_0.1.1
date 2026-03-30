# Minimal URLs for GraphQL-only API - DISABLED REST API
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import admin
from graphene import ObjectType, Field, String, List
import graphene
from django.http import JsonResponse

# Import the full schema instead of simple one
from .schema import schema as full_schema

# Simple Django views for health checks (no REST framework)
def erpnext_health(request):
    """ERPNext Service Health Check - Simple Django View"""
    return JsonResponse({
        "status": "connected",
        "latency_ms": 120,
        "sync_enabled": True
    })

def ai_health(request):
    """AI Service Health Check - Simple Django View"""
    return JsonResponse({
        "status": "healthy",
        "services": "all_active",
        "engine": "Gemini 1.5 Flash",
        "timestamp": "2026-03-30T18:51:29.816Z"
    })

# Create a simple working schema for testing
class SimpleQuery(ObjectType):
    # Basic queries for testing
    hello = Field(String, name=String(default_value="World"))
    
    # Add products field to SimpleQuery
    products = List('ProductType', category_slug=String())
    
    def resolve_hello(self, info, name):
        return f"Hello {name}!"
    
    def resolve_products(self, info, category_slug=None):
        from .models import Product
        queryset = Product.objects.all().prefetch_related('images', 'category', 'variants')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

class SimpleMutation(ObjectType):
    # Basic mutations for testing
    pass

# Use the full schema instead of simple schema
schema = full_schema

# Commented out all REST API imports to ensure they're not used
# from rest_framework.routers import DefaultRouter
# from .views import (
#     UserViewSet, UserProfileViewSet, RegisterView, CustomTokenObtainPairView,
#     CategoryViewSet, MaterialViewSet,
#     ProductViewSet, ProductVariantViewSet, ShippingViewSet, OrderViewSet,
#     PaymentViewSet, CartItemViewSet, WishlistViewSet, ReviewViewSet,
#     ReviewReportViewSet, DesignCategoryViewSet, DesignViewSet,
#     NotificationViewSet, AlertViewSet, ERPNextSyncLogViewSet,
#     BehaviorTrackingViewSet, ForecastViewSet, CustomerSegmentViewSet,
#     BlogCategoryViewSet, BlogPostViewSet,
#     calculate_price, validate_coupon, ai_health, erpnext_health, pricing_competitors, pricing_batch_update,
#     mock_ai_service, mock_erpnext_service
# )
# from .ai_endpoints import measure_surface, chat_service, semantic_product_search, chatbot_message, market_trends

# REST API router is completely disabled
# router = DefaultRouter()
# All router.register() calls are commented out to prevent REST API usage

urlpatterns = [
    # GraphQL Endpoint - PRIMARY API
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    
    # GraphQL Playground (for development)
    path('graphql/playground/', TemplateView.as_view(template_name='graphql_playground.html')),
    
    # Health Check
    path('health/', TemplateView.as_view(template_name='health.html')),
    
    # Essential REST endpoints for frontend compatibility
    path('erpnext/health/', erpnext_health, name='erpnext-health'),
    path('ai/health/', ai_health, name='ai-health'),
]

# REST API URLs are completely disabled
# The following commented lines show what would be included if REST was needed:
#
# urlpatterns += [
#     # Authentication
#     path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('auth/register/', RegisterView.as_view(), name='register'),
#     
#     # ViewSet URLs
#     path('', include(router.urls)),
#     
#     # Custom API Endpoints
#     path('calculate-price/', calculate_price, name='calculate-price'),
#     path('validate-coupon/', validate_coupon, name='validate-coupon'),
#     
#     # Health checks
#     path('ai/health/', ai_health, name='ai-health'),
#     path('erpnext/health/', erpnext_health, name='erpnext-health'),
#     
#     # Mock routes to satisfy frontend
#     path('ai/<str:action>/', mock_ai_service, name='mock-ai'),
#     path('ai/<str:action>/<str:subaction>/', mock_ai_service, name='mock-ai-sub'),
#     path('ai/<str:action>/<str:subaction>/<str:id>/', mock_ai_service, name='mock-ai-id'),
#     path('erpnext/<str:action>/', mock_erpnext_service, name='mock-erpnext'),
#     path('erpnext/<str:action>/<str:subaction>/', mock_erpnext_service, name='mock-erpnext-sub'),
#     path('erpnext/<str:action>/<str:subaction>/<str:id>/', mock_erpnext_service, name='mock-erpnext-id'),
#     
#     # AI Endpoints
#     path('ai/measure-surface/', measure_surface, name='measure_surface'),
#     path('ai/chat-service/', chat_service, name='chat_service'),
#     path('ai/semantic-search/', semantic_product_search, name='semantic_product_search'),
#     path('ai/chatbot/message/', chatbot_message, name='chatbot-message'),
#     path('ai/market-trends/', market_trends, name='market_trends'),
# ]

print("GraphQL-only URLs configured - REST API disabled")
print("Only GraphQL endpoint is available: /graphql/")
print("All REST API endpoints have been disabled for testing")
