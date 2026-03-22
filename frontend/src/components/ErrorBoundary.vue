<template>
  <div class="error-boundary-container">
    <div v-if="hasError" class="error-boundary">
      <div class="error-content">
        <div class="error-icon">
          <i class="fa-solid fa-exclamation-triangle"></i>
        </div>
        <h3>عذراً، حدث خطأ غير متوقع</h3>
        <p>{{ errorMessage }}</p>
        <button @click="retry" class="retry-btn"><i class="fa-solid fa-redo"></i> إعادة المحاولة</button>
      </div>
    </div>
    <div v-else>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorBoundary',
  data() {
    return {
      hasError: false,
      errorMessage: '',
    };
  },
  methods: {
    retry() {
      this.hasError = false;
      this.errorMessage = '';
    },
  },
  errorCaptured(err, vm, info) {
    this.hasError = true;
    this.errorMessage = err.message || 'حدث خطأ غير متوقع';
    console.error('Error caught by boundary:', err, info);
    return false;
  },
};
</script>

<style scoped>
.error-boundary-container {
  width: 100%;
  min-height: 100%;
}

.error-boundary {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border-radius: 24px;
  margin: 20px;
  padding: 40px;
}

.error-content {
  text-align: center;
  max-width: 500px;
}

.error-icon {
  font-size: 4rem;
  color: #f44336;
  margin-bottom: 20px;
  animation: shake 0.5s ease;
}

.error-content h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.error-content p {
  color: var(--text-dim);
  margin-bottom: 20px;
}

.retry-btn {
  padding: 12px 24px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 12px;
  color: var(--bg-deep);
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}
</style>
