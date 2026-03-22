<template>
  <div>
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
            <div class="p-3">
              <LoadingSkeleton type="text" width="80%" />
              <LoadingSkeleton type="text" width="40%" />
            </div>
          </div>
        </div>
      </div>

      <!-- Products Error State -->
      <div v-else-if="productsError" class="text-center py-5">
        <p class="text-danger">{{ productsError }}</p>
        <button class="btn btn-outline-gold btn-sm" @click="fetchFeaturedProducts">
          <i class="fa-solid fa-sync-alt me-2"></i> {{ $t('retry') }}
        </button>
      </div>

      <!-- Products Grid -->
      <div v-else class="vinyl-products-grid featured-products mb-5">
        <ProductCard 
          v-for="product in featuredProducts" 
          :key="product.id" 
          :product="product"
          @add-to-cart="handleAddToCart"
          @toggle-favorite="handleToggleFavorite"
        />
        <div v-if="featuredProducts.length === 0" class="col-12 text-center py-5 opacity-50">
          <p>{{ $t('noProductsFound') || 'لا توجد منتجات حالياً' }}</p>
        </div>
      </div>

      <!-- Posts Section -->
      <div class="section-header mt-5">
        <h2 class="section-title">{{ $t('latestArticles') }}</h2>
        <router-link to="/blog" class="view-all">
          {{ $t('viewAll') }}
          <i :class="`fa-solid fa-arrow-${directionIcon}`"></i>
        </router-link>
      </div>

      <!-- Blog Loading Skeleton -->
      <div v-if="loadingPosts" class="row g-4">
        <div v-for="i in 4" :key="i" class="col-md-6 col-lg-3">
          <div class="card border-0 bg-card rounded-lg overflow-hidden">
            <LoadingSkeleton type="image" height="180px" />
            <div class="p-3">
              <LoadingSkeleton type="text" width="90%" />
              <LoadingSkeleton type="text" width="60%" />
            </div>
          </div>
        </div>
      </div>

      <!-- Blog Error State -->
      <div v-else-if="postsError" class="text-center py-5">
        <p class="text-danger">{{ postsError }}</p>
        <button class="btn btn-outline-gold btn-sm" @click="fetchLatestPosts">
          <i class="fa-solid fa-sync-alt me-2"></i> {{ $t('retry') }}
        </button>
      </div>

      <!-- Posts Grid -->
      <div v-else class="vinyl-products-grid mb-5">
        <article v-for="post in posts" :key="post.id" class="w-100">
          <div class="vinyl-product-card h-100">
            <div class="product-image">
              <a :href="post.link" target="_blank">
                <img :src="post.image" :alt="post.title" loading="lazy" />
              </a>
              <span class="product-badge">{{ $t('new') }}</span>
            </div>

            <div class="product-info">
              <h3 class="product-title h6 mb-2">
                <a :href="post.link" target="_blank" class="text-decoration-none">
                  {{ post.translations?.[locale]?.title || post.title }}
                </a>
              </h3>

              <div class="post-meta mb-2">
                <span class="post-date small">
                  <i class="far fa-calendar-alt me-1"></i>
                  {{ formatDate(post.published) }}
                </span>
              </div>

              <p class="product-excerpt small text-muted mb-3">
                {{ post.translations?.[locale]?.summary || post.summary }}
              </p>

              <div class="product-actions mt-auto">
                <a class="btn-view w-100 py-2" :href="post.link" target="_blank">
                  <i class="fa-solid fa-eye me-2"></i>
                  <span>{{ $t('readMore') }}</span>
                </a>
              </div>
            </div>
          </div>
        </article>
        <div v-if="posts.length === 0" class="col-12 text-center py-5 opacity-50">
          <p>{{ $t('noArticlesFound') || 'لا توجد مقالات حالياً' }}</p>
        </div>
      </div>

      <!-- Contact & Map Section -->
      <div class="contact-map-section mt-5">
        <div class="section-header">
          <h2 class="section-title">{{ $t('sendMessage') }}</h2>
        </div>

        <div class="contact-map-grid">
          <!-- Contact Form Column -->
          <ContactForm />

          <!-- Map Column -->
          <div class="map-column">
            <div class="map-card">
              <h3 class="map-title">
                <i class="fa-solid fa-map-marker-alt"></i>
                {{ $t('visitUs') }}
              </h3>
              <div class="map-container">
                <iframe
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d13374.981897722519!2d5.172593343991056!3d36.33623060243317!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12f32e2e76af0f63%3A0x123a8ef4c7f02763!2zQcOvbiBSb3Vh!5e1!3m2!1sen!2sdz!4v1773563421474!5m2!1sen!2sdz"
                  allowfullscreen
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                >
                </iframe>
              </div>

              <div class="contact-info-below">
                <div class="info-item">
                  <i class="fa-solid fa-phone-alt"></i>
                  <div>
                    <h4>{{ $t('phone') }}</h4>
                    <a href="tel:0663140341">0663140341</a>
                  </div>
                </div>
                <div class="info-item">
                  <i class="fa-solid fa-envelope"></i>
                  <div>
                    <h4>{{ $t('email') }}</h4>
                    <a href="mailto:remadnamansour7@gmail.com">remadnamansour7@gmail.com</a>
                  </div>
                </div>
                <div class="info-item">
                  <i class="fab fa-whatsapp"></i>
                  <div>
                    <h4>{{ $t('whatsapp') }}</h4>
                    <a href="https://wa.me/213663140341" target="_blank">0663140341</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useStore } from 'vuex';
import HeroSlider from '@/components/HeroSlider.vue';
import ContactForm from '@/components/common/ContactForm.vue';
import ProductCard from '@/components/ProductCard.vue';
import LoadingSkeleton from '@/components/LoadingSkeleton.vue';
import BlogService from '@/integration/services/BlogService';
import ERPNextService from '@/integration/services/ERPNextService';

const { t, locale } = useI18n();
const store = useStore();

// Posts State
const posts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(null);

// Products State
const featuredProducts = ref([]);
const loadingProducts = ref(true);
const productsError = ref(null);

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
    quantity: 1,
    options: {
      width: 100, // مقاس افتراضي
      height: 100
    }
  };
  
  store.dispatch('cart/addToCart', item);
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

const fetchLatestPosts = async () => {
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
  loadingProducts.value = true;
  productsError.value = null;
  try {
    const response = await ERPNextService.getProducts();
    if (response.success) {
      // نأخذ أول 4 منتجات كمنتجات مميزة
      featuredProducts.value = response.data.slice(0, 4).map((p, index) => {
        const fallbackImages = [
          'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800&auto=format&fit=crop',
          'https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=800&auto=format&fit=crop',
          'https://images.unsplash.com/photo-1505691938895-1758d7eaa511?q=80&w=800&auto=format&fit=crop',
          'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?q=80&w=800&auto=format&fit=crop'
        ];
        
        return {
          id: p.item_code,
          title: p.item_name,
          price: p.standard_rate || 2500,
          originalPrice: (p.standard_rate || 2500) * 1.2,
          discount: 20,
          onSale: index % 2 === 0,
          image: p.image || fallbackImages[index % 4],
          category: p.item_group,
          categoryKey: p.item_group?.toLowerCase() || 'general',
          categoryIcon: 'fa-tag',
          excerpt: p.description || 'تصميم فينيل مخصص عالي الجودة لمساحتك العصرية.',
          translations: {
            ar: {
              title: p.item_name,
              excerpt: p.description || 'تصميم فينيل مخصص عالي الجودة لمساحتك العصرية.'
            },
            en: {
              title: p.item_name_en || p.item_name, // ERPNext often uses separate fields for translations
              excerpt: p.description_en || 'High-quality custom vinyl design for your modern space.'
            },
            fr: {
              title: p.item_name_fr || p.item_name,
              excerpt: p.description_fr || 'Design en vinyle personnalisé de haute qualité pour votre espace moderne.'
            }
          },
          minSize: '100',
          maxSize: '300',
          isNew: index === 0
        };
      });
    } else {
      throw new Error(response.message);
    }
  } catch (err) {
    productsError.value = err.message;
  } finally {
    loadingProducts.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString(locale.value, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

onMounted(() => {
  fetchLatestPosts();
  fetchFeaturedProducts();
});
</script>

<style scoped>
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 30px 0 20px;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  padding-right: 12px;
}

[dir='ltr'] .section-title {
  padding-right: 0;
  padding-left: 12px;
}

.section-title::before {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  width: 3px;
  height: 24px;
  background: var(--gold-gradient);
  transform: translateY(-50%);
}

[dir='ltr'] .section-title::before {
  right: auto;
  left: 0;
}

.view-all {
  color: var(--gold-primary);
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  font-size: 0.9rem;
  white-space: nowrap;
  text-decoration: none;
}

.vinyl-products-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.vinyl-product-card {
  background: var(--bg-card);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s;
  border: 1px solid var(--border-subtle);
  width: 100%;
}

.vinyl-product-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.product-image {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.vinyl-product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  z-index: 2;
}

.product-info {
  padding: 15px;
}

.product-category {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--gold-primary);
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.product-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 10px;
  line-height: 1.4;
}

.product-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color 0.3s;
}

.product-title a:hover {
  color: var(--gold-primary);
}

.post-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
  font-size: 0.75rem;
  color: var(--text-dim);
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.product-excerpt {
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-actions {
  display: flex;
  gap: 10px;
}

.btn-view {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border-radius: 10px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s;
  border: 1px solid var(--border-subtle);
}

.btn-view:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.load-more-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 30px;
  border-radius: 30px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.load-more-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: scale(1.05);
  box-shadow: var(--shadow-gold);
}

.blog-pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding: 20px;
  background: var(--bg-card);
  border-radius: 16px;
  border: 1px solid var(--border-subtle);
}

.blog-pager-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 10px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.blog-pager-btn:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.page-info {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--gold-primary);
}

.contact-map-section {
  margin-top: 60px;
  margin-bottom: 60px;
}

.contact-map-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}

@media (min-width: 992px) {
  .contact-map-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (min-width: 768px) {
  .vinyl-products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
}

@media (min-width: 1024px) {
  .vinyl-products-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
  }
}

@media (min-width: 1400px) {
  .vinyl-products-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
  }
}

.featured-products {
  padding-bottom: 20px;
}

.featured-products :deep(.product-card) {
  height: 100%;
  max-width: 100%;
}

@media (min-width: 1400px) {
  .container {
    max-width: 1320px;
  }
}

.section-header {
  margin-top: 60px !important;
  margin-bottom: 30px !important;
}

.contact-form-card,
.map-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 25px;
  border: 1px solid var(--border-subtle);
  height: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

@media (min-width: 768px) {
  .form-row {
    grid-template-columns: 1fr 1fr;
  }
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--gold-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--gold-primary);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-status {
  margin-top: 20px;
  padding: 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  font-weight: 600;
}

.form-status.success {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.form-status.error {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.map-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--gold-primary);
}

.map-container {
  height: 300px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 20px;
}

.map-container iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.contact-info-below {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  border-radius: 12px;
  background: var(--bg-secondary);
}

.info-item i {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.info-item h4 {
  font-size: 0.8rem;
  color: var(--text-dim);
  margin: 0;
}

.info-item a {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.info-item a:hover {
  color: var(--gold-primary);
}
</style>
