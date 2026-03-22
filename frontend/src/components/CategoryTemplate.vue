<template>
  <div class="category-page">
    <div class="container">
      <!-- ===== الهيدر الرئيسي ===== -->
      <div class="page-header text-center py-5">
        <h1 class="display-4">
          <i :class="icon" class="text-gold"></i>
          {{ $t(titleKey) }}
        </h1>
        <p class="lead text-muted">{{ $t(descriptionKey) }}</p>
      </div>

      <!-- ===== أقسام فرعية (اختياري) ===== -->
      <div v-if="subCategories && subCategories.length" class="sub-categories row g-4 mb-5">
        <div v-for="sub in subCategories" :key="sub.id" class="col-md-4">
          <div
            class="card h-100 shadow-sm border-0 rounded-lg hover-lift"
            @click="navigateTo(sub.link)"
          >
            <div class="card-body text-center">
              <div class="fs-1 mb-3">{{ sub.emoji }}</div>
              <h3 class="h5 card-title">{{ $t(sub.titleKey) }}</h3>
              <p class="card-text small text-muted">{{ $t(sub.descKey) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== أحدث التصاميم ===== -->
      <div class="section-title d-flex justify-content-between align-items-center mb-4">
        <h2 class="h3">
          <i class="fa-solid fa-clock text-gold"></i>
          {{ $t(latestLabelKey) || $t('latestDesigns') }}
        </h2>
        <router-link :to="'/search?q=' + $t(labelKey)" class="text-gold text-decoration-none">
          {{ $t('viewAll') }} <i class="fa-solid fa-arrow-left ms-1"></i>
        </router-link>
      </div>

      <!-- شبكة المنتجات -->
      <div class="products-grid row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-5">
        <div v-if="loading" class="col-12 text-center py-5">
          <div class="spinner-border text-gold" role="status">
            <span class="visually-hidden">{{ $t('loading') }}</span>
          </div>
          <p class="mt-3 text-muted">{{ $t('loading') }}</p>
        </div>

        <div v-else-if="error" class="col-12 text-center py-5">
          <div class="alert alert-danger d-inline-block px-5">
            <i class="fa-solid fa-exclamation-circle me-2"></i>
            {{ errorMessage }}
            <button @click="fetchData" class="btn btn-sm btn-outline-danger ms-3">
              {{ $t('retry') || 'إعادة المحاولة' }}
            </button>
          </div>
        </div>

        <div v-else-if="products.length === 0" class="col-12 text-center py-5">
          <p class="text-muted fs-4">{{ $t('noDesignsFound') || 'لا توجد تصاميم متاحة حالياً' }}</p>
        </div>

        <template v-else>
          <div v-for="product in products" :key="product.id" class="col">
            <article class="product-card card h-100 shadow-sm border-0 rounded-lg overflow-hidden">
              <div class="product-image-container position-relative">
                <router-link :to="product.link">
                  <img
                    :src="product.image"
                    :alt="product.title"
                    class="card-img-top product-img"
                    loading="lazy"
                  />
                </router-link>
                <span class="badge bg-gold position-absolute top-0 end-0 m-3 shadow-sm">
                  {{ badgeLabel || $t('new') }}
                </span>
              </div>
              <div class="card-body">
                <h3 class="h5 card-title text-truncate">
                  <router-link :to="product.link" class="text-dark text-decoration-none">{{
                    product.title
                  }}</router-link>
                </h3>
                <p class="card-text text-muted small mb-3">{{ product.summary }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <router-link
                    :to="product.link"
                    class="btn btn-outline-dark btn-sm rounded-pill px-3"
                  >
                    <i class="fa-solid fa-eye me-1"></i> {{ $t('preview') }}
                  </router-link>
                  <a
                    :href="
                      'https://wa.me/213663140341?text=' +
                      encodeURIComponent($t('whatsappInquiry') + ': ' + product.title)
                    "
                    class="btn btn-success btn-sm rounded-pill px-3 shadow-sm"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <i class="fab fa-whatsapp me-1"></i> {{ $t('inquiry') }}
                  </a>
                </div>
              </div>
            </article>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import BlogService from '@/integration/services/BlogService';

const props = defineProps({
  icon: { type: String, required: true },
  titleKey: { type: String, required: true },
  descriptionKey: { type: String, required: true },
  labelKey: { type: String, required: true },
  latestLabelKey: { type: String, default: 'latestDesigns' },
  subCategories: { type: Array, default: () => [] },
  badgeLabel: { type: String, default: '' },
});

const router = useRouter();
const { t } = useI18n();
const products = ref([]);
const loading = ref(true);
const error = ref(false);
const errorMessage = ref('');

const fetchData = async () => {
  loading.value = true;
  error.value = false;
  try {
    const labels = {
      ar: t(props.labelKey, 'ar'),
      en: t(props.labelKey, 'en'),
    };
    products.value = await BlogService.getPostsByLabel(labels);
  } catch (err) {
    error.value = true;
    errorMessage.value = t('failedToLoadProducts') || 'فشل تحميل المنتجات. يرجى المحاولة مرة أخرى.';
    console.error('❌ Error fetching data:', err);
  } finally {
    loading.value = false;
  }
};

const navigateTo = (link) => {
  if (link.startsWith('http')) {
    window.open(link, '_blank');
  } else {
    router.push(link);
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.category-page {
  background-color: #fcfcfc;
  min-height: 100vh;
}

.text-gold {
  color: #d4af37;
}

.bg-gold {
  background-color: #d4af37;
  color: #1a1a2e;
}

.hover-lift {
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.hover-lift:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1) !important;
}

.product-img {
  height: 240px;
  object-fit: cover;
  transition: transform 0.5s;
}

.product-card:hover .product-img {
  transform: scale(1.05);
}

.btn-success {
  background-color: #25d366;
  border-color: #25d366;
}

.btn-success:hover {
  background-color: #128c7e;
  border-color: #128c7e;
}
</style>
