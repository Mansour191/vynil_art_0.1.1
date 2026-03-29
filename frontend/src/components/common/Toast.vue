<template>
  <div 
    class="toast-container position-fixed bottom-0 p-3" 
    :class="[isRtl ? 'start-0' : 'end-0']"
    style="z-index: 10000; pointer-events: none;"
  >
    <transition-group name="toast-slide">
      <div 
        v-for="toast in toasts" 
        :key="toast.id" 
        class="toast show mb-2 border-0 shadow-lg overflow-hidden" 
        :class="[`bg-${toast.type}`, 'text-white']"
        role="alert" 
        aria-live="assertive" 
        aria-atomic="true"
        style="pointer-events: auto;"
      >
        <div class="toast-progress" :style="{ width: toast.progress + '%' }"></div>
        <div class="toast-header bg-transparent border-0 text-white d-flex align-items-center py-2 px-3">
          <i :class="toast.icon" class="me-2 fs-5"></i>
          <strong class="me-auto">{{ toast.title }}</strong>
          <button 
            type="button" 
            class="btn-close btn-close-white ms-2" 
            @click="removeToast(toast.id)"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body px-3 pb-3 pt-0 opacity-90 small">
          {{ toast.message }}
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();
const toasts = ref([]);
const TOAST_DURATION = 5000;

const isRtl = computed(() => locale.value === 'ar');

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id);
};

const addToast = (event) => {
  const { title, message, type, icon } = event.detail;
  const id = Date.now();
  
  const newToast = {
    id,
    title,
    message,
    type: type === 'error' ? 'danger' : (type || 'info'),
    icon: icon || 'fa-solid fa-info-circle',
    progress: 100
  };

  toasts.value.push(newToast);

  const interval = 50;
  const step = 100 / (TOAST_DURATION / interval);
  
  const timer = setInterval(() => {
    newToast.progress -= step;
    if (newToast.progress <= 0) {
      clearInterval(timer);
      removeToast(id);
    }
  }, interval);
};

onMounted(() => {
  window.addEventListener('app-toast', addToast);
});

onUnmounted(() => {
  window.removeEventListener('app-toast', addToast);
});
</script>

<style scoped>
.toast-container {
  max-width: 350px;
  width: 100%;
}

.toast {
  border-radius: 12px;
  position: relative;
  min-width: 300px;
  backdrop-filter: blur(10px);
}

.toast-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 3px;
  background: rgba(255, 255, 255, 0.4);
  transition: width 0.05s linear;
}

/* Animations */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

[dir="rtl"] .toast-slide-enter-from {
  transform: translateX(-100%);
}

.toast-slide-leave-to {
  transform: scale(0.8);
  opacity: 0;
}

/* Colors */
.bg-success { background: linear-gradient(135deg, #28a745 0%, #34ce57 100%) !important; }
.bg-danger { background: linear-gradient(135deg, #dc3545 0%, #f86d7d 100%) !important; }
.bg-warning { background: linear-gradient(135deg, #ffc107 0%, #ffdb6e 100%) !important; color: #000 !important; }
.bg-info { background: linear-gradient(135deg, #17a2b8 0%, #29d6f1 100%) !important; }

.bg-warning .btn-close-white { filter: invert(1) grayscale(100%) brightness(0); }

/* Custom Scrollbar for small mobile screens if many toasts */
.toast-container {
  max-height: 100vh;
  overflow-y: auto;
  scrollbar-width: none;
}
.toast-container::-webkit-scrollbar { display: none; }
</style>
