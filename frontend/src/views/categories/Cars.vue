<template>
  <CategoryTemplate
    icon="fa-solid fa-car"
    titleKey="carsTitle"
    descriptionKey="carsDescription"
    labelKey="carsLabel"
    latestLabelKey="latestCarDesigns"
    :subCategories="carCategories"
    badgeLabel="carWrap"
  >
    <!-- يمكنك إضافة أقسام مخصصة هنا إذا أردت استخدام السلوتس مستقبلاً -->
  </CategoryTemplate>
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const carCategories = ref([
  {
    id: 1,
    emoji: '⚫',
    titleKey: 'matteCars',
    descKey: 'matteCarsDesc',
    link: '/search?q=matte',
  },
  {
    id: 2,
    emoji: '✨',
    titleKey: 'glossyCars',
    descKey: 'glossyCarsDesc',
    link: '/search?q=glossy',
  },
  {
    id: 3,
    emoji: '🎨',
    titleKey: 'satinCars',
    descKey: 'satinCarsDesc',
    link: '/search?q=satin',
  },
  {
    id: 4,
    emoji: '🪞',
    titleKey: 'chromeCars',
    descKey: 'chromeCarsDesc',
    link: '/search?q=chrome',
  },
]);
</script>
