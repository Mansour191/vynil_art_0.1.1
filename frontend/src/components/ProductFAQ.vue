<template>
  <v-card variant="elevated" class="product-faq mt-8 pa-6">
    <!-- Header -->
    <v-card-title class="text-h5 font-weight-bold mb-6">
      <v-icon color="primary" class="mr-2">mdi-help-circle</v-icon>
      {{ $t('productFaq') || 'الأسئلة الشائعة حول هذا المنتج' }}
    </v-card-title>
    
    <!-- FAQ Accordion -->
    <v-expansion-panels variant="accordion" class="mb-6">
      <v-expansion-panel
        v-for="(item, index) in faqItems"
        :key="index"
        :value="index"
        :title="item.question"
      >
        <v-expansion-panel-text class="text-body-2">
          {{ item.answer }}
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
    
    <!-- Quality Badges -->
    <v-card variant="outlined" class="trust-badges pa-4">
      <v-card-title class="text-h6 mb-4">ضمانات الجودة</v-card-title>
      <v-row justify="center" class="ga-4">
        <v-col cols="auto" class="d-flex align-center ga-2">
          <v-icon color="primary" size="large">mdi-certificate</v-icon>
          <span class="text-body-2 font-weight-medium">جودة عالية (A+)</span>
        </v-col>
        <v-col cols="auto" class="d-flex align-center ga-2">
          <v-icon color="success" size="large">mdi-shield-check</v-icon>
          <span class="text-body-2 font-weight-medium">ضمان 12 شهر</span>
        </v-col>
        <v-col cols="auto" class="d-flex align-center ga-2">
          <v-icon color="info" size="large">mdi-hand-coin</v-icon>
          <span class="text-body-2 font-weight-medium">أفضل سعر للـ م²</span>
        </v-col>
      </v-row>
    </v-card>
  </v-card>
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
      { question: 'هل يتأثر الملصق بغاز السيارات؟', answer: 'لا يتأثر، الملصق مصمم لتحمل ظروف الجو الصعبة وغاز السيارات المتكرر.' }
    ],
    kitchens: [
      { question: 'هل يتحمل حرارة المطبخ؟', answer: 'نعم، الفينيل المستخدم مقاوم للحرارة والرطوبة العالية داخل المطبخ.' }
    ]
  };

  return [...generalFaq, ...(categorySpecificFaq[props.category] || [])];
});
</script>

