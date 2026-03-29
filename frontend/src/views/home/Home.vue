<template>
  <div>
    <!-- Error Boundary Wrapper -->
    <div v-if="hasCriticalError" class="error-boundary">
      <div class="alert alert-danger text-center m-4">
        <i class="fa-solid fa-exclamation-triangle me-2"></i>
        {{ $t('pageLoadError') || 'حدث خطأ أثناء تحميل الصفحة' }}
        <button @click="retryLoading" class="btn btn-primary btn-sm ms-2">
          {{ $t('retry') || 'إعادة المحاولة' }}
        </button>
      </div>
    </div>

    <div v-else>
      <!-- Hero Slider -->
      <HeroSlider />

      <div class="container">
        <!-- Featured Products Section -->
        <div class="section-header mt-5">
          <h2 class="section-title">{{ $t('featuredProducts') || 'منتجات مميزة' }}</h2>
          <router-link to="/shop" class="view-all">
            {{ $t('viewAll') }}
            <i :class="`fa-solid fa-arrow-${directionIcon}`"></i>
          </router-link>
        </div>

      <!-- Products Loading Skeleton -->
      <div v-if="loadingProducts" class="row g-4">
        <div v-for="i in 4" :key="i" class="col-6 col-md-3">
          <div class="card border-0 bg-card rounded-lg overflow-hidden">
            <LoadingSkeleton type="image" height="200px" />
            <div class="card-body">
              <LoadingSkeleton type="text" height="20px" class="mb-2" />
              <LoadingSkeleton type="text" height="16px" width="80%" />
            </div>
          </div>
        </div>
      </div>

      <!-- Products Error -->
      <div v-else-if="productsError" class="alert alert-danger text-center">
        <i class="fa-solid fa-exclamation-triangle me-2"></i>
        {{ productsError }}
      </div>

      <!-- Featured Products Grid -->
      <div v-else class="row g-4">
        <div v-for="(product, index) in featuredProducts" :key="product.id" class="col-6 col-md-3">
          <ProductCard 
            :product="product"
            @add-to-cart="handleAddToCart"
            @toggle-favorite="handleToggleFavorite"
            :is-new="index === 0"
          />
        </div>
      </div>

      <!-- Blog Section -->
      <div class="section-header mt-5">
        <h2 class="section-title">{{ $t('latestBlog') || 'أحدث المدونات' }}</h2>
        <router-link to="/blog" class="view-all">
          {{ $t('viewAll') }}
          <i :class="`fa-solid fa-arrow-${directionIcon}`"></i>
        </router-link>
      </div>

      <!-- Blog Loading Skeleton -->
      <div v-if="loadingPosts" class="row g-4">
        <div v-for="i in 4" :key="i" class="col-6 col-md-3">
          <div class="card border-0 bg-card rounded-lg overflow-hidden">
            <LoadingSkeleton type="image" height="150px" />
            <div class="card-body">
              <LoadingSkeleton type="text" height="20px" class="mb-2" />
              <LoadingSkeleton type="text" height="14px" width="90%" />
            </div>
          </div>
        </div>
      </div>

      <!-- Blog Error -->
      <div v-else-if="postsError" class="alert alert-warning text-center">
        <i class="fa-solid fa-exclamation-triangle me-2"></i>
        {{ postsError }}
      </div>

      <!-- Blog Posts Grid -->
      <div v-else class="row g-4">
        <div v-for="post in posts" :key="post.id" class="col-6 col-md-3">
          <div class="card border-0 bg-card rounded-lg overflow-hidden h-100">
            <img :src="post.image" class="card-img-top" :alt="post.title" />
            <div class="card-body">
              <h5 class="card-title">{{ post.title }}</h5>
              <p class="card-text text-muted">{{ post.excerpt }}</p>
              <router-link :to="`/blog/${post.slug}`" class="btn btn-outline-primary btn-sm">
                {{ $t('readMore') || 'اقرأ المزيد' }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Section -->
    <ContactForm />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onErrorCaptured } from 'vue';
import { useI18n } from 'vue-i18n';
import { useStore } from 'vuex';
import HeroSlider from '@/components/HeroSlider.vue';
import ContactForm from '@/components/common/ContactForm.vue';
import ProductCard from '@/components/ProductCard.vue';
import LoadingSkeleton from '@/components/LoadingSkeleton.vue';
import BlogService from '@/integration/services/BlogService';
import { useProducts } from '@/composables/useGraphQL';

const { t, locale } = useI18n();
const store = useStore();

// Error boundary state
const hasCriticalError = ref(false);
const errorDetails = ref(null);

// Capture errors from child components
onErrorCaptured((error, instance, info) => {
  console.error('Home.vue Error Boundary:', error, info);
  hasCriticalError.value = true;
  errorDetails.value = { error: error.message, info };
  
  // Prevent error from propagating further
  return false;
});

// GraphQL Products Hook with error handling - Initialize only once
let productsData;
let isProductsInitialized = false;

const initializeProducts = () => {
  if (isProductsInitialized) {
    return productsData;
  }
  
  try {
    productsData = useProducts();
    isProductsInitialized = true;
    console.log('✅ Products composable initialized');
  } catch (error) {
    console.error('Error initializing useProducts:', error);
    productsData = {
      products: ref([]),
      loading: ref(false),
      error: ref(error.message),
      fetchProducts: async () => {}
    };
    isProductsInitialized = true;
  }
  
  return productsData;
};

const { products: featuredProducts, loading: loadingProducts, error: productsError, fetchProducts } = initializeProducts();

// Posts State (keep BlogService as is)
const posts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(null);

const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
const directionIcon = computed(() => (locale.value === 'ar' ? 'left' : 'right'));

const handleAddToCart = (product) => {
  if (!isAuthenticated.value) {
    router.push('/login');
    return;
  }
  
  const item = {
    id: product.id,
    title: product.title,
    price: product.price,
    image: product.image,
    quantity: 1
  };
  
  store.dispatch('cart/addToCart', item);
  
  // Show success message
  store.dispatch('notifications/showNotification', {
    type: 'success',
    message: `${product.title} ${t('addedToCart') || 'تمت إضافته إلى السلة'}`
  });
};

const handleToggleFavorite = ({ productId }) => {
  if (!isAuthenticated.value) {
    router.push('/login');
    return;
  }
  
  const product = featuredProducts.value.find(p => p.id === productId);
  if (product) {
    store.dispatch('wishlist/toggleWishlist', product);
  }
};

// Retry function for error recovery
const retryLoading = () => {
  hasCriticalError.value = false;
  errorDetails.value = null;
  
  // Re-trigger fetch without reinitializing the composable
  try {
    console.log('🔄 Retrying products fetch...');
    fetchFeaturedProducts();
  } catch (error) {
    console.error('Retry failed:', error);
    hasCriticalError.value = true;
    errorDetails.value = { error: error.message, info: 'retry_failed' };
  }
};

const fetchLatestPosts = async () => {
  // Prevent duplicate requests
  if (loadingPosts.value) {
    console.log('⏳ Posts fetch already in progress, skipping...');
    return;
  }
  
  loadingPosts.value = true;
  postsError.value = null;
  try {
    posts.value = await BlogService.getLatestPosts(4);
  } catch (err) {
    postsError.value = err.message;
  } finally {
    loadingPosts.value = false;
  }
};

const fetchFeaturedProducts = async () => {
  // Prevent duplicate requests
  if (loadingProducts.value) {
    console.log('⏳ Products fetch already in progress, skipping...');
    return;
  }
  
  // Use the composable correctly - no parameters for featured products
  try {
    // useProducts() will automatically fetch all products (no category filter)
    const productsResult = await fetchProducts();
    console.log('✅ Featured products fetched via GraphQL');
  } catch (error) {
    console.error('❌ Error fetching featured products:', error);
    productsError.value = error.message;
  }
};

// Fetch data on mount - SIMPLIFIED
onMounted(() => {
  // useProducts composable already handles automatic fetching
  // No need for manual fetchFeaturedProducts call
  fetchLatestPosts(); // Only fetch posts manually
});
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
  margin: 0;
}

.view-all {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.3s ease;
}

.view-all:hover {
  color: var(--primary-hover);
}

.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.card-text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-muted);
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.alert-danger {
  background-color: #fee;
  border-color: #fcc;
  color: #721c24;
}

.alert-warning {
  background-color: #fff3cd;
  border-color: #ffeaa7;
  color: #856404;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .view-all {
    align-self: flex-end;
  }
}
</style>
