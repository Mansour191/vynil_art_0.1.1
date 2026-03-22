<template>
  <div class="product-faq mt-5 pt-5 border-top">
    <h4 class="mb-4 text-gold font-weight-bold">
      <i class="fa-solid fa-question-circle me-2"></i> {{ $t('productFaq') || 'الأسئلة الشائعة حول هذا المنتج' }}
    </h4>
    
    <div class="accordion" :id="'faqAccordion-' + productId">
      <div v-for="(item, index) in faqItems" :key="index" class="accordion-item mb-2 border-0 rounded overflow-hidden shadow-sm">
        <h2 class="accordion-header">
          <button 
            class="accordion-button bg-light font-weight-bold text-dark" 
            type="button" 
            :class="{ collapsed: index !== 0 }"
            data-bs-toggle="collapse" 
            :data-bs-target="'#collapse' + productId + index"
            :aria-expanded="index === 0 ? 'true' : 'false'"
          >
            {{ item.question }}
          </button>
        </h2>
        <div 
          :id="'collapse' + productId + index" 
          class="accordion-collapse collapse" 
          :class="{ show: index === 0 }"
          :data-bs-parent="'#faqAccordion-' + productId"
        >
          <div class="accordion-body bg-white text-secondary small">
            {{ item.answer }}
          </div>
        </div>
      </div>
    </div>

    <!-- Quality Badges for Product -->
    <div class="trust-badges-row mt-4 d-flex justify-content-center gap-4 flex-wrap bg-light p-3 rounded-lg border-dashed">
      <div class="trust-badge-item d-flex align-items-center gap-2">
        <i class="fa-solid fa-certificate text-gold"></i>
        <span class="small font-weight-bold">جودة عالية (A+)</span>
      </div>
      <div class="trust-badge-item d-flex align-items-center gap-2">
        <i class="fa-solid fa-shield-alt text-success"></i>
        <span class="small font-weight-bold">ضمان 12 شهر</span>
      </div>
      <div class="trust-badge-item d-flex align-items-center gap-2">
        <i class="fa-solid fa-hand-holding-usd text-info"></i>
        <span class="small font-weight-bold">أفضل سعر للـ m²</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  productId: { type: String, required: true },
  category: { type: String, default: 'general' }
});

const { t } = useI18n();

const faqItems = computed(() => {
  const generalFaq = [
    { 
      question: t('faqQ1') || 'هل الملصق سهل الإزالة لاحقاً؟', 
      answer: t('faqA1') || 'نعم، يمكن إزالة الفينيل بسهولة دون ترك أي آثار لاصقة أو إتلاف الطلاء الأصلي.' 
    },
    { 
      question: t('faqQ2') || 'كيف أقوم بتنظيف المنتج؟', 
      answer: t('faqA2') || 'يمكنك تنظيفه بقطعة قماش ناعمة ومبللة قليلاً، فهو مقاوم للماء والمنظفات الخفيفة.' 
    }
  ];

  const categorySpecificFaq = {
    walls: [
      { question: 'هل يحتاج الجدار لمعالجة قبل التركيب؟', answer: 'يجب أن يكون الجدار نظيفاً وجافاً وخالياً من الرطوبة أو التقشر للحصول على أفضل نتيجة.' }
    ],
    cars: [
      { question: 'هل يتأثر الملصق بغسيل السيارات؟', answer: 'لا يتأثر، الملصق مصمم لتحمل ظروف الجو الصعبة وغسيل السيارات المتكرر.' }
    ],
    kitchens: [
      { question: 'هل يتحمل حرارة المطبخ؟', answer: 'نعم، الفينيل المستخدم مقاوم للحرارة والرطوبة العالية داخل المطبخ.' }
    ]
  };

  return [...generalFaq, ...(categorySpecificFaq[props.category] || [])];
});
</script>

<style scoped>
.text-gold { color: var(--gold-primary); }
.accordion-button:not(.collapsed) { background: rgba(212, 175, 55, 0.1); color: #000; box-shadow: none; }
.accordion-button:focus { box-shadow: none; border-color: var(--gold-primary); }
.border-dashed { border: 1px dashed #ddd; }
.trust-badge-item i { font-size: 1.1rem; }
</style>
