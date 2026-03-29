"""
URL configuration for paclos_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.http import JsonResponse
from django.utils import timezone

# Use full schema instead of minimal schema
from api.schema import schema

# All REST API imports removed - using GraphQL only
# from api.views_simple import api_root

urlpatterns = [
    # GraphQL endpoint - PRIMARY API with simple schema
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG, schema=schema)), name='graphql'),
    
    # Admin interface (keep for Django admin)
    path('admin/', admin.site.urls),
    
    # Simple health check endpoint
    path('health/', lambda request: JsonResponse({'status': 'healthy', 'timestamp': timezone.now()}), name='health'),
    
    # Include minimal URLs (GraphQL only)
    path('api/', include('api.urls_minimal')),
]

# Static and media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print("🚀 Production URLs configured with GraphQL only")
print("⚠️  REST API completely removed - only GraphQL available")
print("📈 Using optimized schema with environment-based debug setting")
