<!-- src/components/ProductGrid.vue -->
<template>
  <div class="product-grid-wrapper">
    <!-- شريط التصفية -->
    <div class="filter-toolbar">
      <div class="filter-left">
        <div class="filters-chips">
          <button
            v-for="filter in filters"
            :key="filter.value"
            class="filter-btn"
            :class="{ active: currentFilter === filter.value }"
            @click="setFilter(filter.value)"
          >
            <i :class="['fas', filter.icon || 'fa-tag']"></i>
            {{ $t(filter.label) }}
          </button>
        </div>
      </div>

      <div class="filter-right">
        <!-- ترتيب حسب -->
        <div class="sort-container">
          <i class="fa-solid fa-sort-amount-down sort-icon"></i>
          <select v-model="sortBy" class="sort-select">
            <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>

        <!-- عرض شبكة/قائمة -->
        <div class="view-toggle">
          <button
            class="toggle-btn"
            :class="{ active: viewMode === 'grid' }"
            @click="viewMode = 'grid'"
          >
            <i class="fa-solid fa-th-large"></i>
          </button>
          <button
            class="toggle-btn"
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
          >
            <i class="fa-solid fa-list"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- شبكة المنتجات -->
    <div v-if="viewMode === 'grid'" class="products-grid">
      <ProductCard
        v-for="product in sortedProducts"
        :key="product.id"
        :product="product"
        @toggle-favorite="handleToggleFavorite"
        @add-to-cart="handleAddToCart"
      />
    </div>

    <!-- عرض القائمة -->
    <div v-else class="products-list">
      <div v-for="product in sortedProducts" :key="product.id" class="list-item">
        <router-link :to="`/product/${product.id}`" class="item-link">
          <div class="item-image">
            <img :src="product.image" :alt="product.title" />
          </div>
          <div class="item-content">
            <div class="item-header">
              <h3 class="item-title">{{ product.title }}</h3>
              <span v-if="product.onSale" class="sale-badge">
                {{ product.discount }}% OFF
              </span>
            </div>
            <div class="item-meta">
              <span class="category-tag">
                <i :class="['fas', product.categoryIcon || 'fa-tag']"></i>
                {{ $t(product.categoryKey || 'general') }}
              </span>
              <span class="size-tag">
                <i class="fa-solid fa-ruler-combined"></i>
                {{ product.minSize }} - {{ product.maxSize }} سم
              </span>
            </div>
            <p class="item-excerpt">{{ product.excerpt }}</p>
            <div class="item-footer">
              <span class="item-price">{{ formatPrice(product.price) }}</span>
            </div>
          </div>
        </router-link>
        <div class="item-actions">
          <button class="btn-fav" @click="handleToggleFavorite(product)">
            <i class="far fa-heart"></i>
          </button>
          <button class="btn-cart" @click="handleAddToCart(product)">
            <i class="fa-solid fa-shopping-cart"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import ProductCard from '@/components/ProductCard.vue';

const props = defineProps({
  products: {
    type: Array,
    required: true,
  },
});

const { t, locale } = useI18n();
const emit = defineEmits(['toggle-favorite', 'add-to-cart']);

// State
const currentFilter = ref('all');
const sortBy = ref('newest');
const viewMode = ref('grid');

const filters = [
  { label: 'all', value: 'all', icon: 'fa-solid fa-th-large' },
  { label: 'onSale', value: 'sale', icon: 'fa-solid fa-tag' },
  { label: 'isNew', value: 'new', icon: 'fa-solid fa-star' },
  { label: 'popular', value: 'popular', icon: 'fa-solid fa-fire' },
];

const sortOptions = [
  { label: t('newest'), value: 'newest' },
  { label: t('priceLowToHigh'), value: 'price_asc' },
  { label: t('priceHighToLow'), value: 'price_desc' },
  { label: t('bestRating'), value: 'rating' },
];

// Computed
const filteredProducts = computed(() => {
  if (currentFilter.value === 'all') return props.products;
  if (currentFilter.value === 'sale') return props.products.filter((p) => p.onSale);
  if (currentFilter.value === 'new') return props.products.filter((p) => p.isNew);
  if (currentFilter.value === 'popular') return props.products.filter((p) => p.rating >= 4.5);
  return props.products;
});

const sortedProducts = computed(() => {
  const products = [...filteredProducts.value];
  if (sortBy.value === 'newest') return products.reverse();
  if (sortBy.value === 'price_asc') return products.sort((a, b) => a.price - b.price);
  if (sortBy.value === 'price_desc') return products.sort((a, b) => b.price - a.price);
  if (sortBy.value === 'rating') return products.sort((a, b) => b.rating - a.rating);
  return products;
});

// Methods
const setFilter = (filter) => {
  currentFilter.value = filter;
};

const formatPrice = (price) => {
  return new Intl.NumberFormat(locale.value, {
    style: 'currency',
    currency: 'DZD',
    minimumFractionDigits: 0,
  }).format(price);
};

const handleToggleFavorite = (p) => emit('toggle-favorite', p);
const handleAddToCart = (p) => emit('add-to-cart', p);
</script>

<style scoped>
.product-grid-wrapper {
  width: 100%;
}

.filter-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
  background: var(--bg-card);
  padding: 15px 25px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
}

.filters-chips {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--border-light);
  background: transparent;
  color: var(--text-dim);
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  background: rgba(212, 175, 55, 0.1);
  color: #d4af37;
}

.filter-btn.active {
  background: var(--gold-gradient);
  color: #000;
  border: none;
}

.filter-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.sort-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-primary);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

.sort-icon {
  color: #d4af37;
}

.sort-select {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 0.85rem;
  cursor: pointer;
  outline: none;
}

.view-toggle {
  display: flex;
  background: var(--bg-primary);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
}

.toggle-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.3s;
}

.toggle-btn.active {
  background: var(--bg-card);
  color: #d4af37;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.list-item {
  background: var(--bg-card);
  border-radius: 20px;
  border: 1px solid var(--border-light);
  overflow: hidden;
  display: flex;
  transition: all 0.3s;
  position: relative;
}

.list-item:hover {
  transform: translateX(-5px);
  border-color: #d4af37;
}

.item-link {
  display: flex;
  flex: 1;
  text-decoration: none;
  color: inherit;
}

.item-image {
  width: 200px;
  height: 150px;
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-content {
  flex: 1;
  padding: 20px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-title {
  font-size: 1.2rem;
  color: #fff;
}

.sale-badge {
  background: var(--gold-gradient);
  color: #000;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
}

.item-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
}

.category-tag, .size-tag {
  font-size: 0.8rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 6px;
}

.item-excerpt {
  font-size: 0.9rem;
  color: var(--text-dim);
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #d4af37;
}

.item-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  background: rgba(255,255,255,0.02);
  border-right: 1px solid var(--border-light);
}

.btn-fav, .btn-cart {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  background: var(--bg-primary);
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.3s;
}

.btn-fav:hover { color: #f44336; background: #fff; }
.btn-cart:hover { color: #000; background: var(--gold-gradient); border: none; }

@media (max-width: 768px) {
  .list-item { flex-direction: column; }
  .item-image { width: 100%; height: 200px; }
  .item-actions { flex-direction: row; border-right: none; border-top: 1px solid var(--border-light); }
}
</style>
