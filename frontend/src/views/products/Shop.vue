<template>
  <div class="shop-page bg-deep min-h-screen pb-20">
    <!-- Hero Banner -->
    <section class="shop-hero relative h-80 flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 bg-black/60 z-10"></div>
      <img src="https://i.postimg.cc/0QKmBBJ9/kitchen2.png" class="absolute inset-0 w-full h-full object-cover grayscale-[0.5]" />
      <div class="relative z-20 text-center px-4">
        <h1 class="text-5xl md:text-6xl font-bold gold-text mb-4 drop-shadow-lg">{{ $t('shopTitle') || 'الكتالوج الملكي' }}</h1>
        <p class="text-xl text-white/80 max-w-2xl mx-auto">{{ $t('shopSubtitle') || 'تصاميم فينيل ورخام تجسد الفخامة في كل تفصيل' }}</p>
      </div>
    </section>

    <div class="container mx-auto px-4 mt-12">
      <div class="flex flex-col lg:flex-row gap-12">
        <!-- Mobile Filter Toggle -->
        <div class="lg:hidden flex justify-between items-center mb-6">
          <button class="btn-filter-mobile" @click="showMobileFilters = true">
            <i class="fa-solid fa-sliders-h"></i>
            {{ $t('filter') }}
          </button>
          <div class="text-white/60 text-sm">
            {{ filteredProducts.length }} {{ $t('results') }}
          </div>
        </div>

        <!-- Mobile Filter Drawer -->
        <transition name="fade">
          <div v-if="showMobileFilters" class="mobile-filter-overlay" @click="showMobileFilters = false"></div>
        </transition>
        <transition name="slide-up">
          <div v-if="showMobileFilters" class="mobile-filter-drawer">
            <div class="drawer-header">
              <h3 class="gold-text font-bold">{{ $t('filter') }}</h3>
              <button @click="showMobileFilters = false"><i class="fa-solid fa-times"></i></button>
            </div>
            <div class="drawer-content p-6">
              <!-- Categories (Mobile) -->
              <div class="mb-8">
                <h4 class="text-white font-bold mb-4">{{ $t('categories') }}</h4>
                <div class="grid grid-cols-2 gap-3">
                  <button
                    v-for="cat in categories"
                    :key="cat.id"
                    @click="activeCategory = cat.id"
                    class="mobile-cat-btn"
                    :class="{ active: activeCategory === cat.id }"
                  >
                    <i :class="getCategoryIcon(cat.id)"></i>
                    {{ $t(cat.id) }}
                  </button>
                </div>
              </div>

              <!-- Price Range (Mobile) -->
              <div class="mb-8">
                <h4 class="text-white font-bold mb-4">{{ $t('price') }}</h4>
                <input
                  type="range"
                  class="gold-range w-full"
                  min="0"
                  max="50000"
                  step="500"
                  v-model="priceRange"
                />
                <div class="flex justify-between mt-4 gold-text">
                  <span>0 دج</span>
                  <span>{{ priceRange.toLocaleString() }} دج</span>
                </div>
              </div>

              <button class="w-full btn-gold py-4 rounded-xl font-bold" @click="showMobileFilters = false">
                {{ $t('apply') }}
              </button>
            </div>
          </div>
        </transition>

        <!-- Sidebar Filters (Desktop) -->
        <aside class="hidden lg:block lg:w-1/4">
          <div class="glass-card p-8 sticky top-24">
            <h3 class="text-2xl font-bold gold-text mb-8 flex items-center gap-3">
              <i class="fa-solid fa-sliders-h"></i> {{ $t('filter') }}
            </h3>

            <!-- Categories -->
            <div class="mb-10">
              <h4 class="text-white font-bold mb-4 uppercase text-xs tracking-widest">{{ $t('categories') }}</h4>
              <div class="flex flex-col gap-2">
                <button
                  v-for="cat in categories"
                  :key="cat.id"
                  @click="activeCategory = cat.id"
                  class="filter-link"
                  :class="{ active: activeCategory === cat.id }"
                >
                  <span class="flex items-center gap-3">
                    <i :class="getCategoryIcon(cat.id)"></i>
                    {{ $t(cat.id) }}
                  </span>
                  <span class="count-badge">{{ cat.count }}</span>
                </button>
              </div>
            </div>

            <!-- Price Range -->
            <div class="mb-10">
              <h4 class="text-white font-bold mb-4 uppercase text-xs tracking-widest">{{ $t('price') }}</h4>
              <input
                type="range"
                class="gold-range w-full"
                min="0"
                max="50000"
                step="500"
                v-model="priceRange"
              />
              <div class="flex justify-between mt-4 text-sm font-mono gold-text">
                <span>0 دج</span>
                <span>{{ priceRange.toLocaleString() }} دج</span>
              </div>
            </div>

            <button class="w-full btn-gold-outline py-4 rounded-xl font-bold" @click="resetFilters">
              {{ $t('reset') }}
            </button>
          </div>
        </aside>

        <!-- Product Grid -->
        <main class="lg:w-3/4">
          <!-- Toolbar -->
          <div class="flex flex-col sm:flex-row justify-between items-center mb-10 gap-6">
            <div class="text-white/60 font-medium">
              تم العثور على <span class="gold-text font-bold text-xl mx-1">{{ filteredProducts.length }}</span> تصميم
            </div>
            <div class="flex items-center gap-4">
              <input
                v-model="semanticQuery"
                type="text"
                class="glass-select py-2 px-4"
                placeholder="بحث دلالي: modern marble for office"
              />
              <button class="btn-gold-outline py-2 px-4 rounded-xl font-bold" @click="runSemanticSearch">
                بحث ذكي
              </button>
              <span class="text-xs text-white/40 uppercase tracking-widest">ترتيب:</span>
              <select class="glass-select py-2 px-6" v-model="sortBy">
                <option value="newest">{{ $t('newest') }}</option>
                <option value="price-low">السعر: الأدنى أولاً</option>
                <option value="price-high">السعر: الأعلى أولاً</option>
              </select>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="loader-royal mb-6"></div>
            <p class="gold-text animate-pulse">جاري تحميل التصاميم الملكية...</p>
          </div>

          <!-- No Results -->
          <div v-else-if="filteredProducts.length === 0" class="glass-card text-center py-20 px-8">
            <div class="mb-6 text-6xl text-white/10">
              <i class="fa-solid fa-search"></i>
            </div>
            <h3 class="text-2xl font-bold gold-text mb-2">لا توجد نتائج تطابق بحثك</h3>
            <p class="text-white/40">جرب تغيير الفلاتر أو السعر للحصول على نتائج أفضل</p>
          </div>

          <!-- Grid -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
            <div v-for="product in paginatedProducts" :key="product.id" class="product-item-anim">
              <ProductCard :product="product" />
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="mt-16 flex justify-center gap-4">
            <button 
              class="pagination-btn" 
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              <i class="fa-solid fa-chevron-right"></i>
            </button>
            
            <button 
              v-for="page in totalPages" 
              :key="page"
              class="pagination-btn"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>

            <button 
              class="pagination-btn" 
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              <i class="fa-solid fa-chevron-left"></i>
            </button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import ProductCard from '@/components/ProductCard.vue';
import ERPNextService from '@/integration/services/ERPNextService';
import SemanticSearchService from '@/integration/services/SemanticSearchService';

const products = ref([]);
const loading = ref(true);
const activeCategory = ref('all');
const priceRange = ref(50000);
const sortBy = ref('newest');
const currentPage = ref(1);
const itemsPerPage = ref(9);
const showMobileFilters = ref(false);
const semanticQuery = ref('');

const categories = ref([
  { id: 'all', key: 'allCategories', icon: 'fa-solid fa-th-large', count: 0 },
  { id: 'furniture', key: 'furniture', icon: 'fa-solid fa-couch', count: 0 },
  { id: 'doors', key: 'doors', icon: 'fa-solid fa-door-open', count: 0 },
  { id: 'walls', key: 'walls', icon: 'fa-solid fa-paint-roller', count: 0 },
  { id: 'ceilings', key: 'ceilings', icon: 'fa-solid fa-arrow-up', count: 0 },
  { id: 'tiles', key: 'tiles', icon: 'fa-solid fa-border-all', count: 0 },
  { id: 'kitchens', key: 'kitchens', icon: 'fa-solid fa-utensils', count: 0 },
  { id: 'cars', key: 'cars', icon: 'fa-solid fa-car', count: 0 },
]);

const getCategoryIcon = (id) => {
  const icons = {
    all: 'fa-solid fa-th-large',
    walls: 'fa-solid fa-paint-roller',
    doors: 'fa-solid fa-door-open',
    furniture: 'fa-solid fa-couch',
    kitchens: 'fa-solid fa-utensils',
    ceilings: 'fa-solid fa-arrow-up',
    tiles: 'fa-solid fa-border-all',
    cars: 'fa-solid fa-car'
  };
  return icons[id] || 'fa-solid fa-box';
};

const mapERPNextCategory = (group) => {
  const mapping = {
    Walls: 'walls',
    Doors: 'doors',
    Furniture: 'furniture',
    Kitchens: 'kitchens',
    Ceilings: 'ceilings',
    Tiles: 'tiles',
    Cars: 'cars',
  };
  return mapping[group] || 'all';
};

const updateCategoryCounts = () => {
  categories.value.forEach((cat) => {
    if (cat.id === 'all') {
      cat.count = products.value.length;
    } else {
      cat.count = products.value.filter((p) => p.category === cat.id).length;
    }
  });
};

const filteredProducts = computed(() => {
  let result = [...products.value];
  if (activeCategory.value !== 'all') {
    result = result.filter((p) => p.category === activeCategory.value);
  }
  result = result.filter((p) => p.price <= priceRange.value);
  if (sortBy.value === 'price-low') {
    result.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === 'price-high') {
    result.sort((a, b) => b.price - a.price);
  }
  return result;
});

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredProducts.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage.value));

const resetFilters = () => {
  activeCategory.value = 'all';
  priceRange.value = 50000;
  sortBy.value = 'newest';
};

const runSemanticSearch = async () => {
  const query = semanticQuery.value.trim();
  if (!query) return;
  loading.value = true;
  try {
    const data = await SemanticSearchService.searchProducts(query, {
      category: activeCategory.value,
      topK: 40,
    });
    products.value = (data.results || []).map((p) => ({
      id: p.id,
      title: p.name,
      price: p.price,
      image: p.image || 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
      category: p.category || 'all',
      categoryKey: p.category || 'all',
      categoryIcon: 'fa-solid fa-star',
      minSize: '50',
      maxSize: '200',
      excerpt: `Semantic score: ${p.score}`,
      onSale: false,
      discount: 0,
      isNew: false,
    }));
    updateCategoryCounts();
    currentPage.value = 1;
  } catch (error) {
    console.error('Semantic search failed:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  try {
    const response = await ERPNextService.getProducts();
    if (response.success) {
      products.value = response.data.map((p) => ({
        id: p.name,
        title: p.item_name,
        price: p.standard_rate,
        image: p.image || 'https://i.postimg.cc/wjXjw0mj/slider-decore2.png',
        category: mapERPNextCategory(p.item_group),
        categoryKey: mapERPNextCategory(p.item_group),
        categoryIcon: 'fa-solid fa-star', // For compatibility with ProductCard
        minSize: '50',
        maxSize: '200',
        excerpt: p.description || 'تصميم ملكي فاخر بجودة عالية',
        onSale: Math.random() > 0.7,
        discount: 15,
        isNew: Math.random() > 0.8
      }));
      updateCategoryCounts();
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.bg-deep {
  background:
    radial-gradient(circle at 20% 0%, rgba(212, 175, 55, 0.08), transparent 38%),
    radial-gradient(circle at 80% 100%, rgba(180, 180, 180, 0.08), transparent 35%),
    linear-gradient(180deg, #08090c 0%, #101319 60%, #12161d 100%);
}
.gold-text { color: #d4af37; }

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
}

.filter-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  text-align: right;
}

.filter-link:hover {
  background: rgba(212, 175, 55, 0.05);
  color: #d4af37;
}

.filter-link.active {
  background: rgba(212, 175, 55, 0.1);
  color: #d4af37;
  font-weight: 700;
  box-shadow: inset 0 0 10px rgba(212, 175, 55, 0.1);
}

.count-badge {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-mono: true;
}

.gold-range {
  accent-color: #d4af37;
  height: 4px;
  border-radius: 2px;
}

.btn-gold-outline {
  border: 1px solid #d4af37;
  color: #d4af37;
  transition: all 0.3s;
}

.btn-gold-outline:hover {
  background: #d4af37;
  color: #000;
}

.glass-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  outline: none;
  cursor: pointer;
}

.loader-royal {
  width: 48px;
  height: 48px;
  border: 3px solid #d4af37;
  border-bottom-color: transparent;
  border-radius: 50%;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.pagination-btn {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  border-color: #d4af37;
  color: #d4af37;
  transform: translateY(-2px);
}

.pagination-btn.active {
  background: #d4af37;
  color: #000;
  border-color: #d4af37;
  font-weight: 800;
}

.pagination-btn:disabled {
  opacity: 0.2;
  cursor: not-allowed;
}

/* Mobile Filter Drawer Styles */
.mobile-filter-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  z-index: 1000;
}

.mobile-filter-drawer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #121212;
  border-top: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 32px 32px 0 0;
  z-index: 1001;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 24px 12px;
}

.drawer-header button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-cat-btn {
  padding: 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s;
}

.mobile-cat-btn.active {
  background: rgba(212, 175, 55, 0.1);
  border-color: #d4af37;
  color: #d4af37;
}

.btn-filter-mobile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: #d4af37;
  color: #000;
  border-radius: 12px;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.btn-gold {
  background: #d4af37;
  color: #000;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

/* Transitions */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }

.product-item-anim {
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transition: transform 0.35s ease, filter 0.35s ease;
}

.product-item-anim:hover {
  transform: translateY(-6px) scale(1.01);
  filter: drop-shadow(0 10px 28px rgba(212, 175, 55, 0.2));
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom classes for Tailwind-like utilities */
.container { max-width: 1400px; }
.shop-hero img {
  transform: scale(1.04);
  transition: transform 6s ease;
}

.shop-hero:hover img {
  transform: scale(1.09);
}
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.gap-12 { gap: 3rem; }
.gap-8 { gap: 2rem; }
.gap-6 { gap: 1.5rem; }
.gap-4 { gap: 1rem; }
.gap-3 { gap: 0.75rem; }
.mx-auto { margin-left: auto; margin-right: auto; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.mt-12 { margin-top: 3rem; }
.mt-16 { margin-top: 4rem; }
.mb-10 { margin-bottom: 2.5rem; }
.mb-8 { margin-bottom: 2rem; }
.mb-6 { margin-bottom: 1.5rem; }
.w-full { width: 100%; }
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.p-6 { padding: 1.5rem; }
.p-8 { padding: 2rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.py-20 { padding-top: 5rem; padding-bottom: 5rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.px-8 { padding-left: 2rem; padding-right: 2rem; }
.sticky { position: sticky; }
.top-24 { top: 6rem; }

@media (min-width: 640px) { .sm\:flex-row { flex-direction: row; } }
@media (min-width: 768px) { .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { 
  .lg\:flex-row { flex-direction: row; }
  .lg\:w-1\/4 { width: 25%; } 
  .lg\:w-3\/4 { width: 75%; } 
  .hidden.lg\:block { display: block; }
  .lg\:hidden { display: none; }
}
@media (min-width: 1280px) { .xl\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }

.hidden { display: none; }
</style>
