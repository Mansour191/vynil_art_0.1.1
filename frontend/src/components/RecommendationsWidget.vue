<template>
  <div class="recommendations-widget">
    <!-- عنوان حسب النوع -->
    <div class="widget-header" v-if="title">
      <h3><i :class="icon"></i> {{ title }}</h3>
      <router-link v-if="viewAllLink" :to="viewAllLink" class="view-all">
        عرض الكل <i class="fa-solid fa-chevron-left"></i>
      </router-link>
    </div>

    <!-- حالة التحميل -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>جاري تحميل التوصيات...</p>
    </div>

    <!-- قائمة المنتجات -->
    <div v-else-if="products.length > 0" class="products-grid" :class="{ horizontal: horizontal }">
      <div
        v-for="item in products"
        :key="item.product?.id || item.id"
        class="product-card"
        @click="viewProduct(item.product || item)"
      >
        <div class="product-image">
          <img :src="item.product?.image || item.image" :alt="item.product?.name || item.name" />
          <span v-if="item.score" class="score-badge">
            {{ Math.round(item.score * 100) }}% توافق
          </span>
        </div>

        <div class="product-info">
          <h4 class="product-name">{{ item.product?.name || item.name }}</h4>
          <p class="product-category">
            {{ getCategoryLabel(item.product?.category || item.category) }}
          </p>

          <div class="product-price">
            <span class="current-price">{{
              formatCurrency(item.product?.price || item.price)
            }}</span>
          </div>

          <button class="btn-add-cart" @click.stop="addToCart(item.product || item)">
            <i class="fa-solid fa-shopping-cart"></i>
            <span>أضف للسلة</span>
          </button>
        </div>

        <!-- أضف داخل product-card، بعد product-info -->
        <div v-if="item.details" class="product-badges">
          <span v-if="item.details.event" class="badge event">
            <i class="fa-solid fa-gift"></i> {{ item.details.event }}
          </span>
          <span v-if="item.details.season" class="badge season">
            <i class="fa-solid fa-sun"></i> {{ getSeasonName(item.details.season) }}
          </span>
          <span v-if="item.details.priority === 'high'" class="badge urgent">
            <i class="fa-solid fa-exclamation-circle"></i> مخزون محدود
          </span>
          <span v-if="item.details.daysUntil === 0" class="badge today">
            <i class="fa-solid fa-clock"></i> اليوم آخر فرصة
          </span>
        </div>

        <!-- شارة نوع التوصية -->
        <div v-if="item.type" class="recommendation-badge" :class="item.type">
          <i :class="getTypeIcon(item.type)"></i>
          <span>{{ getTypeLabel(item.type) }}</span>
        </div>
      </div>
    </div>

    <!-- لا توجد توصيات -->
    <div v-else class="empty-state">
      <i class="fa-solid fa-gift"></i>
      <p>لا توجد توصيات متاحة</p>
    </div>
  </div>
</template>

<script>
import CurrencyService from '@/integration/services/CurrencyService';

export default {
  name: 'RecommendationsWidget',
  props: {
    title: {
      type: String,
      default: 'توصيات لك',
    },
    icon: {
      type: String,
      default: 'fa-solid fa-star',
    },
    products: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
    horizontal: {
      type: Boolean,
      default: false,
    },
    viewAllLink: {
      type: [String, Object],
      default: null,
    },
  },
  methods: {
    formatCurrency(value) {
      return CurrencyService.formatAmount(value || 0);
    },

    getCategoryLabel(category) {
      const categories = {
        walls: 'جدران',
        doors: 'أبواب',
        cars: 'سيارات',
        kitchens: 'مطابخ',
        furniture: 'أثاث',
        ceilings: 'أسقف',
        tiles: 'بلاط',
      };
      return categories[category] || category;
    },

    getTypeIcon(type) {
      const icons = {
        collaborative: 'fa-solid fa-users',
        content: 'fa-solid fa-tag',
        trending: 'fa-solid fa-fire',
        similar: 'fa-solid fa-clone',
      };
      return icons[type] || 'fa-solid fa-star';
    },

    getTypeLabel(type) {
      const labels = {
        collaborative: 'مناسب لك',
        content: 'مقترح',
        trending: 'رائج',
        similar: 'مشابه',
      };
      return labels[type] || 'توصية';
    },

    viewProduct(product) {
      this.$router.push(`/dashboard/products?view=${product.id}`);
    },

    addToCart(product) {
      this.$emit('add-to-cart', product);
      this.$toast?.success('تمت الإضافة إلى السلة');
    },

    getSeasonName(season) {
      const names = {
        spring: 'الربيع',
        summer: 'الصيف',
        autumn: 'الخريف',
        winter: 'الشتاء',
      };
      return names[season] || season;
    },
  },
};
</script>

<style scoped>
.recommendations-widget {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid var(--border-light);
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.widget-header h3 {
  color: white;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.widget-header h3 i {
  color: var(--gold-1);
}

.view-all {
  color: var(--gold-1);
  text-decoration: none;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s;
}

.view-all:hover {
  transform: translateX(-3px);
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: var(--text-dim);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(212, 175, 55, 0.3);
  border-top-color: var(--gold-1);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.products-grid.horizontal {
  display: flex;
  overflow-x: auto;
  padding-bottom: 10px;
  gap: 15px;
}

.products-grid.horizontal .product-card {
  min-width: 200px;
  flex-shrink: 0;
}

.product-card {
  background: var(--bg-primary);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.product-image {
  height: 150px;
  position: relative;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.score-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
}

.product-info {
  padding: 15px;
}

.product-name {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 5px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-category {
  color: var(--gold-1);
  font-size: 0.75rem;
  margin-bottom: 8px;
}

.product-price {
  margin-bottom: 10px;
}

.current-price {
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
}

.btn-add-cart {
  width: 100%;
  padding: 8px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: var(--bg-deep);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s;
}

.btn-add-cart:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.recommendation-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  gap: 3px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

.recommendation-badge.collaborative {
  background: #9c27b0;
}

.recommendation-badge.trending {
  background: #f44336;
}

.recommendation-badge.similar {
  background: #2196f3;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-dim);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: var(--gold-1);
  opacity: 0.5;
}

.product-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 8px;
}

.badge {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.65rem;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}

.badge.event {
  background: #9c27b0;
  color: white;
}

.badge.season {
  background: #ff9800;
  color: white;
}

.badge.urgent {
  background: #f44336;
  color: white;
  animation: pulse 1.5s infinite;
}

.badge.today {
  background: #d4af37;
  color: #1a1a2e;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
