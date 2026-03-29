# Django Channels Routing Configuration
# WebSocket URL routing for real-time features

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # AI Chat WebSocket endpoint
    re_path(r'ws/ai/chat/$', consumers.AIChatConsumer.as_asgi()),
    
    # GraphQL Subscriptions endpoint
    re_path(r'ws/graphql/subscriptions/$', consumers.GraphQLSubscriptionConsumer.as_asgi()),
    
    # Order updates WebSocket endpoint
    re_path(r'ws/orders/(?P<order_id>\d+)/$', consumers.GraphQLSubscriptionConsumer.as_asgi()),
]

print("🔗 WebSocket routes configured for AI Chat and GraphQL Subscriptions")
