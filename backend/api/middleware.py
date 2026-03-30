# Custom middleware for GraphQL Error Handling
from django.contrib.auth.middleware import get_user
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class GraphQLJWTAuthenticationMiddleware:
    """
    Middleware to handle basic authentication for GraphQL requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Basic authentication without JWT for now
        if request.path == '/graphql/' or request.path == '/api/graphql/':
            try:
                # For now, just set user from Django session
                request.user = get_user(request)
                if request.user.is_authenticated:
                    logger.info(f"User {request.user.username} authenticated for GraphQL")
            except Exception as e:
                logger.error(f"Authentication error: {str(e)}")
                pass

        response = self.get_response(request)
        return response

def graphql_error_middleware(next, root, info, **args):
    """
    GraphQL middleware for consistent error handling
    """
    try:
        result = next(root, info, **args)
        return result
    except Exception as e:
        logger.error(f"GraphQL error in {info.field_name}: {str(e)}")
        
        # Handle specific error types
        if "ERPNext" in str(e):
            return {
                "success": False,
                "error": "ERPNext connection failed",
                "message": "Unable to connect to ERPNext system. Please try again later.",
                "code": "ERPNEXT_CONNECTION_ERROR"
            }
        elif "AI" in str(e) or "Gemini" in str(e):
            return {
                "success": False,
                "error": "AI service unavailable",
                "message": "AI service is temporarily unavailable. Please try again later.",
                "code": "AI_SERVICE_ERROR"
            }
        elif "permission" in str(e).lower():
            return {
                "success": False,
                "error": "Permission denied",
                "message": "You don't have permission to perform this action.",
                "code": "PERMISSION_DENIED"
            }
        else:
            return {
                "success": False,
                "error": "Internal server error",
                "message": "An unexpected error occurred. Please try again later.",
                "code": "INTERNAL_SERVER_ERROR"
            }

class GraphQLRateLimitMiddleware:
    """
    Middleware to implement rate limiting for GraphQL requests
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}

    def __call__(self, request):
        if request.path == '/graphql/':
            client_ip = self.get_client_ip(request)
            
            # Simple rate limiting (in production, use Redis or similar)
            if self.is_rate_limited(client_ip):
                return JsonResponse({
                    "errors": [{
                        "message": "Rate limit exceeded",
                        "extensions": {"code": "RATE_LIMITED"}
                    }]
                }, status=429)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, client_ip):
        # Simple in-memory rate limiting (for demo purposes)
        import time
        current_time = time.time()
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Remove old requests (older than 1 hour)
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if current_time - timestamp < 3600
        ]
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        
        # Check if rate limit exceeded (1000 requests per hour for authenticated users)
        rate_limit = 1000 if hasattr(self, 'user') and self.user.is_authenticated else 100
        
        return len(self.request_counts[client_ip]) > rate_limit

class GraphQLSecurityMiddleware:
    """
    Security middleware for GraphQL requests
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/graphql/':
            # Security checks
            if not self.is_valid_origin(request):
                return JsonResponse({
                    "errors": [{
                        "message": "Invalid origin",
                        "extensions": {"code": "INVALID_ORIGIN"}
                    }]
                }, status=403)
            
            # Check for suspicious queries
            if self.is_suspicious_query(request):
                logger.warning(f"Suspicious GraphQL query from {self.get_client_ip(request)}")
                return JsonResponse({
                    "errors": [{
                        "message": "Query blocked for security reasons",
                        "extensions": {"code": "SECURITY_VIOLATION"}
                    }]
                }, status=403)
        
        response = self.get_response(request)
        return response
    
    def is_valid_origin(self, request):
        # Check origin against allowed origins
        origin = request.META.get('HTTP_ORIGIN')
        if not origin:
            return True
        
        allowed_origins = [
            'http://localhost:3000',
            'http://localhost:5173',
            'http://127.0.0.1:3000',
            'http://127.0.0.1:5173'
        ]
        
        return origin in allowed_origins
    
    def is_suspicious_query(self, request):
        # Check for suspicious patterns in GraphQL queries
        if request.method == 'POST':
            try:
                import json
                data = json.loads(request.body)
                query = data.get('query', '')
                
                # Check for introspection queries in production
                if '__schema' in query and not self.is_debug_mode():
                    return True
                
                # Check for extremely large queries
                if len(query) > 10000:
                    return True
                
                # Check for nested depth attacks
                depth = self.calculate_query_depth(query)
                if depth > 10:
                    return True
                
            except (json.JSONDecodeError, KeyError):
                return True
        
        return False
    
    def is_debug_mode(self):
        from django.conf import settings
        return settings.DEBUG
    
    def calculate_query_depth(self, query):
        # Simple depth calculation (in production, use proper GraphQL analysis)
        return query.count('{')
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

print("GraphQL middleware loaded with authentication, error handling, rate limiting, and security")
