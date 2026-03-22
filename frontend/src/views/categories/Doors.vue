<template>
  <CategoryTemplate
    icon="fa-solid fa-door-open"
    titleKey="doorsTitle"
    descriptionKey="doorsDescription"
    labelKey="doorsLabel"
    latestLabelKey="latestDoorDesigns"
    :subCategories="doorCategories"
    badgeLabel="doorDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const doorCategories = ref([
  {
    id: 1,
    emoji: '🚪',
    titleKey: 'woodenDoors',
    descKey: 'woodenDoorsDesc',
    link: '/search?q=wooden',
  },
  {
    id: 2,
    emoji: '🏢',
    titleKey: 'modernDoors',
    descKey: 'modernDoorsDesc',
    link: '/search?q=modern',
  },
  {
    id: 3,
    emoji: '✨',
    titleKey: 'glassDoors',
    descKey: 'glassDoorsDesc',
    link: '/search?q=glass',
  },
]);
</script>
