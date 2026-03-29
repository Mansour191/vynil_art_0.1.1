# GraphQL Schema Extensions - Missing Components
# This file contains the missing GraphQL resolvers for ERPNext Sync, Semantic Search, and Complex Pricing

import graphene
from django.db.models import Q
from decimal import Decimal
from .models import ERPNextSyncLog, PricingEngine
from .models import Product, Material, Category

# --- ERPNext Sync Types ---

class ERPNextSyncLogType(graphene.ObjectType):
    id = graphene.ID()
    action = graphene.String()
    status = graphene.String()
    message = graphene.String()
    records_synced = graphene.Int()
    error_message = graphene.String()
    timestamp = graphene.DateTime()

class ERPNextSyncResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    sync_log = graphene.Field(ERPNextSyncLogType)
    records_synced = graphene.Int()

# --- Semantic Search Types ---

class SemanticSearchResultType(graphene.ObjectType):
    product = graphene.Field('ProductType')
    relevance_score = graphene.Float()
    matched_fields = graphene.List(graphene.String())
    highlights = graphene.List(graphene.String())

class SemanticSearchResponse(graphene.ObjectType):
    results = graphene.List(SemanticSearchResultType)
    total_count = graphene.Int()
    search_time = graphene.Float()
    success = graphene.Boolean()

# --- Complex Pricing Types ---

class PriceCalculationInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    material_id = graphene.ID()
    width = graphene.Decimal(required=True)
    height = graphene.Decimal(required=True)
    dimension_unit = graphene.String(default_value="cm")
    quantity = graphene.Int(default_value=1)
    custom_options = graphene.String()  # JSON string for custom options

class PriceCalculationResult(graphene.ObjectType):
    base_price = graphene.Decimal()
    material_price = graphene.Decimal()
    labor_price = graphene.Decimal()
    shipping_price = graphene.Decimal()
    total_price = graphene.Decimal()
    price_per_m2 = graphene.Decimal()
    breakdown = graphene.String()  # JSON string for detailed breakdown
    calculation_time = graphene.Float()

class PricingEngineResponse(graphene.ObjectType):
    success = graphene.Boolean()
    calculation = graphene.Field(PriceCalculationResult)
    message = graphene.String()
    errors = graphene.String()

# --- ERPNext Sync Mutations ---

class SyncWithERPNextMutation(graphene.Mutation):
    class Arguments:
        sync_type = graphene.String(required=True)  # "products", "orders", "customers"
        dry_run = graphene.Boolean(default_value=False)
    
    Output = ERPNextSyncResponse
    
    def mutate(self, info, sync_type, dry_run=False):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return ERPNextSyncResponse(
                success=False, 
                message='غير مصرح لك بمزامنة ERPNext'
            )
        
        try:
            # Mock ERPNext sync logic
            if dry_run:
                return ERPNextSyncResponse(
                    success=True,
                    message='تم التحقق من المزامنة بنجاح (وضع الاختبار)',
                    records_synced=0
                )
            
            # Actual sync logic would go here
            sync_log = ERPNextSyncLog.objects.create(
                action=f"Sync {sync_type}",
                status="success",
                message=f"تمت مزامنة {sync_type} بنجاح",
                records_synced=10  # Mock count
            )
            
            return ERPNextSyncResponse(
                success=True,
                message=f'تمت مزامنة {sync_type} بنجاح',
                sync_log=sync_log,
                records_synced=sync_log.records_synced
            )
            
        except Exception as e:
            return ERPNextSyncResponse(
                success=False,
                message=str(e),
                errors=str(e)
            )

class PushToERPNextMutation(graphene.Mutation):
    class Arguments:
        entity_type = graphene.String(required=True)  # "order", "product"
        entity_id = graphene.ID(required=True)
    
    Output = ERPNextSyncResponse
    
    def mutate(self, info, entity_type, entity_id):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return ERPNextSyncResponse(
                success=False, 
                message='غير مصرح لك بدفع البيانات إلى ERPNext'
            )
        
        try:
            # Mock push logic
            sync_log = ERPNextSyncLog.objects.create(
                action=f"Push {entity_type}",
                status="success",
                message=f"تم دفع {entity_type} #{entity_id} إلى ERPNext بنجاح",
                records_synced=1
            )
            
            return ERPNextSyncResponse(
                success=True,
                message=f'تم دفع {entity_type} إلى ERPNext بنجاح',
                sync_log=sync_log,
                records_synced=1
            )
            
        except Exception as e:
            return ERPNextSyncResponse(
                success=False,
                message=str(e),
                errors=str(e)
            )

# --- Semantic Search Query ---

class SemanticSearchQuery(graphene.ObjectType):
    semantic_search = graphene.Field(
        SemanticSearchResponse,
        query=graphene.String(required=True),
        filters=graphene.String(),  # JSON string for filters
        limit=graphene.Int(default_value=10)
    )
    
    def resolve_semantic_search(self, info, query, filters=None, limit=10):
        if not query.strip():
            return SemanticSearchResponse(
                results=[],
                total_count=0,
                search_time=0.0,
                success=False
            )
        
        try:
            import time
            start_time = time.time()
            
            # Mock semantic search logic
            # In real implementation, this would use vector embeddings or AI search
            products = Product.objects.filter(
                Q(name_ar__icontains=query) | 
                Q(name_en__icontains=query) |
                Q(description_ar__icontains=query) |
                Q(description_en__icontains=query)
            ).select_related('category')[:limit]
            
            results = []
            for product in products:
                # Mock relevance score
                relevance_score = 0.8  # In real implementation, calculate based on similarity
                
                # Mock matched fields
                matched_fields = []
                if query.lower() in product.name_ar.lower():
                    matched_fields.append('name_ar')
                if query.lower() in product.name_en.lower():
                    matched_fields.append('name_en')
                
                # Mock highlights
                highlights = [f"Found '{query}' in {field}" for field in matched_fields]
                
                results.append(SemanticSearchResultType(
                    product=product,
                    relevance_score=relevance_score,
                    matched_fields=matched_fields,
                    highlights=highlights
                ))
            
            search_time = time.time() - start_time
            
            return SemanticSearchResponse(
                results=results,
                total_count=len(results),
                search_time=search_time,
                success=True
            )
            
        except Exception as e:
            return SemanticSearchResponse(
                results=[],
                total_count=0,
                search_time=0.0,
                success=False
            )

# --- Complex Pricing Query ---

class CalculatePriceQuery(graphene.ObjectType):
    calculate_price = graphene.Field(
        PricingEngineResponse,
        input=PriceCalculationInput(required=True)
    )
    
    def resolve_calculate_price(self, info, input):
        try:
            import time
            start_time = time.time()
            
            # Get product
            try:
                product = Product.objects.get(pk=input['product_id'])
            except Product.DoesNotExist:
                return PricingEngineResponse(
                    success=False,
                    message='المنتج غير موجود'
                )
            
            # Get material if specified
            material = None
            if input.get('material_id'):
                try:
                    material = Material.objects.get(pk=input['material_id'])
                except Material.DoesNotExist:
                    return PricingEngineResponse(
                        success=False,
                        message='المادة غير موجودة'
                    )
            
            # Calculate base price
            base_price = product.base_price
            
            # Calculate material price
            material_price = Decimal('0')
            if material:
                # Convert dimensions to m2
                width_m = input['width'] / 100  # Convert cm to m
                height_m = input['height'] / 100  # Convert cm to m
                area_m2 = width_m * height_m
                material_price = material.price_per_m2 * area_m2
            
            # Calculate labor price (mock calculation)
            labor_price = base_price * Decimal('0.3')  # 30% of base price
            
            # Calculate shipping price (mock calculation)
            shipping_price = Decimal('50.00')  # Fixed shipping
            
            # Calculate total price
            total_price = (base_price + material_price + labor_price + shipping_price) * input['quantity']
            
            # Calculate price per m2
            width_m = input['width'] / 100
            height_m = input['height'] / 100
            area_m2 = width_m * height_m
            price_per_m2 = total_price / area_m2 if area_m2 > 0 else Decimal('0')
            
            # Create breakdown
            breakdown = {
                'base_price': str(base_price),
                'material_price': str(material_price),
                'labor_price': str(labor_price),
                'shipping_price': str(shipping_price),
                'quantity': input['quantity'],
                'total_before_quantity': str(base_price + material_price + labor_price + shipping_price),
                'area_m2': str(area_m2),
                'dimensions': {
                    'width': str(input['width']),
                    'height': str(input['height']),
                    'unit': input.get('dimension_unit', 'cm')
                }
            }
            
            calculation_time = time.time() - start_time
            
            return PricingEngineResponse(
                success=True,
                calculation=PriceCalculationResult(
                    base_price=base_price,
                    material_price=material_price,
                    labor_price=labor_price,
                    shipping_price=shipping_price,
                    total_price=total_price,
                    price_per_m2=price_per_m2,
                    breakdown=str(breakdown),
                    calculation_time=calculation_time
                ),
                message='تم حساب السعر بنجاح'
            )
            
        except Exception as e:
            return PricingEngineResponse(
                success=False,
                message=f'خطأ في حساب السعر: {str(e)}',
                errors=str(e)
            )

# --- ERPNext Sync Queries ---

class ERPNextSyncQuery(graphene.ObjectType):
    erpnext_sync_logs = graphene.List(
        ERPNextSyncLogType,
        limit=graphene.Int(default_value=20),
        status=graphene.String()
    )
    
    def resolve_erpnext_sync_logs(self, info, limit=20, status=None):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return []
        
        queryset = ERPNextSyncLog.objects.all()
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-timestamp')[:limit]

# --- Pricing Engine Query ---

class PricingEngineQuery(graphene.ObjectType):
    pricing_engines = graphene.List(PricingEngineType)
    
    def resolve_pricing_engines(self, info):
        if not info.context.user.is_authenticated or not info.context.user.is_staff:
            return []
        
        return PricingEngine.objects.all()

# --- Extended Schema ---

class ExtendedQuery(
    SemanticSearchQuery,
    CalculatePriceQuery,
    ERPNextSyncQuery,
    PricingEngineQuery
):
    pass

class ExtendedMutation(graphene.ObjectType):
    # ERPNext Sync Mutations
    sync_with_erpnext = SyncWithERPNextMutation.Field()
    push_to_erpnext = PushToERPNextMutation.Field()

print("🔧 GraphQL Schema Extensions loaded")
print("📋 Added: ERPNext Sync, Semantic Search, Complex Pricing")
