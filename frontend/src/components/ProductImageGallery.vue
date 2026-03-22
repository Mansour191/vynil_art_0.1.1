<template>
  <div class="product-gallery">
    <!-- Main Image Display -->
    <div class="main-image-wrapper card border-0 shadow-sm rounded-lg overflow-hidden mb-3" @click="$emit('open-lightbox')">
      <img 
        :src="currentImage || images[0]" 
        :alt="title" 
        class="main-img transition-all"
        loading="lazy"
      >
      <div class="zoom-hint">
        <i class="fa-solid fa-search-plus"></i>
      </div>
    </div>

    <!-- Thumbnails Grid -->
    <div v-if="images.length > 1" class="thumbnails-row d-flex gap-2 overflow-auto pb-2">
      <div 
        v-for="(img, index) in images" 
        :key="index"
        class="thumb-item rounded border-2 transition-all"
        :class="{ 'active border-gold': currentImage === img || (!currentImage && index === 0) }"
        @click="currentImage = img"
      >
        <img :src="img" :alt="`${title} - ${index + 1}`" loading="lazy">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  images: { type: Array, required: true },
  title: { type: String, required: true }
});

const currentImage = ref(null);

defineEmits(['open-lightbox']);
</script>

<style scoped>
.main-image-wrapper {
  position: relative;
  aspect-ratio: 1;
  cursor: zoom-in;
  background: #f8f9fa;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.main-image-wrapper:hover .main-img {
  transform: scale(1.05);
}

.zoom-hint {
  position: absolute;
  bottom: 15px;
  right: 15px;
  background: rgba(0,0,0,0.5);
  color: white;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.main-image-wrapper:hover .zoom-hint {
  opacity: 1;
}

.thumbnails-row {
  scrollbar-width: thin;
  scrollbar-color: var(--gold-primary) transparent;
}

.thumb-item {
  width: 70px;
  height: 70px;
  flex-shrink: 0;
  cursor: pointer;
  border: 2px solid transparent;
  background: white;
}

.thumb-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-item.active {
  border-color: var(--gold-primary) !important;
}

.border-gold {
  border-color: var(--gold-primary) !important;
}
</style>
