<template>
  <div class="dialog-overlay" v-if="show" @click.self="handleOverlayClick">
    <div class="dialog-content">
      <div class="dialog-header">
        <i class="fa-solid fa-exclamation-triangle"></i>
        <h3>{{ $t('unsavedChanges') }}</h3>
      </div>

      <div class="dialog-body">
        <p>{{ $t('unsavedChangesMessage') }}</p>
      </div>

      <div class="dialog-footer">
        <button class="btn-stay" @click="stay">
          <i class="fa-solid fa-edit"></i>
          {{ $t('stayOnPage') }}
        </button>
        <button class="btn-leave" @click="leave">
          <i class="fa-solid fa-sign-out-alt"></i>
          {{ $t('leaveAnyway') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UnsavedChangesDialog',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    stay() {
      this.$emit('stay');
    },
    leave() {
      this.$emit('leave');
    },
    handleOverlayClick() {
      this.stay();
    },
  },
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dialog-content {
  background: var(--bg-card);
  border-radius: 20px;
  width: 90%;
  max-width: 450px;
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft), 0 0 30px rgba(212, 175, 55, 0.2);
  overflow: hidden;
}

.dialog-header {
  padding: 25px 25px 15px;
  text-align: center;
}

.dialog-header i {
  font-size: 3rem;
  color: var(--gold-primary);
  margin-bottom: 10px;
}

.dialog-header h3 {
  color: var(--gold-primary);
  font-size: 1.5rem;
  margin: 0;
}

.dialog-body {
  padding: 0 25px 20px;
  text-align: center;
}

.dialog-body p {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
}

.dialog-footer {
  padding: 20px 25px 25px;
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-stay,
.btn-leave {
  flex: 1;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-stay {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
}

.btn-stay:hover {
  border-color: var(--gold-primary);
  background: rgba(212, 175, 55, 0.1);
}

.btn-leave {
  background: var(--gold-gradient);
  border: none;
  color: var(--bg-deep);
}

.btn-leave:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold);
}

@media (max-width: 480px) {
  .dialog-footer {
    flex-direction: column;
  }
}
</style>
