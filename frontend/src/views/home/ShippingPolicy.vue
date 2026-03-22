<template>
  <div class="info-page container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow-sm border-0 rounded-lg overflow-hidden bg-card">
          <div class="card-header bg-surface border-bottom p-5 text-center">
            <h1 class="display-5 text-gold mb-3 font-weight-bold">
              <i class="fa-solid fa-shipping-fast me-3"></i> {{ $t('shippingPolicy') || 'سياسة الشحن والتوصيل' }}
            </h1>
            <p class="lead text-muted">{{ $t('shippingPolicyIntro') || 'كل ما تود معرفته عن توصيل طلباتك' }}</p>
          </div>

          <div class="card-body p-5">
            <div class="row g-4 mb-5">
              <div v-for="(item, index) in policyItems" :key="index" class="col-md-6">
                <div class="card h-100 border-0 bg-light p-4 text-center hover-shadow transition-all">
                  <div class="policy-icon-wrapper mb-3">
                    <i :class="item.icon" class="fa-3x text-gold"></i>
                  </div>
                  <h3 class="h5 mb-2 font-weight-bold">{{ item.title }}</h3>
                  <p class="text-secondary small mb-0">{{ item.description }}</p>
                </div>
              </div>
            </div>

            <div class="shipping-table mt-5 overflow-hidden rounded-lg border">
              <table class="table table-hover mb-0">
                <thead class="bg-surface text-gold">
                  <tr>
                    <th class="p-3">{{ $t('wilayaGroup') || 'الولايات' }}</th>
                    <th class="p-3">{{ $t('deliveryTime') || 'مدة التوصيل' }}</th>
                    <th class="p-3">{{ $t('shippingFee') || 'تكلفة الشحن' }}</th>
                  </tr>
                </thead>
                <tbody class="bg-white">
                  <tr>
                    <td class="p-3">الجزائر العاصمة</td>
                    <td class="p-3">24 - 48 ساعة</td>
                    <td class="p-3 font-weight-bold text-success">مجاني</td>
                  </tr>
                  <tr>
                    <td class="p-3">ولايات الشمال</td>
                    <td class="p-3">2 - 4 أيام</td>
                    <td class="p-3 font-weight-bold">400 د.ج</td>
                  </tr>
                  <tr>
                    <td class="p-3">ولايات الجنوب والهضاب</td>
                    <td class="p-3">3 - 6 أيام</td>
                    <td class="p-3 font-weight-bold">700 د.ج</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="mt-5 p-4 bg-light rounded-lg border-dashed">
              <h4 class="text-gold mb-3 h5 font-weight-bold"><i class="fa-solid fa-info-circle me-2"></i> ملاحظات هامة:</h4>
              <ul class="text-muted small">
                <li>يتم البدء في تجهيز الطلب فور تأكيده هاتفياً أو إلكترونياً.</li>
                <li>تختلف مدة التوصيل حسب توفر المنتج في المخزن أو الحاجة لتصنيعه.</li>
                <li>الشحن مجاني لجميع الطلبات التي تتجاوز قيمتها 10,000 د.ج.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const policyItems = computed(() => [
  {
    icon: 'fa-solid fa-clock',
    title: t('deliverySpeed') || 'سرعة التوصيل',
    description: t('deliverySpeedDesc') || 'نحرص على توصيل طلباتكم في أسرع وقت ممكن عبر شبكة واسعة من الشركاء.'
  },
  {
    icon: 'fa-solid fa-map-marked-alt',
    title: t('wideCoverage') || 'تغطية شاملة',
    description: t('wideCoverageDesc') || 'نوفر خدمة التوصيل لجميع الولايات الـ 58 في الجزائر.'
  },
  {
    icon: 'fa-solid fa-box-open',
    title: t('securePackaging') || 'تغليف آمن',
    description: t('securePackagingDesc') || 'يتم تغليف التصاميم بعناية فائقة لضمان وصولها بحالة ممتازة.'
  },
  {
    icon: 'fa-solid fa-headset',
    title: t('orderTracking') || 'تتبع الطلب',
    description: t('orderTrackingDesc') || 'يمكنك تتبع حالة طلبك لحظة بلحظة من خلال حسابك أو عبر الهاتف.'
  }
]);
</script>

<style scoped>
.bg-card { background: var(--bg-card); }
.bg-surface { background: var(--bg-surface); }
.text-gold { color: var(--gold-primary); }
.policy-icon-wrapper { height: 80px; display: flex; align-items: center; justify-content: center; }
.hover-shadow:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.05); transform: translateY(-5px); }
.transition-all { transition: all 0.3s ease; }
.border-dashed { border: 2px dashed #ddd; }
</style>
