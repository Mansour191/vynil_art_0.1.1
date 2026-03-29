"""
GraphQL-only URL configuration for API app.
This file replaces the DRF-based urls.py to remove rest_framework dependency.
"""

from django.urls import path
from .views_simple import (
    # Simple function-based views for essential endpoints
    ai_health, 
    erpnext_health,
    calculate_price,
    validate_coupon,
    pricing_competitors,
    pricing_batch_update,
    mock_ai_service,
    mock_erpnext_service,
    api_root
)
from .ai_endpoints_simple import (
    measure_surface, 
    chat_service, 
    semantic_product_search, 
    chatbot_message, 
    market_trends
)
from .views_blog import (
    blog_posts_list,
    blog_post_detail
)
from .views_products import (
    products_list,
    product_detail,
    categories_list
)

# Simple URL patterns without DRF router
urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),
    
    # Health checks
    path('ai/health/', ai_health, name='ai-health'),
    path('erpnext/health/', erpnext_health, name='erpnext-health'),
    
    # Blog endpoints
    path('blog/posts/', blog_posts_list, name='blog-posts-list'),
    path('blog/posts/<slug:slug>/', blog_post_detail, name='blog-post-detail'),
    
    # Products endpoints
    path('products/', products_list, name='products-list'),
    path('products/test/', products_list, name='products-test'),  # Add test endpoint
    path('products/<int:product_id>/', product_detail, name='product-detail'),
    path('categories/', categories_list, name='categories-list'),
    
    # Pricing endpoints
    path('calculate-price/', calculate_price, name='calculate-price'),
    path('validate-coupon/', validate_coupon, name='validate-coupon'),
    path('pricing/competitors/<slug:slug>/', pricing_competitors, name='pricing-competitors'),
    path('pricing/batch-update/', pricing_batch_update, name='pricing-batch-update'),
    
    # Mock routes to satisfy frontend
    path('ai/<str:action>/', mock_ai_service, name='mock-ai'),
    path('ai/<str:action>/<str:subaction>/', mock_ai_service, name='mock-ai-sub'),
    path('ai/<str:action>/<str:subaction>/<str:id>/', mock_ai_service, name='mock-ai-id'),
    path('erpnext/<str:action>/', mock_erpnext_service, name='mock-erpnext'),
    path('erpnext/<str:action>/<str:subaction>/', mock_erpnext_service, name='mock-erpnext-sub'),
    path('erpnext/<str:action>/<str:subaction>/<str:id>/', mock_erpnext_service, name='mock-erpnext-id'),
    
    # AI Chatbot endpoints
    path('ai/chatbot/message/', chatbot_message, name='chatbot-message'),
    path('ai/analytics/market-trends/', market_trends, name='market-trends'),
    path('v1/measure/', measure_surface, name='measure-surface'),
    path('v1/chat/', chat_service, name='chat-service'),
    path('v1/semantic-search/', semantic_product_search, name='semantic-product-search'),
]
