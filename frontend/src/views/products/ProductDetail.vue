<template>
  <section class="relative min-h-screen overflow-hidden bg-slate-950 py-8 text-slate-100">
    <div class="pointer-events-none absolute -left-28 -top-28 h-64 w-64 rounded-full bg-amber-400/20 blur-3xl"></div>
    <div class="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-sky-300/20 blur-3xl"></div>

    <div class="container relative z-10 mx-auto px-4">
      <Breadcrumbs class="mb-6" />

      <div v-if="loading" class="grid gap-6 lg:grid-cols-2">
        <div class="h-[420px] animate-pulse rounded-3xl bg-slate-800/80"></div>
        <div class="space-y-4 rounded-3xl border border-slate-700 bg-slate-900/70 p-6">
          <div class="h-6 w-32 animate-pulse rounded bg-slate-800"></div>
          <div class="h-9 w-2/3 animate-pulse rounded bg-slate-800"></div>
          <div class="h-20 animate-pulse rounded bg-slate-800"></div>
          <div class="h-12 animate-pulse rounded bg-slate-800"></div>
        </div>
      </div>

      <div v-else-if="error" class="rounded-3xl border border-red-400/30 bg-red-500/10 p-8 text-center">
        <h2 class="mb-2 text-2xl font-bold">{{ $t('productDetail.errorTitle') }}</h2>
        <p class="mb-5 text-red-100/90">{{ error }}</p>
        <button
          type="button"
          class="rounded-xl bg-red-500 px-5 py-2.5 font-semibold text-white transition hover:bg-red-600"
          @click="loadProduct"
        >
          {{ $t('productDetail.retry') }}
        </button>
      </div>

      <div v-else-if="product" class="grid items-start gap-6 lg:grid-cols-2">
        <div class="rounded-3xl border border-slate-700 bg-slate-900/70 p-4">
          <img
            :src="product.image"
            :alt="product.name"
            class="h-[420px] w-full rounded-2xl object-cover md:h-[560px]"
          />
        </div>

        <div class="sticky top-24 rounded-3xl border border-slate-700 bg-slate-900/70 p-6 md:p-8">
          <div class="mb-3 flex flex-wrap gap-2">
            <span class="rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-xs font-semibold">
              {{ product.type }}
            </span>
            <span class="rounded-full bg-amber-300 px-3 py-1 text-xs font-bold text-slate-900">PACLOS</span>
          </div>

          <h1 class="mb-3 text-3xl font-extrabold md:text-4xl">{{ product.name }}</h1>
          <p class="mb-6 leading-7 text-slate-300">{{ product.description }}</p>

          <div class="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div class="rounded-xl border border-slate-700 bg-slate-800/60 p-3">
              <div class="text-xs text-slate-400">{{ $t('productDetail.code') }}</div>
              <div class="font-semibold">{{ product.code }}</div>
            </div>
            <div class="rounded-xl border border-slate-700 bg-slate-800/60 p-3">
              <div class="text-xs text-slate-400">{{ $t('productDetail.type') }}</div>
              <div class="font-semibold">{{ product.type }}</div>
            </div>
          </div>

          <div class="mb-6 rounded-xl bg-gradient-to-r from-amber-300/20 to-slate-700/20 p-4">
            <div class="text-xs text-slate-400">{{ $t('productDetail.price') }}</div>
            <div class="text-2xl font-extrabold text-amber-300">{{ formatPrice(product.price) }}</div>
          </div>

          <div class="mb-6 rounded-xl border border-slate-700 bg-slate-800/60 p-4">
            <h3 class="mb-3 text-sm font-bold text-amber-300">{{ $t('productDetail.aiSmartMeasurement') }}</h3>
            <div class="mb-3">
              <label class="mb-1 block text-xs text-slate-300">{{ $t('productDetail.referenceDimensionCm') }}</label>
              <input
                v-model="referenceDimensionCm"
                type="number"
                min="10"
                class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-sm text-white outline-none"
              />
            </div>
            <div class="mb-3">
              <input
                type="file"
                accept="image/*"
                class="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 text-xs text-slate-300"
                @change="onImageChange"
              />
            </div>
            <button
              type="button"
              class="mb-3 w-full rounded-lg border border-amber-300/50 bg-amber-300/20 px-3 py-2 text-sm font-semibold text-amber-200 hover:bg-amber-300/30"
              :disabled="aiLoading || !aiImageFile"
              @click="runSmartMeasurement"
            >
              {{ aiLoading ? $t('loading') : $t('productDetail.calculateWithAi') }}
            </button>

            <div class="rounded-lg border border-slate-600 bg-slate-900/70 p-3 text-sm">
              <div class="mb-1 text-slate-300">
                {{ $t('productDetail.estimatedArea') }}:
                <strong class="text-white">{{ estimatedAreaM2.toFixed(2) }} m²</strong>
              </div>
              <div class="text-slate-300">
                {{ $t('productDetail.estimatedTotal') }}:
                <strong class="text-amber-300">{{ formatPrice(calculatedTotalPrice) }}</strong>
              </div>
              <p v-if="aiError" class="mt-2 text-xs text-red-300">{{ aiError }}</p>
              <p v-if="fallbackMode" class="mt-1 text-xs text-slate-400">{{ $t('productDetail.fallbackPrice') }}</p>
            </div>
          </div>

          <button
            type="button"
            class="w-full rounded-xl bg-gradient-to-r from-amber-400 to-amber-300 px-4 py-3 font-bold text-slate-900 transition hover:brightness-110"
            @click="confirmOrder"
          >
            {{ $t('productDetail.orderNow') }}
          </button>
        </div>
      </div>
    </div>
  </section>
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
