<template>
  <CategoryTemplate
    icon="fa-solid fa-couch"
    titleKey="furnitureTitle"
    descriptionKey="furnitureDescription"
    labelKey="furnitureLabel"
    latestLabelKey="featuredFurniture"
    :subCategories="furnitureCategories"
    badgeLabel="furnitureDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const furnitureCategories = ref([
  {
    id: 1,
    emoji: '🛋️',
    titleKey: 'sofas',
    descKey: 'sofasDesc',
    link: '/search?q=sofa',
  },
  {
    id: 2,
    emoji: '🪑',
    titleKey: 'chairs',
    descKey: 'chairsDesc',
    link: '/search?q=chair',
  },
  {
    id: 3,
    emoji: '🛏️',
    titleKey: 'beds',
    descKey: 'bedsDesc',
    link: '/search?q=bed',
  },
]);
</script>
