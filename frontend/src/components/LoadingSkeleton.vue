<template>
  <v-skeleton-loader
    :type="skeletonType"
    :width="width"
    :height="height"
    :loading="animate"
    class="skeleton-item"
    :style="customStyle"
  />
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();

const props = defineProps({
  type: {
    type: String,
    default: 'text', // text, title, avatar, image, button, circle
  },
  width: {
    type: String,
    default: '100%',
  },
  height: {
    type: String,
    default: '1rem',
  },
  animate: {
    type: Boolean,
    default: true,
  },
  borderRadius: {
    type: String,
    default: '8px',
  }
});

const isRtl = computed(() => locale.value === 'ar');

const skeletonType = computed(() => {
  const typeMap = {
    'text': 'text',
    'title': 'heading',
    'avatar': 'avatar',
    'image': 'image',
    'button': 'button',
    'circle': 'avatar'
  };
  return typeMap[props.type] || 'text';
});

const customStyle = computed(() => ({
  width: props.width,
  height: props.height,
  borderRadius: props.type === 'circle' || props.type === 'avatar' ? '50%' : props.borderRadius
}));
</script>

