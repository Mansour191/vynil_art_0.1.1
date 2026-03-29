"""
Blog endpoints for Django GraphQL project.
Simple blog posts endpoint to avoid 404 errors.
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta
import random

@csrf_exempt
@require_http_methods(["GET"])
def blog_posts_list(request):
    """Simple blog posts endpoint to avoid 404 errors"""
    try:
        # Get limit parameter
        limit = int(request.GET.get('limit', 10))
        
        # Mock blog posts data
        mock_posts = [
            {
                "id": 1,
                "title": "أحدث اتجاهات تصميم الفينيل لعام 2024",
                "title_en": "Latest Vinyl Design Trends 2024",
                "slug": "latest-vinyl-design-trends-2024",
                "excerpt": "استكشف أحدث التقنيات والاتجاهات في عالم تصميم الفينيل...",
                "content": "محتوى مفصل حول اتجاهات تصميم الفينيل لعام 2024...",
                "author": "فريق تصميم الفينيل",
                "published_at": "2024-03-15T10:00:00Z",
                "category": "design",
                "image": "/images/blog/vinyl-trends-2024.jpg",
                "read_time": 5,
                "likes": 42,
                "comments": 8
            },
            {
                "id": 2,
                "title": "كيفية اختيار أفضل نوع الفينيل لمشروعك",
                "title_en": "How to Choose the Best Vinyl Type for Your Project",
                "slug": "choose-best-vinyl-type",
                "excerpt": "دليل شامل لأنواع الفينيل المختلفة واستخداماتها...",
                "content": "محتوى مفصل حول أنواع الفينيل وكيفية الاختيار...",
                "author": "خبراء الفينيل",
                "published_at": "2024-03-10T14:30:00Z",
                "category": "tutorial",
                "image": "/images/blog/vinyl-types.jpg",
                "read_time": 7,
                "likes": 35,
                "comments": 12
            },
            {
                "id": 3,
                "title": "تقنيات التركيب الاحترافية للفينيل",
                "title_en": "Professional Vinyl Installation Techniques",
                "slug": "professional-vinyl-installation",
                "excerpt": "تعلم أفضل طرق تركيب الفينيل لضمان نتائج مثالية...",
                "content": "محتوى مفصل حول تقنيات تركيب الفينيل...",
                "author": "الفنيون المتخصصون",
                "published_at": "2024-03-05T09:15:00Z",
                "category": "installation",
                "image": "/images/blog/installation.jpg",
                "read_time": 10,
                "likes": 28,
                "comments": 6
            },
            {
                "id": 4,
                "title": "العناية والصيانة: كيفية الحفاظ على الفينيل",
                "title_en": "Care and Maintenance: How to Preserve Vinyl",
                "slug": "vinyl-care-maintenance",
                "excerpt": "نصائح هامة للحفاظ على جودة ومظهر الفينيل...",
                "content": "محتوى مفصل حول العناية بالفينيل...",
                "author": "فريق الصيانة",
                "published_at": "2024-02-28T16:45:00Z",
                "category": "maintenance",
                "image": "/images/blog/vinyl-care.jpg",
                "read_time": 6,
                "likes": 19,
                "comments": 4
            }
        ]
        
        # Limit results
        limited_posts = mock_posts[:limit]
        
        return JsonResponse({
            "status": "success",
            "count": len(limited_posts),
            "results": limited_posts
        })
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def blog_post_detail(request, slug):
    """Get single blog post by slug"""
    try:
        # Mock post lookup
        mock_posts = {
            "latest-vinyl-design-trends-2024": {
                "id": 1,
                "title": "أحدث اتجاهات تصميم الفينيل لعام 2024",
                "title_en": "Latest Vinyl Design Trends 2024",
                "slug": "latest-vinyl-design-trends-2024",
                "content": "محتوى مفصل حول اتجاهات تصميم الفينيل لعام 2024...",
                "author": "فريق تصميم الفينيل",
                "published_at": "2024-03-15T10:00:00Z",
                "category": "design",
                "image": "/images/blog/vinyl-trends-2024.jpg",
                "read_time": 5,
                "likes": 42,
                "comments": 8,
                "tags": ["تصميم", "فينيل", "اتجاهات", "2024"]
            }
        }
        
        if slug not in mock_posts:
            return JsonResponse({
                "status": "error",
                "message": "Blog post not found"
            }, status=404)
            
        return JsonResponse({
            "status": "success",
            "post": mock_posts[slug]
        })
        
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)
