<template>
  <CategoryTemplate
    icon="fa-solid fa-utensils"
    titleKey="kitchensTitle"
    descriptionKey="kitchensDescription"
    labelKey="kitchensLabel"
    latestLabelKey="latestKitchenDesigns"
    :subCategories="kitchenCategories"
    badgeLabel="kitchenDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const kitchenCategories = ref([
  {
    id: 1,
    emoji: '🍳',
    titleKey: 'modernKitchens',
    descKey: 'modernKitchensDesc',
    link: '/search?q=modern',
  },
  {
    id: 2,
    emoji: '🏠',
    titleKey: 'classicKitchens',
    descKey: 'classicKitchensDesc',
    link: '/search?q=classic',
  },
  {
    id: 3,
    emoji: '✨',
    titleKey: 'minimalistKitchens',
    descKey: 'minimalistKitchensDesc',
    link: '/search?q=minimalist',
  },
]);
</script>
