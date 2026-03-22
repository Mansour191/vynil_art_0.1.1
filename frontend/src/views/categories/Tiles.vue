<template>
  <CategoryTemplate
    icon="fa-solid fa-border-all"
    titleKey="tilesTitle"
    descriptionKey="tilesDescription"
    labelKey="tilesLabel"
    latestLabelKey="latestTileDesigns"
    :subCategories="tileCategories"
    badgeLabel="tileDesign"
  />
</template>

<script setup>
import { ref } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';

const tileCategories = ref([
  {
    id: 1,
    emoji: '🧱',
    titleKey: 'ceramicTiles',
    descKey: 'ceramicTilesDesc',
    link: '/search?q=ceramic',
  },
  {
    id: 2,
    emoji: '💎',
    titleKey: 'marbleTiles',
    descKey: 'marbleTilesDesc',
    link: '/search?q=marble',
  },
  {
    id: 3,
    emoji: '🎨',
    titleKey: 'patternedTiles',
    descKey: 'patternedTilesDesc',
    link: '/search?q=patterned',
  },
]);
</script>
