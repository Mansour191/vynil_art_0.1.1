"""
Products endpoints for Django GraphQL project.
Simple products endpoint to provide product data for frontend.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime

@csrf_exempt
@require_http_methods(["GET"])
def products_list(request):
    """Simple products endpoint to provide product data"""
    try:
        # Get limit parameter
        limit = int(request.GET.get('limit', 50))
        
        # Mock products data with comprehensive information
        mock_products = [
            {
                "id": 1,
                "name": "PROD-001",
                "item_name": "ملصق جدار وردة حمراء",
                "item_code": "WAL-001",
                "description": "ملصق جداري عالي الجودة بتصميم وردة حمراء أنيقة، مثالي لتزيين غرف المعيشة والمنازل",
                "category": "Walls",
                "item_group": "Walls",
                "stock_uom": "Unit",
                "standard_rate": 45,
                "actual_qty": 23,
                "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.5,
                "reviews_count": 12,
                "tags": ["جدار", "ورود", "أحمر", "ديكور"],
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-03-20T14:30:00Z"
            },
            {
                "id": 2,
                "name": "PROD-002",
                "item_name": "ملصق باب خشبي كلاسيكي",
                "item_code": "DOR-001",
                "description": "تصميم خشبي كلاسيكي للأبواب، يضيف لمسة فاخرة لأي باب داخلي أو خارجي",
                "category": "Doors",
                "item_group": "Doors",
                "stock_uom": "Unit",
                "standard_rate": 65,
                "actual_qty": 18,
                "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.8,
                "reviews_count": 8,
                "tags": ["باب", "خشب", "كلاسيكي", "ديكور"],
                "created_at": "2024-01-20T09:15:00Z",
                "updated_at": "2024-03-18T16:45:00Z"
            },
            {
                "id": 3,
                "name": "PROD-003",
                "item_name": "ملصق أرضية رخامي أبيض",
                "item_code": "TIL-001",
                "description": "ملصق أرضيات بتصميم رخامي أبيض فاخر، يوفر مظهراً راقياً بتكلفة معقولة",
                "category": "Tiles",
                "item_group": "Tiles",
                "stock_uom": "Square Meter",
                "standard_rate": 120,
                "actual_qty": 45,
                "image_url": "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?q=80&w=800&auto=format&fit=crop",
                "featured": False,
                "rating": 4.2,
                "reviews_count": 15,
                "tags": ["أرضية", "رخام", "أبيض", "فاخر"],
                "created_at": "2024-02-01T11:30:00Z",
                "updated_at": "2024-03-22T10:20:00Z"
            },
            {
                "id": 4,
                "name": "PROD-004",
                "item_name": "ملصق سقف نجومي ليلي",
                "item_code": "CEL-001",
                "description": "تصميم سماوي ليلي بالنجوم، مثالي لغرف الأطفال وغرف النوم",
                "category": "Ceilings",
                "item_group": "Ceilings",
                "stock_uom": "Unit",
                "standard_rate": 85,
                "actual_qty": 12,
                "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.7,
                "reviews_count": 20,
                "tags": ["سقف", "نجوم", "ليلي", "أطفال"],
                "created_at": "2024-02-10T14:00:00Z",
                "updated_at": "2024-03-19T13:15:00Z"
            },
            {
                "id": 5,
                "name": "PROD-005",
                "item_name": "ملصق مطبخ زيتون أخضر",
                "item_code": "KIT-001",
                "description": "تصميم طبيعي بأغصان الزيتون، يضيف جمالاً طبيعياً للمطابخ",
                "category": "Kitchens",
                "item_group": "Kitchens",
                "stock_uom": "Unit",
                "standard_rate": 95,
                "actual_qty": 8,
                "image_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?q=80&w=800&auto=format&fit=crop",
                "featured": False,
                "rating": 4.6,
                "reviews_count": 9,
                "tags": ["مطبخ", "زيتون", "أخضر", "طبيعي"],
                "created_at": "2024-02-15T16:45:00Z",
                "updated_at": "2024-03-21T09:30:00Z"
            },
            {
                "id": 6,
                "name": "PROD-006",
                "item_name": "ملصق سيارة سباق أحمر",
                "item_code": "CAR-001",
                "description": "تصميم ديناميكي لسيارات السباق، مثالي لعشاق السيارات والسرعة",
                "category": "Cars",
                "item_group": "Cars",
                "stock_uom": "Unit",
                "standard_rate": 150,
                "actual_qty": 5,
                "image_url": "https://images.unsplash.com/photo-1542362567-b07e54358753?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.9,
                "reviews_count": 25,
                "tags": ["سيارة", "سباق", "أحمر", "ديناميكي"],
                "created_at": "2024-02-20T10:30:00Z",
                "updated_at": "2024-03-23T15:00:00Z"
            },
            {
                "id": 7,
                "name": "PROD-007",
                "item_name": "ملصق أثاث أنيق بيج",
                "item_code": "FUR-001",
                "description": "تصميم بيج أنيق للأثاث، يناسب مختلف أنواع الأثاث المنزلي",
                "category": "Furniture",
                "item_group": "Furniture",
                "stock_uom": "Unit",
                "standard_rate": 75,
                "actual_qty": 15,
                "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop",
                "featured": False,
                "rating": 4.3,
                "reviews_count": 11,
                "tags": ["أثاث", "بيج", "أنيق", "منزلي"],
                "created_at": "2024-02-25T12:15:00Z",
                "updated_at": "2024-03-17T11:45:00Z"
            },
            {
                "id": 8,
                "name": "PROD-008",
                "item_name": "ملصق بلاط أزرق بحري",
                "item_code": "TIL-002",
                "description": "تصميم بحري باللون الأزرق، مثالي للحمامات والمطابخ",
                "category": "Tiles",
                "item_group": "Tiles",
                "stock_uom": "Square Meter",
                "standard_rate": 110,
                "actual_qty": 30,
                "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.4,
                "reviews_count": 18,
                "tags": ["بلاط", "أزرق", "بحري", "حمام"],
                "created_at": "2024-03-01T08:30:00Z",
                "updated_at": "2024-03-24T14:20:00Z"
            }
        ]
        
        # Filter featured products if requested
        featured_only = request.GET.get('featured', 'false').lower() == 'true'
        if featured_only:
            mock_products = [p for p in mock_products if p.get('featured', False)]
        
        # Limit results
        limited_products = mock_products[:limit]
        
        return JsonResponse({
            "success": True,
            "count": len(limited_products),
            "results": limited_products
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
            "error": "products_fetch_error"
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, product_id):
    """Get single product by ID"""
    try:
        # Mock product lookup
        mock_products = {
            1: {
                "id": 1,
                "name": "PROD-001",
                "item_name": "ملصق جدار وردة حمراء",
                "item_code": "WAL-001",
                "description": "ملصق جداري عالي الجودة بتصميم وردة حمراء أنيقة، مثالي لتزيين غرف المعيشة والمنازل",
                "category": "Walls",
                "item_group": "Walls",
                "stock_uom": "Unit",
                "standard_rate": 45,
                "actual_qty": 23,
                "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800&auto=format&fit=crop",
                "featured": True,
                "rating": 4.5,
                "reviews_count": 12,
                "tags": ["جدار", "ورود", "أحمر", "ديكور"],
                "specifications": {
                    "width": "100cm",
                    "height": "70cm",
                    "material": "Vinyl Premium",
                    "water_resistant": True,
                    "uv_protected": True
                }
            }
        }
        
        if product_id not in mock_products:
            return JsonResponse({
                "success": False,
                "message": "Product not found",
                "error": "product_not_found"
            }, status=404)
            
        return JsonResponse({
            "success": True,
            "product": mock_products[product_id]
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
            "error": "product_fetch_error"
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def categories_list(request):
    """Get product categories"""
    try:
        categories = [
            {"id": 1, "name": "Walls", "name_ar": "الجدران", "count": 15},
            {"id": 2, "name": "Doors", "name_ar": "الأبواب", "count": 8},
            {"id": 3, "name": "Tiles", "name_ar": "البلاط", "count": 12},
            {"id": 4, "name": "Ceilings", "name_ar": "الأسقف", "count": 6},
            {"id": 5, "name": "Kitchens", "name_ar": "المطابخ", "count": 10},
            {"id": 6, "name": "Cars", "name_ar": "السيارات", "count": 5},
            {"id": 7, "name": "Furniture", "name_ar": "الأثاث", "count": 9}
        ]
        
        return JsonResponse({
            "success": True,
            "count": len(categories),
            "results": categories
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e),
            "error": "categories_fetch_error"
        }, status=400)
