import math
import os
import re
from collections import Counter

from django.db.models import Prefetch
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

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


def _estimate_area_with_cv2(image_bytes, reference_dimension_cm):
    import cv2  # optional dependency
    import numpy as np

    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image data")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 70, 180)
    edge_pixels = int((edges > 0).sum())
    total_pixels = edges.shape[0] * edges.shape[1]
    if total_pixels == 0:
        raise ValueError("Empty image")

    # Heuristic: more edges usually means wider visible surface coverage.
    coverage_ratio = min(max((edge_pixels / total_pixels) * 8, 0.15), 0.95)
    reference_m = float(reference_dimension_cm) / 100.0
    estimated_area = max((reference_m ** 2) * (1.6 + coverage_ratio), 0.5)
    return round(estimated_area, 3)


def _estimate_area_fallback(image_bytes, reference_dimension_cm):
    from PIL import Image
    from io import BytesIO

    image = Image.open(BytesIO(image_bytes))
    w, h = image.size
    if w <= 0 or h <= 0:
        raise ValueError("Invalid image dimensions")
    aspect_factor = max(min(max(w, h) / max(min(w, h), 1), 2.5), 1.0)
    reference_m = float(reference_dimension_cm) / 100.0
    estimated_area = max((reference_m ** 2) * (1.4 + (aspect_factor * 0.5)), 0.5)
    return round(estimated_area, 3)


@api_view(["POST"])
@permission_classes([AllowAny])
def measure_surface(request):
    image = request.FILES.get("image")
    reference_dimension_cm = request.data.get("reference_dimension_cm")
    price_per_m2 = request.data.get("price_per_m2")

    if not image:
        return Response({"error": "image is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        reference_dimension_cm = float(reference_dimension_cm)
        if reference_dimension_cm <= 0:
            raise ValueError()
    except Exception:
        return Response({"error": "reference_dimension_cm must be a positive number"}, status=400)

    image_bytes = image.read()
    try:
        estimated_area_m2 = _estimate_area_with_cv2(image_bytes, reference_dimension_cm)
        engine = "opencv"
    except Exception:
        estimated_area_m2 = _estimate_area_fallback(image_bytes, reference_dimension_cm)
        engine = "fallback"

    total_price = None
    if price_per_m2 not in (None, ""):
        try:
            total_price = round(float(price_per_m2) * estimated_area_m2, 2)
        except Exception:
            total_price = None

    return Response(
        {
            "estimated_area_m2": estimated_area_m2,
            "total_price": total_price,
            "engine": engine,
        }
    )


def _load_knowledge_chunks():
    kb_dir = os.getenv("KB_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base"))
    chunks = []
    if not os.path.isdir(kb_dir):
        return chunks

    for name in os.listdir(kb_dir):
        path = os.path.join(kb_dir, name)
        if not os.path.isfile(path):
            continue

        text = ""
        lower = name.lower()
        try:
            if lower.endswith((".md", ".txt")):
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            elif lower.endswith(".pdf"):
                try:
                    from pypdf import PdfReader

                    reader = PdfReader(path)
                    text = "\n".join((page.extract_text() or "") for page in reader.pages)
                except Exception:
                    text = ""
        except Exception:
            text = ""

        if text.strip():
            for paragraph in text.split("\n\n"):
                clean = paragraph.strip()
                if len(clean) > 40:
                    chunks.append({"source": name, "text": clean})

    return chunks


def _gemini_answer(prompt):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
        response = model.generate_content(prompt)
        return getattr(response, "text", None)
    except Exception:
        return None


@api_view(["POST"])
@permission_classes([AllowAny])
def chat_service(request):
    message = (request.data.get("message") or "").strip()
    if not message:
        return Response({"error": "message is required"}, status=400)

    chunks = _load_knowledge_chunks()
    ranked = sorted(
        chunks,
        key=lambda c: _cosine_similarity(message, c["text"]),
        reverse=True,
    )
    top = [c for c in ranked[:3] if _cosine_similarity(message, c["text"]) > 0.12]

    if top:
        context = "\n\n".join([f"[{c['source']}] {c['text'][:500]}" for c in top])
        answer = (
            "اعتماداً على دليل Paclos:\n\n"
            f"{context[:900]}\n\n"
            "إذا أردت، أستطيع تحويل هذه الخطوات إلى قائمة تطبيق عملية لمساحتك."
        )
        return Response({"answer": answer, "source": "knowledge_base"})

    prompt = (
        "You are Paclos interior decoration assistant. "
        "Answer in Arabic, stay concise, and keep context on vinyl/marble interior applications.\n"
        f"User question: {message}"
    )
    gemini = _gemini_answer(prompt)
    if gemini:
        return Response({"answer": gemini, "source": "gemini"})

    return Response(
        {
            "answer": "حالياً قاعدة المعرفة غير كافية لهذا السؤال، لكن يمكنني مساعدتك باقتراح خامة فينيل مناسبة حسب نوع السطح والإضاءة.",
            "source": "fallback",
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def semantic_product_search(request):
    query = (request.data.get("query") or "").strip()
    category = (request.data.get("category") or "").strip().lower()
    top_k = int(request.data.get("top_k") or 12)

    if not query:
        return Response({"results": [], "total": 0})

    products = Product.objects.select_related("category").prefetch_related(
        Prefetch("variants", queryset=ProductVariant.objects.all())
    )
    if category and category != "all":
        products = products.filter(category__slug=category)

    results = []
    for product in products:
        style_tags = " ".join(v.name_en for v in product.variants.all())
        blob = " ".join(
            [
                product.name_ar or "",
                product.name_en or "",
                product.description_ar or "",
                product.description_en or "",
                product.category.name_ar or "",
                product.category.name_en or "",
                style_tags,
            ]
        )
        score = _cosine_similarity(query, blob)
        if score > 0:
            results.append(
                {
                    "id": product.id,
                    "slug": product.slug,
                    "name": product.name_ar or product.name_en,
                    "price": float(product.base_price),
                    "image": product.image.url if product.image else "",
                    "category": product.category.slug,
                    "score": round(score, 4),
                }
            )

    results.sort(key=lambda x: x["score"], reverse=True)
    trimmed = results[:top_k]
    return Response({"results": trimmed, "total": len(results)})
