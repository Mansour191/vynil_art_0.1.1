<template>
  <div class="info-page container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow-sm border-0 rounded-lg overflow-hidden bg-card">
          <div class="card-header bg-surface border-bottom p-5 text-center">
            <h1 class="display-5 text-gold mb-3 font-weight-bold">
              <i class="fa-solid fa-shopping-cart me-3"></i> {{ $t('howToOrder') || 'كيف أطلب' }}
            </h1>
            <p class="lead text-muted">{{ $t('howToOrderIntro') || 'خطوات بسيطة للحصول على تصاميمك المفضلة' }}</p>
          </div>

          <div class="card-body p-5">
            <div class="steps-container">
              <div v-for="(step, index) in steps" :key="index" class="step-item d-flex gap-4 mb-5">
                <div class="step-number-wrapper">
                  <span class="step-number">{{ index + 1 }}</span>
                  <div v-if="index < steps.length - 1" class="step-line"></div>
                </div>
                <div class="step-content pt-2">
                  <h3 class="h4 mb-2 text-gold font-weight-bold">{{ step.title }}</h3>
                  <p class="text-secondary mb-0 lead">{{ step.description }}</p>
                </div>
              </div>
            </div>

            <div class="mt-5 p-4 bg-light rounded-lg border-dashed text-center">
              <h4 class="text-dark mb-3">{{ $t('needHelp') || 'هل تحتاج لمساعدة؟' }}</h4>
              <p class="text-muted mb-4">{{ $t('contactOurTeam') || 'فريقنا متاح دائماً لمساعدتك في عملية الطلب.' }}</p>
              <router-link to="/contact" class="btn btn-gold btn-lg px-5 shadow-sm">
                {{ $t('contactUs') }}
              </router-link>
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

const steps = computed(() => [
  {
    title: t('step1Title') || 'اختر التصميم المناسب',
    description: t('step1Desc') || 'تصفح معرض الأعمال أو المتجر واختر التصميم الذي يعجبك.'
  },
  {
    title: t('step2Title') || 'حدد المقاسات والألوان',
    description: t('step2Desc') || 'أدخل الطول والعرض المطلوبين، واختر الألوان ونوعية الخامة المفضلة.'
  },
  {
    title: t('step3Title') || 'أضف للسلة وأتمم الطلب',
    description: t('step3Desc') || 'أضف المنتج لسلة التسوق ثم توجه لصفحة الدفع وأدخل بيانات الشحن.'
  },
  {
    title: t('step4Title') || 'تأكيد الطلب والتوصيل',
    description: t('step4Desc') || 'بمجرد تأكيد الطلب، سيقوم فريقنا بتجهيزه وشحنه إليك في أسرع وقت.'
  }
]);
</script>

<style scoped>
.bg-card { background: var(--bg-card); }
.bg-surface { background: var(--bg-surface); }
.text-gold { color: var(--gold-primary); }
.btn-gold { background: var(--gold-gradient); color: #000; border: none; font-weight: 700; }

.step-number-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.step-number {
  width: 50px;
  height: 50px;
  background: var(--gold-gradient);
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
  z-index: 2;
}

.step-line {
  width: 2px;
  flex-grow: 1;
  background: var(--border-subtle);
  margin-top: 10px;
}

.border-dashed { border: 2px dashed #ddd; }
</style>
