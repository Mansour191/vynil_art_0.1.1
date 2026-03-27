<template>
  <div class="product-gallery">
    <!-- Main Image Display -->
    <v-card
      class="main-image-wrapper mb-4"
      elevation="4"
      @click="$emit('open-lightbox')"
      style="cursor: zoom-in"
    >
      <v-img
        :src="currentImage || images[0]"
        :alt="title"
        aspect-ratio="1"
        cover
        class="main-img"
      >
        <template v-slot:placeholder>
          <v-row class="fill-height" align="center" justify="center">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-row>
        </template>
      </v-img>
      
      <!-- Zoom Hint -->
      <v-btn
        class="zoom-hint"
        icon="mdi-magnify-plus"
        variant="elevated"
        size="small"
        color="white"
        style="position: absolute; bottom: 15px; right: 15px;"
      />
    </v-card>

    <!-- Thumbnails Grid -->
    <div v-if="images.length > 1" class="thumbnails-row d-flex ga-2 overflow-auto pb-2">
      <v-card
        v-for="(img, index) in images"
        :key="index"
        class="thumb-item"
        :class="{ 'border-primary': currentImage === img || (!currentImage && index === 0) }"
        elevation="2"
        width="70"
        height="70"
        @click="currentImage = img"
        style="cursor: pointer"
      >
        <v-img
          :src="img"
          :alt="`${title} - ${index + 1}`"
          cover
          height="70"
        />
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  images: { type: Array, required: true },
  title: { type: String, required: true }
});

defineEmits(['open-lightbox']);

const currentImage = ref(null);
</script>

