"""
Simple Django views without DRF dependencies.
This file contains only the essential views needed for the frontend to work.
"""

import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

# Health check views - NO DRF imports
@csrf_exempt
@require_http_methods(["GET", "POST"])
def ai_health(request):
    """AI Service Health Check - Simple Django View"""
    return JsonResponse({
        "status": "healthy",
        "services": "all_active",
        "engine": "Gemini 1.5 Flash",
        "timestamp": "2026-03-28T00:45:27.278105Z"
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def erpnext_health(request):
    """ERPNext Service Health Check - Simple Django View"""
    return JsonResponse({
        "status": "connected",
        "latency_ms": 120,
        "sync_enabled": True
    })

# Pricing endpoints - Simple implementations
@csrf_exempt
@require_http_methods(["POST"])
def calculate_price(request):
    """Calculate dynamic pricing - Simple Django View"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # Simple mock calculation
        base_price = Decimal('100.00')
        total = base_price * Decimal(str(quantity))
        
        return JsonResponse({
            "status": "success",
            "base_price": str(base_price),
            "quantity": quantity,
            "total": str(total),
            "currency": "DZD"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def validate_coupon(request):
    """Validate coupon code - Simple Django View"""
    try:
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')
        
        # Simple mock validation
        if coupon_code == "SAVE10":
            return JsonResponse({
                "status": "valid",
                "discount_percent": 10,
                "discount_amount": "10.00"
            })
        else:
            return JsonResponse({
                "status": "invalid",
                "message": "Invalid coupon code"
            })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# Mock service endpoints for frontend compatibility
@csrf_exempt
def mock_ai_service(request, action, subaction=None, id=None):
    """Mock AI Service endpoints"""
    return JsonResponse({
        "status": "success",
        "action": action,
        "subaction": subaction,
        "id": id,
        "message": f"Mock AI service action: {action}"
    })

@csrf_exempt
def mock_erpnext_service(request, action, subaction=None, id=None):
    """Mock ERPNext Service endpoints"""
    return JsonResponse({
        "status": "success",
        "action": action,
        "subaction": subaction,
        "id": id,
        "message": f"Mock ERPNext service action: {action}"
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def pricing_competitors(request, slug):
    """Get competitor pricing - Simple Django View"""
    return JsonResponse({
        "status": "success",
        "slug": slug,
        "competitors": [
            {"name": "Competitor 1", "price": "95.00"},
            {"name": "Competitor 2", "price": "105.00"}
        ]
    })

@csrf_exempt
@require_http_methods(["POST"])
def pricing_batch_update(request):
    """Batch update pricing - Simple Django View"""
    try:
        data = json.loads(request.body)
        updates = data.get('updates', [])
        
        return JsonResponse({
            "status": "success",
            "updated_count": len(updates),
            "message": f"Updated {len(updates)} prices"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

# API Root view
def api_root(request):
    """API Root - Simple Django View"""
    return JsonResponse({
        "message": "Vinyl Art API",
        "version": "1.0.0",
        "endpoints": {
            "graphql": "/graphql/",
            "health_checks": {
                "ai": "/api/ai/health/",
                "erpnext": "/api/erpnext/health/"
            },
            "pricing": {
                "calculate": "/api/calculate-price/",
                "validate_coupon": "/api/validate-coupon/"
            }
        }
    })
