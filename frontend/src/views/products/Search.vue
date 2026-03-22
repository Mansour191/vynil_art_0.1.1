<template>
  <div class="search-page">
    <div class="container py-5">
      <!-- Search Header -->
      <div class="search-header mb-5 text-center">
        <h1 class="mb-4 text-gold">{{ $t('advancedSearch') || 'البحث المتقدم' }}</h1>
        <div class="row justify-content-center">
          <div class="col-md-8">
            <form @submit.prevent="handleSearch" class="search-bar shadow-sm rounded-pill overflow-hidden">
              <div class="input-group input-group-lg">
                <span class="input-group-text border-0 bg-white ps-4">
                  <i class="fa-solid fa-search text-muted"></i>
                </span>
                <input
                  type="text"
                  class="form-control border-0 px-3"
                  v-model="filters.query"
                  :placeholder="$t('searchPlaceholder') || 'ابحث عن منتج، مقال، أو تصميم...'"
                  autofocus
                />
                <button class="btn btn-gold px-5 rounded-pill m-1" type="submit">
                  {{ $t('search') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Sidebar Filters -->
        <div class="col-lg-3 mb-4">
          <div class="filters-sidebar card shadow-sm border-0 rounded-lg sticky-top" style="top: 100px">
            <div class="card-body p-4">
              <h5 class="mb-4 border-bottom pb-2">
                <i class="fa-solid fa-sliders-h me-2"></i> {{ $t('filters') || 'تصفية النتائج' }}
              </h5>

              <!-- Type Filter -->
              <div class="filter-group mb-4">
                <label class="form-label font-weight-bold mb-3">{{ $t('resultType') || 'نوع النتيجة' }}</label>
                <div class="btn-group-vertical w-100" role="group">
                  <input type="radio" class="btn-check" name="type" id="type-all" value="all" v-model="filters.type">
                  <label class="btn btn-outline-light-gold text-start mb-1 rounded" for="type-all">
                    <i class="fa-solid fa-th-large me-2"></i> {{ $t('all') || 'الكل' }}
                  </label>
                  
                  <input type="radio" class="btn-check" name="type" id="type-product" value="product" v-model="filters.type">
                  <label class="btn btn-outline-light-gold text-start mb-1 rounded" for="type-product">
                    <i class="fa-solid fa-shopping-bag me-2"></i> {{ $t('products') || 'المنتجات' }}
                  </label>

                  <input type="radio" class="btn-check" name="type" id="type-article" value="article" v-model="filters.type">
                  <label class="btn btn-outline-light-gold text-start mb-1 rounded" for="type-article">
                    <i class="fa-solid fa-newspaper me-2"></i> {{ $t('articles') || 'المقالات' }}
                  </label>

                  <input type="radio" class="btn-check" name="type" id="type-design" value="design" v-model="filters.type">
                  <label class="btn btn-outline-light-gold text-start mb-1 rounded" for="type-design">
                    <i class="fa-solid fa-images me-2"></i> {{ $t('designs') || 'التصاميم' }}
                  </label>
                </div>
              </div>

              <!-- Category Filter -->
              <div class="filter-group mb-4">
                <label class="form-label font-weight-bold mb-3">{{ $t('category') }}</label>
                <select class="form-select border-0 bg-light" v-model="filters.category">
                  <option value="all">{{ $t('allCategories') }}</option>
                  <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                    {{ $t(cat.nameKey) }}
                  </option>
                </select>
              </div>

              <!-- Price Filter (Only for products) -->
              <div v-if="filters.type === 'product' || filters.type === 'all'" class="filter-group mb-4">
                <label class="form-label font-weight-bold mb-3">{{ $t('priceRange') || 'نطاق السعر' }}</label>
                <div class="d-flex align-items-center gap-2">
                  <input type="number" class="form-control form-control-sm border-0 bg-light" placeholder="0" v-model="filters.minPrice">
                  <span>-</span>
                  <input type="number" class="form-control form-control-sm border-0 bg-light" placeholder="50000" v-model="filters.maxPrice">
                </div>
              </div>

              <button class="btn btn-outline-gold w-100 mt-3" @click="resetFilters">
                <i class="fa-solid fa-undo me-2"></i> {{ $t('resetFilters') || 'إعادة تعيين' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Search Results Area -->
        <div class="col-lg-9">
          <div class="search-content">
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-gold" role="status">
                <span class="visually-hidden">{{ $t('loading') }}</span>
              </div>
              <p class="mt-3 text-muted">{{ $t('searchingAcrossSources') || 'جاري البحث في جميع المصادر...' }}</p>
            </div>

            <!-- Empty State -->
            <div v-else-if="results.length === 0" class="text-center py-5 card border-0 shadow-sm">
              <div class="card-body">
                <i class="fa-solid fa-search-minus fa-5x text-muted opacity-25 mb-4"></i>
                <h3>{{ $t('noResultsFound') || 'لم يتم العثور على نتائج' }}</h3>
                <p class="text-muted">{{ $t('tryAdjustingFilters') || 'جرب تغيير الكلمات المفتاحية أو تعديل الفلاتر' }}</p>
                <button class="btn btn-gold mt-3" @click="resetFilters">{{ $t('resetSearch') || 'بحث جديد' }}</button>
              </div>
            </div>

            <!-- Results List -->
            <div v-else>
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="mb-0">
                  {{ $t('foundResultsCount') || 'نتائج البحث:' }} 
                  <span class="text-gold">{{ totalResults }}</span>
                </h5>
                <div class="results-source-info small text-muted">
                  <span class="badge bg-light text-dark border me-2">ERPNext</span>
                  <span class="badge bg-light text-dark border me-2">Blogger</span>
                  <span class="badge bg-light text-dark border">Gallery</span>
                </div>
              </div>

              <div class="row g-4">
                <div v-for="item in results" :key="item.type + '-' + item.id" class="col-md-6 col-xl-4">
                  <!-- Result Card -->
                  <div class="result-card card h-100 shadow-sm border-0 overflow-hidden transition-hover">
                    <div class="position-relative">
                      <img :src="item.image" :alt="item.title" class="card-img-top" style="height: 200px; object-fit: cover;">
                      <span :class="['type-badge badge', item.type]">
                        {{ item.type === 'product' ? 'منتج' : item.type === 'article' ? 'مقال' : 'تصميم' }}
                      </span>
                    </div>
                    <div class="card-body d-flex flex-direction-column">
                      <div class="mb-2">
                        <small class="text-gold font-weight-bold">{{ item.category }}</small>
                      </div>
                      <h6 class="card-title mb-3 line-clamp-2">{{ item.title }}</h6>
                      
                      <div v-if="item.type === 'product'" class="mt-auto">
                        <div class="h5 text-dark mb-3">{{ item.price }} د.ج</div>
                        <router-link :to="item.link" class="btn btn-gold btn-sm w-100">
                          {{ $t('viewDetails') }}
                        </router-link>
                      </div>
                      <div v-else class="mt-auto">
                        <p v-if="item.summary" class="small text-muted line-clamp-2 mb-3">{{ item.summary }}</p>
                        <a v-if="item.type === 'article'" :href="item.link" target="_blank" class="btn btn-outline-gold btn-sm w-100">
                          {{ $t('readMore') || 'اقرأ المزيد' }}
                        </a>
                        <router-link v-else :to="item.link" class="btn btn-outline-gold btn-sm w-100">
                          {{ $t('viewInGallery') || 'عرض في المعرض' }}
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Pagination -->
              <div v-if="totalPages > 1" class="d-flex justify-content-center mt-5">
                <nav>
                  <ul class="pagination pagination-lg">
                    <li class="page-item" :class="{ disabled: filters.page === 1 }">
                      <button class="page-link border-0 shadow-sm rounded-circle mx-1" @click="changePage(filters.page - 1)">
                        <i class="fa-solid fa-chevron-right"></i>
                      </button>
                    </li>
                    <li v-for="p in totalPages" :key="p" class="page-item" :class="{ active: filters.page === p }">
                      <button class="page-link border-0 shadow-sm rounded-circle mx-1" @click="changePage(p)">
                        {{ p }}
                      </button>
                    </li>
                    <li class="page-item" :class="{ disabled: filters.page === totalPages }">
                      <button class="page-link border-0 shadow-sm rounded-circle mx-1" @click="changePage(filters.page + 1)">
                        <i class="fa-solid fa-chevron-left"></i>
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import SearchService from '@/integration/services/SearchService';

const route = useRoute();
const router = useRouter();

// State
const results = ref([]);
const totalResults = ref(0);
const totalPages = ref(1);
const loading = ref(false);

const filters = reactive({
  query: route.query.q || '',
  type: route.query.type || 'all',
  category: route.query.category || 'all',
  minPrice: route.query.minPrice || null,
  maxPrice: route.query.maxPrice || null,
  page: parseInt(route.query.page) || 1,
  limit: 12
});

const categories = [
  { value: 'furniture', nameKey: 'furniture' },
  { value: 'doors', nameKey: 'doors' },
  { value: 'walls', nameKey: 'walls' },
  { value: 'ceilings', nameKey: 'ceilings' },
  { value: 'tiles', nameKey: 'tiles' },
  { value: 'kitchens', nameKey: 'kitchens' },
  { value: 'cars', nameKey: 'cars' },
];

// Methods
const handleSearch = async () => {
  loading.value = true;
  try {
    const response = await SearchService.globalSearch({ ...filters });
    results.value = response.results;
    totalResults.value = response.total;
    totalPages.value = response.totalPages;
  } catch (error) {
    console.error('Error during global search:', error);
  } finally {
    loading.value = false;
    updateURL();
  }
};

const updateURL = () => {
  const query = { ...filters };
  // Remove empty or default values
  Object.keys(query).forEach(key => {
    if (!query[key] || query[key] === 'all') delete query[key];
  });
  
  router.push({ query });
};

const changePage = (p) => {
  if (p < 1 || p > totalPages.value) return;
  filters.page = p;
  handleSearch();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const resetFilters = () => {
  filters.query = '';
  filters.type = 'all';
  filters.category = 'all';
  filters.minPrice = null;
  filters.maxPrice = null;
  filters.page = 1;
  handleSearch();
};

// Watchers
watch(() => filters.type, () => { filters.page = 1; handleSearch(); });
watch(() => filters.category, () => { filters.page = 1; handleSearch(); });

// Lifecycle
onMounted(() => {
  if (filters.query || filters.type !== 'all' || filters.category !== 'all') {
    handleSearch();
  }
});
</script>

<style scoped>
.search-page {
  background-color: #fbfbfb;
  min-height: 100vh;
}

.text-gold {
  color: #d4af37;
}

.search-bar {
  background: white;
  padding: 5px;
}

.btn-gold {
  background: linear-gradient(135deg, #d4af37 0%, #f1d592 100%);
  color: #1a1a2e;
  font-weight: 600;
  border: none;
}

.btn-outline-gold {
  color: #d4af37;
  border: 1.5px solid #d4af37;
}

.btn-outline-gold:hover {
  background: var(--gold-gradient);
  color: #1a1a2e;
}

.btn-outline-light-gold {
  border: 1px solid transparent;
  color: #666;
}

.btn-outline-light-gold:hover {
  background: rgba(212, 175, 55, 0.05);
  color: #d4af37;
}

.btn-check:checked + .btn-outline-light-gold {
  background: rgba(212, 175, 55, 0.1);
  border-color: #d4af37;
  color: #d4af37;
  font-weight: bold;
}

.result-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}

.type-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 8px 12px;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.75rem;
  z-index: 1;
}

.type-badge.product { background: #d4af37; color: white; }
.type-badge.article { background: #1a1a2e; color: white; }
.type-badge.design { background: #28a745; color: white; }

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination .page-link {
  color: #666;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination .active .page-link {
  background: var(--gold-gradient);
  color: #1a1a2e;
  font-weight: bold;
}

.page-item.disabled .page-link {
  opacity: 0.5;
}

.sticky-top {
  z-index: 100;
}
</style>
