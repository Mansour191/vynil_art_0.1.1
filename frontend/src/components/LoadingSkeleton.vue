<template>
  <div 
    class="skeleton-item" 
    :class="[type, { 'animate-pulse': animate }]" 
    :style="style"
    aria-hidden="true"
  ></div>
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

const style = computed(() => ({
  width: props.width,
  height: props.height,
  borderRadius: props.type === 'circle' || props.type === 'avatar' ? '50%' : props.borderRadius,
  '--rtl-direction': isRtl.value ? '-1' : '1'
}));
</script>

<style scoped>
.skeleton-item {
  background: linear-gradient(
    90deg,
    var(--border-subtle, rgba(255, 255, 255, 0.05)) 25%,
    var(--bg-surface, rgba(255, 255, 255, 0.1)) 50%,
    var(--border-subtle, rgba(255, 255, 255, 0.05)) 75%
  );
  background-size: 200% 100%;
  display: inline-block;
  vertical-align: middle;
}

.animate-pulse {
  animation: loading 1.5s infinite ease-in-out;
}

@keyframes loading {
  0% {
    background-position: calc(200% * var(--rtl-direction, 1)) 0;
  }
  100% {
    background-position: calc(-200% * var(--rtl-direction, 1)) 0;
  }
}

/* Types */
.title { height: 2.5rem; margin-bottom: 1.5rem; width: 70%; }
.text { height: 1.2rem; margin-bottom: 0.8rem; }
.avatar { width: 50px; height: 50px; }
.image { width: 100%; height: 250px; }
.button { width: 140px; height: 45px; border-radius: 12px; }
.circle { width: 40px; height: 40px; }

/* Light Mode Adjustment */
:global(body.light-mode) .skeleton-item {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #f8f8f8 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
}
</style>
