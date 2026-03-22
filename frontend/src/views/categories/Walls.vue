<template>
  <CategoryTemplate
    icon="fa-solid fa-th-large"
    titleKey="wallsTitle"
    descriptionKey="wallsDescription"
    labelKey="wallsLabel"
    latestLabelKey="latestWallDesigns"
    :subCategories="wallCategories"
    badgeLabel="wallDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const wallCategories = ref([
  {
    id: 1,
    emoji: '🖼️',
    titleKey: '3dWallpapers',
    descKey: '3dWallpapersDesc',
    link: '/search?q=3d',
  },
  {
    id: 2,
    emoji: '🌿',
    titleKey: 'natureDesigns',
    descKey: 'natureDesignsDesc',
    link: '/search?q=nature',
  },
  {
    id: 3,
    emoji: '🏢',
    titleKey: 'officeWalls',
    descKey: 'officeWallsDesc',
    link: '/search?q=office',
  },
]);
</script>
