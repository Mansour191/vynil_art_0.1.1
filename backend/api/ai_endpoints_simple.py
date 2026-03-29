"""
Simple AI endpoints without DRF dependencies.
This file contains AI-related views using plain Django.
"""

import json
import math
import re
from collections import Counter
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch

from .models import Product, ProductVariant


def _tokenize(text):
    text = (text or "").lower()
    text = re.sub(r"[^\w\u0600-\u06FF\s]", " ", text)
    return [tok for tok in text.split() if len(tok) > 1]


def _cosine_similarity(text_a, text_b):
    a_tokens = Counter(_tokenize(text_a))
    b_tokens = Counter(_tokenize(text_b))
    if not a_tokens or not b_tokens:
        return 0.0
    common = set(a_tokens) & set(b_tokens)
    dot = sum(a_tokens[t] * b_tokens[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a_tokens.values()))
    norm_b = math.sqrt(sum(v * v for v in b_tokens.values()))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


@csrf_exempt
@require_http_methods(["POST"])
def measure_surface(request):
    """Measure surface from image - Simple Django View"""
    try:
        data = json.loads(request.body)
        # Mock surface measurement
        return JsonResponse({
            "status": "success",
            "surface_area": {
                "width": 100.5,
                "height": 80.3,
                "area": 8070.15,
                "unit": "cm²"
            },
            "estimated_cost": {
                "material_cost": "5000.00",
                "labor_cost": "2000.00",
                "total": "7000.00",
                "currency": "DZD"
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def chat_service(request):
    """AI Chat Service - Simple Django View"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        # Mock chat response
        return JsonResponse({
            "status": "success",
            "response": f"AI Response to: {message}",
            "confidence": 0.95,
            "timestamp": "2026-03-28T01:00:00Z"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def semantic_product_search(request):
    """Semantic Product Search - Simple Django View"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '')
        
        # Mock semantic search
        products = Product.objects.all()[:5]
        results = []
        for product in products:
            similarity = _cosine_similarity(query, product.name_en or product.name_ar or '')
            results.append({
                "id": product.id,
                "name": product.name_en or product.name_ar,
                "similarity": similarity,
                "price": str(product.base_price) if hasattr(product, 'base_price') else "100.00"
            })
        
        # Sort by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return JsonResponse({
            "status": "success",
            "query": query,
            "results": results[:10]
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_message(request):
    """Chatbot Message Handler - Simple Django View"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Mock chatbot response
        return JsonResponse({
            "status": "success",
            "message": f"Chatbot response to: {message}",
            "session_id": session_id,
            "timestamp": "2026-03-28T01:00:00Z",
            "intent": "general_inquiry",
            "confidence": 0.87
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def market_trends(request):
    """Market Trends Analysis - Simple Django View"""
    try:
        # Mock market trends data
        return JsonResponse({
            "status": "success",
            "trends": {
                "popular_materials": ["vinyl", "pvc", "adhesive"],
                "price_trends": {
                    "vinyl": {"change": "+5%", "period": "30 days"},
                    "pvc": {"change": "-2%", "period": "30 days"}
                },
                "demand_forecast": {
                    "next_month": "high",
                    "next_quarter": "very_high"
                }
            },
            "last_updated": "2026-03-28T01:00:00Z"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)
