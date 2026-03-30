<template>
  <v-main class="category-page">
    <v-container>
      <!-- Main Header -->
      <v-row class="text-center py-8">
        <v-col cols="12">
          <h1 class="text-h4 font-weight-bold mb-2">
            <v-icon :icon="icon" color="primary" class="mb-2" size="large" />
            {{ $t(titleKey) }}
          </h1>
          <p class="text-body-1 text-medium-emphasis">{{ $t(descriptionKey) }}</p>
        </v-col>
      </v-row>

      <!-- Sub Categories (Optional) -->
      <v-row v-if="subCategories && subCategories.length" class="mb-6">
        <v-col
          v-for="sub in subCategories"
          :key="sub.id"
          cols="12"
          sm="6"
          md="4"
          class="mb-4"
        >
          <v-card
            class="h-100 cursor-pointer"
            elevation="4"
            @click="navigateTo(sub.link)"
            hover
          >
            <v-card-text class="text-center pa-4">
              <div class="text-h4 mb-3">{{ sub.emoji }}</div>
              <h3 class="text-h6 mb-2">{{ $t(sub.titleKey) }}</h3>
              <p class="text-body-2 text-medium-emphasis">{{ $t(sub.descKey) }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Latest Designs Section -->
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between mb-4">
            <h2 class="text-h5 font-weight-bold">
              <v-icon color="primary" class="mr-2">mdi-clock</v-icon>
              {{ $t(latestLabelKey) || $t('latestDesigns') }}
            </h2>
            <v-btn
              :to="'/search?q=' + $t(labelKey)"
              variant="outlined"
              color="primary"
              append-icon="mdi-arrow-left"
            >
              {{ $t('viewAll') }}
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <!-- Products Grid -->
      <v-row class="mb-6">
        <v-col v-if="loading" cols="12" class="text-center py-8">
          <v-progress-circular
            indeterminate
            color="primary"
            size="48"
            class="mb-4"
          />
          <p class="text-body-1 text-medium-emphasis">{{ $t('loading') }}</p>
        </v-col>

        <v-col v-else-if="error" cols="12" class="text-center py-8">
          <v-alert
            type="error"
            variant="elevated"
            class="mb-4"
          >
            <v-alert-title>{{ errorMessage }}</v-alert-title>
            <v-alert-actions>
              <v-btn @click="fetchData" prepend-icon="mdi-refresh">
                {{ $t('retry') || 'إعادة المحاولة' }}
              </v-btn>
            </v-alert-actions>
          </v-alert>
        </v-col>

        <v-col v-else-if="products.length === 0" cols="12" class="text-center py-8">
          <p class="text-h6 text-medium-emphasis">{{ $t('noDesignsFound') || 'لا توجد تصاميم متاحة حالياً' }}</p>
        </v-col>

        <template v-else>
          <v-col
            v-for="product in products"
            :key="product.id"
            cols="12"
            sm="6"
            md="4"
            class="mb-4"
          >
            <v-card class="h-100" elevation="4" hover>
              <!-- Product Image -->
              <v-img
                :src="product.image"
                :alt="product.title"
                height="240"
                cover
                class="product-image"
              >
                <template v-slot:placeholder>
                  <v-row class="fill-height" align="center" justify="center">
                    <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  </v-row>
                </template>
              </v-img>
              
              <!-- Badge -->
              <v-chip
                v-if="badgeLabel"
                :text="badgeLabel || $t('new')"
                color="primary"
                size="small"
                class="ma-3"
              />
              
              <!-- Product Content -->
              <v-card-text class="pa-4">
                <v-card-title class="text-h6 mb-2">
                  <router-link :to="product.link" class="text-decoration-none">
                    {{ product.title }}
                  </router-link>
                </v-card-title>
                
                <v-card-subtitle class="text-body-2 text-medium-emphasis mb-3">
                  {{ product.summary }}
                </v-card-subtitle>
                
                <v-card-actions class="d-flex justify-space-between align-center">
                  <v-btn
                    :to="product.link"
                    variant="outlined"
                    prepend-icon="mdi-eye"
                    size="small"
                  >
                    {{ $t('preview') }}
                  </v-btn>
                  
                  <v-btn
                    :href="'https://wa.me/213663140341?text=' + encodeURIComponent($t('whatsappInquiry') + ': ' + product.title)"
                    target="_blank"
                    rel="noopener noreferrer"
                    color="success"
                    prepend-icon="mdi-whatsapp"
                    size="small"
                  >
                    {{ $t('inquiry') }}
                  </v-btn>
                </v-card-actions>
              </v-card-text>
            </v-card>
          </v-col>
        </template>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import ProductService from '@/integration/services/ProductService';

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
    // جلب المنتجات حسب الفئة من قاعدة البيانات
    const categorySlug = props.labelKey.toLowerCase().replace('label', '');
    products.value = await ProductService.getProductsByCategory(categorySlug, 12);
    
    console.log(`✅ Loaded ${products.value.length} products for category: ${categorySlug}`);
  } catch (err) {
    error.value = true;
    errorMessage.value = t('failedToLoadProducts') || 'فشل تحميل المنتجات. يرجى المحاولة مرة أخرى.';
    console.error('❌ Error fetching products:', err);
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

