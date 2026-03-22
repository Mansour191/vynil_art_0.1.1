<template>
  <CategoryTemplate
    icon="fa-solid fa-arrow-up"
    titleKey="ceilingsTitle"
    descriptionKey="ceilingsDescription"
    labelKey="ceilingsLabel"
    latestLabelKey="latestCeilingDesigns"
    :subCategories="ceilingCategories"
    badgeLabel="ceilingDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const ceilingCategories = ref([
  {
    id: 1,
    emoji: '🌌',
    titleKey: 'starryCeilings',
    descKey: 'starryCeilingsDesc',
    link: '/search?q=starry',
  },
  {
    id: 2,
    emoji: '🏢',
    titleKey: 'stretchCeilings',
    descKey: 'stretchCeilingsDesc',
    link: '/search?q=stretch',
  },
  {
    id: 3,
    emoji: '🎨',
    titleKey: 'decorativeCeilings',
    descKey: 'decorativeCeilingsDesc',
    link: '/search?q=decorative',
  },
]);
</script>
