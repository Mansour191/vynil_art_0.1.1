<template>
  <transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-container delete-modal">
        <div class="modal-header">
          <h2>تأكيد الحذف</h2>
          <button class="close-modal" @click="$emit('close')">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>
            هل أنت متأكد من حذف المنتج 
            <strong>"{{ productName }}"</strong>؟
          </p>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="$emit('close')">إلغاء</button>
          <button class="btn-danger" @click="$emit('confirm')">حذف</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: { type: Boolean, required: true },
  productName: { type: String, default: '' }
});

defineEmits(['close', 'confirm']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  padding: 24px;
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  text-align: right;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.modal-header h2 {
  font-size: 20px;
  margin: 0;
  color: #1a1a2e;
}

.close-modal {
  border: none;
  background: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-secondary {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
}

.btn-danger {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: #f44336;
  color: white;
  cursor: pointer;
}
</style>
