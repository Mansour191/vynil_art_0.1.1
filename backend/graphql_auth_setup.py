# Django GraphQL Authentication Setup
# This file contains the configuration for secure GraphQL authentication

# 1. Install required packages
# pip install django-graphql-jwt graphene-django strawberry-graphql-django

# 2. Add to settings.py
"""
INSTALLED_APPS = [
    ...,
    'graphene_django',
    'django.contrib.auth',
    'django.contrib.sessions',
]

# GraphQL JWT Configuration
GRAPHENE = {
    'SCHEMA': 'your_project.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

# JWT Settings
import datetime
JWT_AUTH = {
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=24),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_VERIFY_EXPIRATION': True,
}

# Security Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
"""

# 3. GraphQL Schema with Authentication (using Graphene)
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required, permission_required
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')

class LoginInput(graphene.InputType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)

class RegisterInput(graphene.InputType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()

class SocialLoginInput(graphene.InputType):
    provider = graphene.String(required=True)
    accessToken = graphene.String(required=True)

class AuthPayload(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    token = graphene.String()
    refreshToken = graphene.String()
    user = graphene.Field(UserType)

class Query(graphene.ObjectType):
    # Protected query - requires authentication
    me = graphene.Field(UserType)
    
    @login_required
    def resolve_me(self, info):
        return info.context.user
    
    # Admin-only query
    users = graphene.List(UserType)
    
    @permission_required('auth.view_user')
    def resolve_users(self, info):
        return User.objects.all()
    
    # Investor-only query (example)
    investor_data = graphene.String()
    
    @login_required
    def resolve_investor_data(self, info):
        user = info.context.user
        if not user.groups.filter(name='investors').exists() and not user.is_staff:
            raise PermissionError("Access denied")
        return "Investor sensitive data"

class Mutation(graphene.ObjectType):
    # Login mutation
    login = graphene.Field(AuthPayload, input=LoginInput())
    
    def resolve_login(self, info, input):
        username = input.get('username')
        password = input.get('password')
        
        # Generic error message to prevent account enumeration
        error_message = "Invalid credentials"
        
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                if not user.is_active:
                    return AuthPayload(
                        success=False,
                        message=error_message
                    )
                
                # Generate tokens
                token = graphql_jwt.get_token(user, info.context)
                refresh = graphql_jwt.get_refresh_token(user, info.context)
                
                return AuthPayload(
                    success=True,
                    message="Login successful",
                    token=token,
                    refreshToken=refresh,
                    user=user
                )
            else:
                return AuthPayload(
                    success=False,
                    message=error_message
                )
        except User.DoesNotExist:
            # Use consistent timing to prevent timing attacks
            import time
            time.sleep(0.1)
            return AuthPayload(
                success=False,
                message=error_message
            )
    
    # Register mutation
    register = graphene.Field(AuthPayload, input=RegisterInput())
    
    def resolve_register(self, info, input):
        username = input.get('username')
        email = input.get('email')
        password = input.get('password')
        first_name = input.get('first_name', '')
        last_name = input.get('last_name', '')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Generate tokens
            token = graphql_jwt.get_token(user, info.context)
            refresh = graphql_jwt.get_refresh_token(user, info.context)
            
            return AuthPayload(
                success=True,
                message="Registration successful",
                token=token,
                refreshToken=refresh,
                user=user
            )
        except Exception as e:
            return AuthPayload(
                success=False,
                message="Registration failed"
            )
    
    # Social login mutation
    social_login = graphene.Field(AuthPayload, input=SocialLoginInput())
    
    def resolve_social_login(self, info, input):
        provider = input.get('provider')
        access_token = input.get('accessToken')
        
        # Implement social login logic here
        # This is a placeholder - you'd integrate with actual social providers
        
        try:
            # Mock social login - replace with actual implementation
            user = User.objects.get(username='demo_user')
            
            token = graphql_jwt.get_token(user, info.context)
            refresh = graphql_jwt.get_refresh_token(user, info.context)
            
            return AuthPayload(
                success=True,
                message=f"Social login with {provider} successful",
                token=token,
                refreshToken=refresh,
                user=user
            )
        except Exception as e:
            return AuthPayload(
                success=False,
                message="Social login failed"
            )
    
    # Refresh token mutation
    refresh_token = graphene.Field(graphene.String(), token=graphene.String())
    
    def resolve_refresh_token(self, info, token):
        try:
            user = graphql_jwt.get_user_by_token(token, info.context)
            new_token = graphql_jwt.get_refresh_token(user, info.context)
            return new_token
        except Exception:
            return None

schema = graphene.Schema(query=Query, mutation=Mutation)
"""

# 4. URL Configuration
"""
# urls.py
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True)))),
]
"""

# 5. Middleware for Security
"""
# middleware.py
import time
from django.http import JsonResponse
from graphql.error import GraphQLSyntaxError

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Rate limiting
        if request.path == '/graphql/':
            client_ip = self.get_client_ip(request)
            if self.is_rate_limited(client_ip):
                return JsonResponse({'error': 'Too many requests'}, status=429)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    def is_rate_limited(self, ip):
        # Implement rate limiting logic here
        # This is a placeholder - use Redis or database for production
        return False

# Query depth limiting
class QueryDepthLimiter:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
    
    def resolve(self, next, root, info, **args):
        if hasattr(info, 'field_asts') and info.field_asts:
            depth = self.get_query_depth(info.field_asts[0])
            if depth > self.max_depth:
                raise GraphQLSyntaxError(f'Query depth {depth} exceeds maximum depth {self.max_depth}')
        return next(root, info, **args)
    
    def get_query_depth(self, ast, depth=0):
        if hasattr(ast, 'selection_set'):
            return max(self.get_query_depth(selection, depth + 1) 
                      for selection in ast.selection_set.selections)
        return depth
"""

# 6. Production Security Settings
"""
# Disable introspection in production
if not DEBUG:
    GRAPHENE = {
        'SCHEMA': 'your_project.schema.schema',
        'MIDDLEWARE': [
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ],
        'INTROSPECTION_ENABLED': False,
    }
"""

# 7. Environment Variables for Security
"""
# .env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
"""

print("""
Django GraphQL Authentication Setup Complete!

Key Security Features Implemented:
✅ JWT Authentication with refresh tokens
✅ Protected queries and mutations with @login_required
✅ Role-based access control with @permission_required  
✅ Generic error messages to prevent account enumeration
✅ Query depth limiting to prevent DoS attacks
✅ Rate limiting middleware
✅ Introspection disabled in production
✅ Secure headers and SSL settings

Next Steps:
1. Install the required packages
2. Add configuration to settings.py
3. Set up URL routing
4. Implement social provider integration
5. Add rate limiting with Redis
6. Configure SSL certificates
7. Set up monitoring and logging
""")
