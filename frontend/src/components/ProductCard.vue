<template>
  <div class="product-card" :class="{ 'on-sale': product.onSale }">
    <!-- صورة المنتج مع شارات -->
    <div class="product-image-container">
      <img :src="product.image" :alt="product.title" class="product-image" loading="lazy" />

      <!-- شارة التخفيض -->
      <span v-if="isOnSale" class="sale-badge">
        {{ discount }}% OFF
      </span>

      <!-- شارة التسعير الذكي -->
      <span v-if="pricingData" class="ai-pricing-badge">
        <i class="fa-solid fa-brain"></i>
        AI
      </span>

      <!-- شارة جديد -->
      <span v-if="product.isNew" class="new-badge">
        {{ $t('new') }}
      </span>

      <!-- زر المفضلة -->
      <button class="favorite-btn" @click="toggleFavorite">
        <i :class="isFavorite ? 'fa-solid fa-heart' : 'far fa-heart'"></i>
      </button>
    </div>

    <!-- معلومات المنتج -->
    <div class="product-info">
      <div class="category-chip">
        <i :class="['fas', product.categoryIcon || 'fa-tag']"></i>
        {{ $t(product.categoryKey || 'general') }}
      </div>

      <h3 class="product-title" v-ai-t>
        <router-link :to="`/product/${product.id}`">
          {{ product.translations?.[locale]?.title || product.title }}
        </router-link>
      </h3>

      <p class="product-excerpt" v-ai-t>{{ product.translations?.[locale]?.excerpt || product.excerpt }}</p>

      <!-- السعر والمساحة مع معلومات التسعير الذكي -->
      <div class="product-footer">
        <div class="price-section">
          <div class="price-container">
            <span class="current-price" :class="{ 'sale-price': isOnSale }">
              {{ formatPrice(currentPrice) }}
            </span>
            <span v-if="isOnSale" class="original-price">
              {{ formatPrice(originalPrice) }}
            </span>
            
            <!-- مؤشر اتجاه السعر -->
            <div v-if="pricingData" class="price-trend" :class="priceTrend">
              <i :class="priceTrend === 'rising' ? 'fa-solid fa-arrow-up' : priceTrend === 'falling' ? 'fa-solid fa-arrow-down' : 'fa-solid fa-minus'"></i>
            </div>
          </div>
          
          <!-- تفاصيل التسعير الذكي -->
          <div v-if="pricingData && showPricingDetails" class="pricing-details">
            <div class="pricing-factors">
              <div v-for="factor in ['demand', 'competition', 'seasonality', 'inventory']" :key="factor" class="factor-item">
                <span class="factor-label">{{ getPricingInsight(factor)?.label }}</span>
                <span class="factor-value" :class="{ positive: getPricingInsight(factor)?.value > 1, negative: getPricingInsight(factor)?.value < 1 }">
                  {{ formatFactorValue(getPricingInsight(factor)?.value, factor) }}
                </span>
              </div>
            </div>
            
            <div class="pricing-explanation">
              <small>{{ generatePricingExplanation() }}</small>
            </div>
            
            <div class="pricing-confidence">
              <span class="confidence-label">مستوى الثقة:</span>
              <div class="confidence-bar">
                <div class="confidence-fill" :style="{ width: (pricingConfidence * 100) + '%' }"></div>
              </div>
              <span class="confidence-value">{{ Math.round(pricingConfidence * 100) }}%</span>
            </div>
          </div>
          
          <!-- زر عرض تفاصيل التسعير -->
          <button 
            v-if="pricingData" 
            class="pricing-toggle-btn" 
            @click="showPricingDetails = !showPricingDetails"
          >
            <i :class="showPricingDetails ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"></i>
            {{ showPricingDetails ? 'إخفاء' : 'عرض' }} التسعير الذكي
          </button>
        </div>
        
        <div class="size-chip">
          <i class="fa-solid fa-ruler-combined"></i>
          {{ product.minSize }} - {{ product.maxSize }} سم
        </div>
      </div>

      <!-- أزرار الإجراءات -->
      <div class="actions-grid">
        <router-link :to="`/product/${product.id}`" class="btn-preview">
          <i class="fa-solid fa-eye"></i>
          {{ $t('preview') }}
        </router-link>
        <button class="btn-order" @click="addToCart" :disabled="pricingLoading">
          <i :class="pricingLoading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-shopping-cart'"></i>
          {{ pricingLoading ? 'جاري التحديث...' : $t('order') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import PricingService from '@/services/PricingService';
import AIService from '@/services/AIService';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['add-to-cart', 'toggle-favorite']);
const store = useStore();
const { locale } = useI18n();

// State
const isFavorite = ref(false);
const pricingData = ref(null);
const pricingLoading = ref(false);
const showPricingDetails = ref(false);

// Computed
const isInWishlist = computed(() => {
  return store.getters['wishlist/isInWishlist'](props.product.id);
});

const currentPrice = computed(() => {
  if (pricingData.value && pricingData.value.finalPrice) {
    return pricingData.value.finalPrice;
  }
  return props.product.price;
});

const originalPrice = computed(() => {
  if (pricingData.value && pricingData.value.basePrice) {
    return pricingData.value.basePrice;
  }
  return props.product.originalPrice || props.product.price;
});

const isOnSale = computed(() => {
  return currentPrice.value < originalPrice.value;
});

const discount = computed(() => {
  if (!isOnSale.value) return 0;
  return Math.round(((originalPrice.value - currentPrice.value) / originalPrice.value) * 100);
});

const pricingConfidence = computed(() => {
  return pricingData.value?.confidence || 0;
});

const pricingRecommendations = computed(() => {
  return pricingData.value?.recommendations || [];
});

const priceTrend = computed(() => {
  if (!pricingData.value) return 'stable';
  
  const factors = pricingData.value.factors || {};
  if (factors.demand > 1.1) return 'rising';
  if (factors.demand < 0.9) return 'falling';
  return 'stable';
});

const addToCart = () => {
  emit('add-to-cart', {
    ...props.product,
    price: currentPrice.value,
    originalPrice: originalPrice.value,
    discount: discount.value,
    pricingData: pricingData.value
  });
};

const formatPrice = (price) => {
  return new Intl.NumberFormat(locale.value, {
    style: 'currency',
    currency: 'DZD',
    minimumFractionDigits: 0,
  }).format(price);
};

const loadDynamicPricing = async () => {
  if (!props.product.id) return;
  
  try {
    pricingLoading.value = true;
    
    // Get dynamic pricing from AI service
    const pricing = await PricingService.calculateDynamicPrice(props.product.id, {
      customerSegment: 'regular', // Could be dynamic based on user
      location: 'algeria',
      quantity: 1
    });
    
    pricingData.value = pricing;
    
    console.log('Dynamic pricing loaded:', pricing);
  } catch (error) {
    console.error('Error loading dynamic pricing:', error);
  } finally {
    pricingLoading.value = false;
  }
};

const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value;
  emit('toggle-favorite', props.product);
};

const getPricingInsight = (type) => {
  const factors = pricingData.value?.factors || {};
  const factorValues = {
    demand: { label: 'الطلب', value: factors.demand, icon: 'fa-chart-line' },
    competition: { label: 'المنافسة', value: factors.competition, icon: 'fa-users' },
    seasonality: { label: 'الموسمية', value: factors.seasonality, icon: 'fa-calendar' },
    inventory: { label: 'المخزون', value: factors.inventory, icon: 'fa-boxes' }
  };
  
  return factorValues[type] || null;
};

const formatFactorValue = (value, type) => {
  if (type === 'demand' || type === 'competition' || type === 'seasonality' || type === 'inventory') {
    const percentage = ((value - 1) * 100).toFixed(1);
    return `${percentage > 0 ? '+' : ''}${percentage}%`;
  }
  return value;
};

const generatePricingExplanation = () => {
  if (!pricingData.value) return '';
  
  const factors = pricingData.value.factors || {};
  const explanations = [];
  
  if (factors.demand > 1.05) {
    explanations.push('الطلب مرتفع على المنتج');
  }
  if (factors.competition < 0.95) {
    explanations.push('سوق تنافسي يتطلب تسعير تنافسي');
  }
  if (factors.seasonality > 1.05) {
    explanations.push('موسمة ذروف تزيد الطلب');
  }
  if (factors.inventory < 0.9) {
    explanations.push('مخزون مرتفع يتطلب عرض خصم');
  }
  
  return explanations.join('، ') || 'التسعير القياسي';
};

// Lifecycle
onMounted(() => {
  loadDynamicPricing();
  
  // Subscribe to real-time pricing updates
  const ws = PricingService.subscribeToPriceUpdates((data) => {
    if (data.productId === props.product.id) {
      pricingData.value = data.pricing;
    }
  });
  
  // Refresh pricing every 5 minutes
  setInterval(loadDynamicPricing, 300000);
});
</script>

<style scoped>
.product-card {
  background: var(--bg-card);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  position: relative;
}

.product-card:hover {
  transform: translateY(-10px);
  border-color: #d4af37;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.product-image-container {
  position: relative;
  height: 250px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover .product-image {
  transform: scale(1.1);
}

.sale-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: var(--gold-gradient);
  color: #000;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  z-index: 2;
}

.new-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background: #4caf50;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  z-index: 2;
}

.ai-pricing-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 0.7rem;
  font-weight: 600;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 4px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.favorite-btn {
  position: absolute;
  bottom: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 2;
}

.favorite-btn:hover {
  background: #fff;
  color: #f44336;
}

.product-info {
  padding: 20px;
}

.category-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(212, 175, 55, 0.1);
  color: #d4af37;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.7rem;
  margin-bottom: 12px;
}

.product-title {
  font-size: 1.1rem;
  margin-bottom: 8px;
  line-height: 1.4;
}

.product-title a {
  color: #fff;
  text-decoration: none;
  transition: color 0.3s;
}

.product-title a:hover {
  color: #d4af37;
}

.product-excerpt {
  font-size: 0.85rem;
  color: var(--text-dim);
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.price-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price-container {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.current-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: #d4af37;
  transition: color 0.3s ease;
}

.sale-price {
  color: #f44336;
}

.original-price {
  font-size: 0.85rem;
  color: var(--text-dim);
  text-decoration: line-through;
  margin-right: 8px;
}

.price-trend {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
}

.price-trend.rising {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.price-trend.falling {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.price-trend.stable {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.pricing-details {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 12px;
  margin-top: 8px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.pricing-factors {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.factor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  font-size: 0.75rem;
}

.factor-label {
  color: var(--text-dim);
  font-weight: 500;
}

.factor-value {
  font-weight: 600;
  font-size: 0.8rem;
}

.factor-value.positive {
  color: #4caf50;
}

.factor-value.negative {
  color: #f44336;
}

.pricing-explanation {
  color: var(--text-dim);
  font-size: 0.8rem;
  line-height: 1.4;
  margin-bottom: 12px;
  padding: 8px;
  background: rgba(212, 175, 55, 0.1);
  border-radius: 8px;
  border-right: 3px solid #d4af37;
}

.pricing-confidence {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.confidence-label {
  font-size: 0.75rem;
  color: var(--text-dim);
  font-weight: 500;
}

.confidence-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #f44336 0%, #ff9800 50%, #4caf50 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.confidence-value {
  font-size: 0.75rem;
  font-weight: 600;
  color: #d4af37;
  min-width: 45px;
}

.pricing-toggle-btn {
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.3);
  color: #667eea;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.pricing-toggle-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
  transform: translateY(-1px);
}

.size-chip {
  font-size: 0.75rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 6px;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.btn-preview, .btn-order {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-preview {
  background: var(--bg-primary);
  color: #fff;
  border: 1px solid var(--border-light);
}

.btn-preview:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #d4af37;
  transform: translateY(-2px);
}

.btn-order {
  background: var(--gold-gradient, linear-gradient(135deg, #d4af37 0%, #f1d592 100%));
  color: #1a1a2e;
  border: none;
}

.btn-order:hover {
  background: linear-gradient(135deg, #f1d592 0%, #d4af37 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
}

.btn-order:disabled {
  background: var(--text-dim);
  cursor: not-allowed;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .pricing-factors {
    grid-template-columns: 1fr;
  }
  
  .price-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .product-footer {
    gap: 8px;
  }
}
</style>
