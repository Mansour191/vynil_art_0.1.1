<template>
  <div class="loading-container" :class="{ fullscreen, overlay }">
    <div class="spinner" :class="{ small, medium, large }">
      <div class="double-bounce1"></div>
      <div class="double-bounce2"></div>
    </div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    fullscreen: {
      type: Boolean,
      default: false,
    },
    overlay: {
      type: Boolean,
      default: false,
    },
    small: {
      type: Boolean,
      default: false,
    },
    medium: {
      type: Boolean,
      default: false,
    },
    large: {
      type: Boolean,
      default: true,
    },
    message: {
      type: String,
      default: '',
    },
  },
};
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.loading-container.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
}

.loading-container.overlay {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.spinner {
  position: relative;
  margin: 0 auto;
}

.spinner.small {
  width: 40px;
  height: 40px;
}

.spinner.medium {
  width: 60px;
  height: 60px;
}

.spinner.large {
  width: 80px;
  height: 80px;
}

.double-bounce1,
.double-bounce2 {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--gold-gradient);
  opacity: 0.6;
  position: absolute;
  top: 0;
  left: 0;
  animation: bounce 2s infinite ease-in-out;
}

.double-bounce2 {
  animation-delay: -1s;
}

@keyframes bounce {
  0%,
  100% {
    transform: scale(0);
  }
  50% {
    transform: scale(1);
  }
}

.loading-message {
  margin-top: 20px;
  color: var(--gold-primary);
  font-size: 1rem;
  font-weight: 500;
}
</style>
