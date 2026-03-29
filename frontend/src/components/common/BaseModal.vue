<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div 
        v-if="modelValue" 
        class="modal-overlay" 
        @mousedown.self="handleOverlayClick"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="titleId"
      >
        <div 
          class="modal-container" 
          :class="[size, { 'modal-full-mobile': fullMobile }]"
          tabindex="-1"
          ref="modalRef"
          @keydown.esc="close"
        >
          <!-- Header -->
          <div v-if="showHeader" class="modal-header">
            <slot name="header">
              <h5 :id="titleId" class="modal-title">{{ title }}</h5>
            </slot>
            <button 
              v-if="showClose" 
              type="button" 
              class="btn-close-modal" 
              @click="close"
              aria-label="Close"
            >
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <slot></slot>
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md' // sm, md, lg, xl
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  showClose: {
    type: Boolean,
    default: true
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  fullMobile: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update:modelValue', 'close', 'open']);

const modalRef = ref(null);
const titleId = `modal-title-${Math.random().toString(36).substr(2, 9)}`;

const close = () => {
  emit('update:modelValue', false);
  emit('close');
};

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close();
  }
};

const onEsc = (e) => {
  if (e.key === 'Escape' && props.modelValue) {
    close();
  }
};

watch(() => props.modelValue, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden';
    emit('open');
    // Focus modal for accessibility
    setTimeout(() => {
      modalRef.value?.focus();
    }, 100);
  } else {
    document.body.style.overflow = '';
  }
});

onMounted(() => {
  window.addEventListener('keydown', onEsc);
});

onUnmounted(() => {
  window.removeEventListener('keydown', onEsc);
  document.body.style.overflow = '';
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-container {
  background: var(--bg-card, #fff);
  border-radius: 20px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid var(--border-subtle, rgba(255, 255, 255, 0.1));
  outline: none;
}

/* Sizes */
.sm { max-width: 400px; }
.md { max-width: 600px; }
.lg { max-width: 800px; }
.xl { max-width: 1100px; }

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid var(--border-subtle, #eee);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  margin: 0;
  font-weight: 700;
  color: var(--gold-primary, #d4af37);
}

.btn-close-modal {
  background: none;
  border: none;
  color: var(--text-dim, #666);
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-modal:hover {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-primary);
}

.modal-body {
  padding: 25px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid var(--border-subtle, #eee);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* RTL Support */
[dir="rtl"] .modal-header {
  flex-direction: row;
}

/* Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

@media (max-width: 576px) {
  .modal-full-mobile {
    max-width: 100%;
    height: 100%;
    max-height: 100%;
    border-radius: 0;
  }
  
  .modal-overlay {
    padding: 0;
  }
}
</style>
