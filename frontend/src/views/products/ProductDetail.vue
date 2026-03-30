<template>
  <v-sheet class="bg-surface min-h-screen overflow-hidden py-8">
    <!-- Background Decorations -->
    <div class="pointer-events-none absolute -left-28 -top-28 h-64 w-64 rounded-full bg-warning/20 blur-3xl"></div>
    <div class="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-info/20 blur-3xl"></div>

    <v-container class="relative z-10">
      <Breadcrumbs class="mb-6" />

      <!-- Loading State -->
      <v-row v-if="loading">
        <v-col cols="12" md="6">
          <v-skeleton-loader
            type="image"
            height="420"
            class="rounded-3xl"
          ></v-skeleton-loader>
        </v-col>
        <v-col cols="12" md="6">
          <v-card elevation="2" class="rounded-3xl pa-6">
            <v-skeleton-loader
              type="heading, text, text, button"
              class="mb-4"
            ></v-skeleton-loader>
          </v-card>
        </v-col>
      </v-row>

      <!-- Error State -->
      <v-alert
        v-else-if="error"
        type="error"
        variant="tonal"
        class="rounded-3xl mb-6"
        text
      >
        <template #prepend>
          <v-icon>mdi-alert-circle</v-icon>
        </template>
        <h2 class="text-h5 font-weight-bold mb-2">{{ $t('productDetail.errorTitle') }}</h2>
        <p class="text-body-2 mb-4">{{ error }}</p>
        <v-btn
          @click="loadProduct"
          color="error"
          variant="elevated"
          class="text-none"
        >
          {{ $t('productDetail.retry') }}
        </v-btn>
      </v-alert>

      <!-- Product Content -->
      <v-row v-else-if="product">
        <v-col cols="12" md="6">
          <v-card elevation="2" class="rounded-3xl pa-4">
            <v-img
              :src="product.image"
              :alt="product.name"
              height="420"
              class="rounded-2xl"
              cover
            >
              <template #placeholder>
                <v-skeleton-loader type="image"></v-skeleton-loader>
              </template>
            </v-img>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card elevation="4" class="rounded-3xl pa-6 pa-md-8 sticky top-24">
          <v-card-text>
            <!-- Product Tags -->
            <div class="d-flex flex-wrap gap-2 mb-4">
              <v-chip
                variant="outlined"
                color="grey-lighten-2"
                size="small"
                class="text-none"
              >
                {{ product.type }}
              </v-chip>
              <v-chip
                color="warning"
                variant="elevated"
                size="small"
                class="text-none font-weight-bold"
              >
                PACLOS
              </v-chip>
            </div>

            <!-- Product Title and Description -->
            <h1 class="text-h3 text-md-h2 font-weight-black mb-4">{{ product.name }}</h1>
            <p class="text-body-1 text-medium-emphasis mb-6">{{ product.description }}</p>

            <!-- Product Details Grid -->
            <v-row class="mb-6">
              <v-col cols="6">
                <v-card variant="outlined" class="pa-3">
                  <div class="text-caption text-medium-emphasis">{{ $t('productDetail.code') }}</div>
                  <div class="font-weight-bold">{{ product.code }}</div>
                </v-card>
              </v-col>
              <v-col cols="6">
                <v-card variant="outlined" class="pa-3">
                  <div class="text-caption text-medium-emphasis">{{ $t('productDetail.type') }}</div>
                  <div class="font-weight-bold">{{ product.type }}</div>
                </v-card>
              </v-col>
            </v-row>

            <!-- Price -->
            <v-card elevation="2" class="mb-6 pa-4 bg-gradient-to-r from-warning/20 to-surface">
              <div class="text-caption text-medium-emphasis mb-1">{{ $t('productDetail.price') }}</div>
              <div class="text-h3 font-weight-black text-warning">{{ formatPrice(product.price) }}</div>
            </v-card>

            <!-- AI Smart Measurement -->
            <v-card elevation="2" class="mb-6 pa-4">
              <h3 class="text-h6 font-weight-bold text-warning mb-3">{{ $t('productDetail.aiSmartMeasurement') }}</h3>
              <v-text-field
                v-model="referenceDimensionCm"
                type="number"
                :label="$t('productDetail.referenceDimensionCm')"
                variant="outlined"
                color="warning"
                min="10"
                class="mb-3"
              ></v-text-field>
              <v-file-input
                accept="image/*"
                :label="$t('productDetail.uploadImage')"
                variant="outlined"
                color="warning"
                prepend-icon="mdi-camera"
                @change="onImageChange"
                class="mb-3"
              ></v-file-input>
              <v-btn
                @click="runSmartMeasurement"
                color="warning"
                variant="tonal"
                prepend-icon="mdi-brain"
                class="w-100 mb-3 text-none"
              >
              :disabled="aiLoading || !aiImageFile"
                class="text-none"
              >
                {{ aiLoading ? $t('loading') : $t('productDetail.calculateWithAi') }}
              </v-btn>

            <!-- AI Results -->
            <v-card variant="outlined" class="pa-3">
              <div class="text-body-2 text-medium-emphasis mb-1">
                {{ $t('productDetail.estimatedArea') }}:
                <strong class="text-white">{{ estimatedAreaM2.toFixed(2) }} m²</strong>
              </div>
              <div class="text-body-2 text-medium-emphasis">
                {{ $t('productDetail.estimatedTotal') }}:
                <strong class="text-warning">{{ formatPrice(calculatedTotalPrice) }}</strong>
              </div>
              <v-alert v-if="aiError" type="error" variant="tonal" class="mt-2" density="compact">
                {{ aiError }}
              </v-alert>
              <p v-if="fallbackMode" class="text-caption text-medium-emphasis mt-1">{{ $t('productDetail.fallbackPrice') }}</p>
            </v-card>
          </v-card-text>

          <!-- Order Button -->
          <v-card-actions class="pa-6">
            <v-btn
              @click="confirmOrder"
              color="warning"
              variant="elevated"
              size="large"
              class="w-100 text-none font-weight-bold"
              prepend-icon="mdi-shopping"
            >
              {{ $t('productDetail.orderNow') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
  </v-sheet>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '@/store/auth';
import Breadcrumbs from '@/components/common/Breadcrumbs.vue';
import apolloClient from '@/integration/services/apollo';
import { GET_PRODUCT_DETAIL } from '@/integration/services/graphql';
import AIMeasureService from '@/integration/services/AIMeasureService';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { locale, t } = useI18n();

const loading = ref(true);
const error = ref('');
const product = ref(null);
const aiImageFile = ref(null);
const referenceDimensionCm = ref(100);
const aiLoading = ref(false);
const aiError = ref('');
const estimatedAreaM2 = ref(1);
const fallbackMode = ref(false);

const routeProductId = computed(() => String(route.params.id || '').trim());
const normalizedSlug = computed(() => routeProductId.value.toLowerCase());

const formatPrice = (price) =>
  new Intl.NumberFormat(locale.value || 'ar-DZ', {
    style: 'currency',
    currency: 'DZD',
    maximumFractionDigits: 0,
  }).format(Number(price || 0));

const calculatedTotalPrice = computed(() => Number(product.value?.price || 0) * Number(estimatedAreaM2.value || 1));

const mapProduct = (raw) => ({
  id: raw.id,
  code: String(raw.slug || routeProductId.value || 'N/A').toUpperCase(),
  name: raw.nameAr || raw.nameEn || t('productDetail.unknownProduct'),
  type: raw.category?.nameEn || t('productDetail.defaultType'),
  description: raw.descriptionAr || raw.descriptionEn || t('productDetail.noDescription'),
  price: raw.basePrice || 0,
  image:
    raw.image ||
    'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?q=80&w=1200&auto=format&fit=crop',
});

const fetchBySlug = async (slug) => {
  const { data, errors } = await apolloClient.query({
    query: GET_PRODUCT_DETAIL,
    variables: { slug },
    fetchPolicy: 'network-only',
  });

  if (errors?.length) {
    throw new Error(errors.map((item) => item.message).join(' | '));
  }

  return data?.productBySlug || null;
};

const loadProduct = async () => {
  loading.value = true;
  error.value = '';
  product.value = null;

  try {
    if (!routeProductId.value) {
      throw new Error(t('productDetail.missingId'));
    }

    const candidateSlugs = [routeProductId.value, normalizedSlug.value].filter(Boolean);
    const uniqueSlugs = [...new Set(candidateSlugs)];
    let rawProduct = null;

    for (const slug of uniqueSlugs) {
      // API currently resolves product detail by slug; we pass route id directly first.
      rawProduct = await fetchBySlug(slug);
      if (rawProduct) break;
    }

    if (!rawProduct) {
      throw new Error(t('productDetail.notFound'));
    }

    product.value = mapProduct(rawProduct);
  } catch (err) {
    error.value = err?.message || t('productDetail.fetchError');
  } finally {
    loading.value = false;
  }
};

const confirmOrder = () => {
  if (!authStore.isAuthenticated) {
    router.push({
      path: '/login',
      query: { redirect: '/checkout', reason: 'auth_required' },
    });
    return;
  }

  router.push('/checkout');
};

const onImageChange = (event) => {
  const file = event.target.files?.[0];
  aiImageFile.value = file || null;
};

const runSmartMeasurement = async () => {
  if (!aiImageFile.value || !product.value) return;
  aiLoading.value = true;
  aiError.value = '';
  fallbackMode.value = false;
  try {
    const result = await AIMeasureService.measureSurface({
      imageFile: aiImageFile.value,
      referenceDimensionCm: referenceDimensionCm.value,
      pricePerM2: product.value.price,
    });
    estimatedAreaM2.value = Number(result.estimated_area_m2 || 1);
  } catch (err) {
    fallbackMode.value = true;
    estimatedAreaM2.value = 1;
    aiError.value = t('productDetail.aiBusy');
  } finally {
    aiLoading.value = false;
  }
};

onMounted(loadProduct);
watch(() => route.params.id, loadProduct);
</script>
