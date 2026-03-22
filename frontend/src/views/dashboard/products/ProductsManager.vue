<template>
  <div class="products-manager">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <h1>إدارة المنتجات</h1>
        <p>إدارة وتحديث مخزون تصاميم الفينيل والرخام</p>
      </div>
      <div class="header-actions">
        <button class="btn-sync" :disabled="syncProgress > 0" @click="$emit('sync')">
          <i class="fa-solid fa-sync-alt" :class="{ 'fa-spin': syncProgress > 0 }"></i>
          {{ syncProgress > 0 ? `مزامنة (${syncProgress}%)` : 'مزامنة مع ERPNext' }}
        </button>
        <button class="btn-primary" @click="openNewProductModal">
          <i class="fa-solid fa-plus"></i> إضافة منتج
        </button>
      </div>
    </header>

    <!-- Stats -->
    <StatCards :stats="productStats" />

    <!-- Filters & Search -->
    <ProductFilters
      v-model:search-query="searchQuery"
      v-model:category-filter="categoryFilter"
      v-model:stock-filter="stockFilter"
      v-model:view-mode="viewMode"
      :categories="categories"
      @update:search-query="debouncedSearch"
      @clear-search="clearSearch"
    />

    <!-- Products Content -->
    <div v-if="viewMode === 'table'">
      <ProductsTable
        :products="paginatedProducts"
        :sort-key="sortKey"
        :sort-order="sortOrder"
        @sort="handleSort"
        @view="viewProduct"
        @edit="editProduct"
        @delete="confirmDelete"
      />
    </div>

    <div v-else class="products-grid">
      <ProductCard
        v-for="product in paginatedProducts"
        :key="product.id"
        :product="product"
        :category-label="getCategoryLabel(product.category)"
        @view="viewProduct"
        @edit="editProduct"
        @delete="confirmDelete"
      />
    </div>

    <!-- Pagination -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:items-per-page="itemsPerPage"
      :total-items="filteredProducts.length"
    />

    <!-- Modals -->
    <DeleteProductModal
      :show="showDeleteModal"
      :product-name="productToDelete?.name"
      @close="showDeleteModal = false"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { debounce } from 'lodash';
import DashboardService from '@/services/DashboardService';
import AIService from '@/services/AIService';
import ERPNextService from '@/services/ERPNextService';
import StatCards from '@/components/common/StatCards.vue';
import Pagination from '@/components/common/Pagination.vue';
import ProductsTable from './components/ProductsTable.vue';
import ProductCard from './components/ProductCard.vue';
import ProductFilters from './components/ProductFilters.vue';
import DeleteProductModal from './components/DeleteProductModal.vue';
import CurrencyService from '@/integration/services/CurrencyService';

const store = useStore();

// State
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const categoryFilter = ref('');
const stockFilter = ref('');
const viewMode = ref('grid');
const sortKey = ref('name');
const sortOrder = ref('asc');
const currentPage = ref(1);
const itemsPerPage = ref(9);
const showDeleteModal = ref(false);
const productToDelete = ref(null);
const products = ref([]);
const syncProgress = ref(0);

const categories = [
  { value: 'furniture', label: 'أثاث' },
  { value: 'doors', label: 'أبواب' },
  { value: 'walls', label: 'جدران' },
  { value: 'ceilings', label: 'أسقف' },
  { value: 'tiles', label: 'بلاط' },
  { value: 'kitchens', label: 'مطابخ' },
  { value: 'cars', label: 'سيارات' },
];

// Methods
const fetchProducts = async () => {
  try {
    loading.value = true;
    error.value = null;

    const filters = {
      search: searchQuery.value,
      category: categoryFilter.value,
      stock_status: stockFilter.value,
      page: currentPage.value,
      limit: itemsPerPage.value,
      sort: sortKey.value,
      order: sortOrder.value
    };

    const response = await DashboardService.getProducts(filters);
    products.value = response.products || [];
    
    console.log('Products loaded:', response);
  } catch (err) {
    console.error('Error fetching products:', err);
    error.value = 'فشل في تحميل المنتجات';
  } finally {
    loading.value = false;
  }
};

const createProduct = async (productData) => {
  try {
    // Generate AI-powered description if not provided
    if (!productData.description) {
      const aiDescription = await AIService.generateProductDescription(
        productData.name,
        productData.category
      );
      productData.description = aiDescription.description;
    }

    const newProduct = await DashboardService.createProduct(productData);
    products.value.unshift(newProduct);
    
    // Sync with ERPNext
    await ERPNextService.syncProduct(newProduct.id);
    
    console.log('Product created successfully:', newProduct);
    return newProduct;
  } catch (err) {
    console.error('Error creating product:', err);
    throw err;
  }
};

const updateProduct = async (productId, productData) => {
  try {
    const updatedProduct = await DashboardService.updateProduct(productId, productData);
    
    const index = products.value.findIndex(p => p.id === productId);
    if (index !== -1) {
      products.value[index] = updatedProduct;
    }
    
    // Sync with ERPNext
    await ERPNextService.syncProduct(productId);
    
    console.log('Product updated successfully:', updatedProduct);
    return updatedProduct;
  } catch (err) {
    console.error('Error updating product:', err);
    throw err;
  }
};

const deleteProduct = async (productId) => {
  try {
    await DashboardService.deleteProduct(productId);
    products.value = products.value.filter(p => p.id !== productId);
    
    // Sync deletion with ERPNext
    await ERPNextService.syncToERPNext('product_deletions', {
      productId,
      timestamp: new Date().toISOString()
    });
    
    console.log('Product deleted successfully:', productId);
  } catch (err) {
    console.error('Error deleting product:', err);
    throw err;
  }
};

const syncAllProducts = async () => {
  try {
    syncProgress.value = 0;
    
    // Start ERPNext sync
    await ERPNextService.migrateProducts();
    
    // Monitor sync progress
    const checkProgress = async () => {
      const status = await ERPNextService.getProductSyncStatus();
      syncProgress.value = status.progress || 0;
      
      if (status.completed) {
        await fetchProducts(); // Refresh products list
        return;
      }
      
      setTimeout(checkProgress, 2000); // Check again in 2 seconds
    };
    
    checkProgress();
  } catch (err) {
    console.error('Error syncing products:', err);
  }
};

const optimizePricing = async (productId) => {
  try {
    const recommendations = await AIService.getPricingRecommendations(productId);
    console.log('Pricing recommendations:', recommendations);
    return recommendations;
  } catch (err) {
    console.error('Error getting pricing recommendations:', err);
    return null;
  }
};

const generateProductImage = async (productName, category) => {
  try {
    const imageGeneration = await AIService.generateProductImage(
      `${productName} ${category} design`,
      'realistic'
    );
    return imageGeneration.imageUrl;
  } catch (err) {
    console.error('Error generating product image:', err);
    return null;
  }
};

const debouncedFetch = debounce(fetchProducts, 500);

// Computed
const lowStockProducts = computed(() => 
  products.value.filter(p => p.stock > 0 && p.stock <= 10)
);

const productStats = computed(() => [
  { label: 'إجمالي المنتجات', value: products.value.length, icon: 'fa-solid fa-box', color: '#d4af37', trend: 12 },
  { label: 'نشط الآن', value: products.value.filter(p => p.active).length, icon: 'fa-solid fa-check-circle', color: '#4caf50', trend: 5 },
  { label: 'مخزون منخفض', value: lowStockProducts.value.length, icon: 'fa-solid fa-exclamation-triangle', color: '#ff9800', trend: -2 },
  { label: 'خارج المخزون', value: products.value.filter(p => p.stock === 0).length, icon: 'fa-solid fa-times-circle', color: '#f44336', trend: 0 }
]);

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchesSearch = !searchQuery.value || p.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCategory = !categoryFilter.value || p.category === categoryFilter.value;
    const matchesStock = !stockFilter.value || (
      stockFilter.value === 'in-stock' ? p.stock > 10 :
      stockFilter.value === 'low-stock' ? (p.stock > 0 && p.stock <= 10) :
      p.stock === 0
    );
    return matchesSearch && matchesCategory && matchesStock;
  });
});

const sortedProducts = computed(() => {
  const sorted = [...filteredProducts.value];
  sorted.sort((a, b) => {
    const aVal = a[sortKey.value];
    const bVal = b[sortKey.value];
    if (typeof aVal === 'number') return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal;
    return sortOrder.value === 'asc' ? String(aVal).localeCompare(String(bVal)) : String(bVal).localeCompare(String(aVal));
  });
  return sorted;
});

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return sortedProducts.value.slice(start, start + itemsPerPage.value);
});

// Methods
const formatAmount = (val) => CurrencyService.formatAmount(val);
const getCategoryLabel = (val) => categories.find(c => c.value === val)?.label || val;
const getStockClass = (stock) => stock === 0 ? 'out' : (stock <= 10 ? 'low' : 'in');

const debouncedSearch = debounce(() => { currentPage.value = 1; }, 300);
const clearSearch = () => { searchQuery.value = ''; currentPage.value = 1; };

const handleSort = (key) => {
  if (sortKey.value === key) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  else { sortKey.value = key; sortOrder.value = 'asc'; }
};

const viewProduct = (p) => console.log('View', p);
const editProduct = (p) => console.log('Edit', p);
const confirmDelete = (p) => { productToDelete.value = p; showDeleteModal.value = true; };
const handleDelete = async () => {
  if (productToDelete.value) {
    await store.dispatch('products/deleteProduct', productToDelete.value.id);
    showDeleteModal.value = false;
  }
};

const openNewProductModal = () => console.log('New Product');

onMounted(() => {
  store.dispatch('products/fetchProducts');
});
</script>

<style scoped>
.products-manager { padding: 24px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.header-content h1 { font-size: 24px; font-weight: 700; color: #1a1a2e; margin: 0; }
.header-actions { display: flex; gap: 12px; }

.btn-primary, .btn-sync {
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-primary { background: var(--gold-gradient); border: none; color: #1a1a2e; }
.btn-sync { background: white; border: 1px solid #dee2e6; color: #1a1a2e; }

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-container { background: white; padding: 24px; border-radius: 16px; width: 90%; max-width: 400px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; }

.btn-secondary { padding: 8px 16px; border-radius: 8px; border: 1px solid #ddd; background: white; cursor: pointer; }
.btn-danger { padding: 8px 16px; border-radius: 8px; border: none; background: #f44336; color: white; cursor: pointer; }
</style>
