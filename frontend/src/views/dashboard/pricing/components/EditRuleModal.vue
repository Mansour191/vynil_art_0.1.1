<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content glass-card" @click.stop>
      <div class="modal-header">
        <h3 class="text-xl font-bold gold-text">
          <i class="fa-solid fa-edit me-2"></i>
          تعديل قاعدة التسعير
        </h3>
        <button class="close-btn" @click="$emit('close')">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="rule-form">
        <div class="form-group">
          <label class="form-label">اسم القاعدة</label>
          <input 
            v-model="rule.name" 
            type="text" 
            class="form-control" 
            placeholder="أدخل اسم القاعدة"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">نوع القاعدة</label>
          <select v-model="rule.type" class="form-control" required>
            <option value="">اختر نوع القاعدة</option>
            <option value="percentage">نسبة مئوية</option>
            <option value="fixed">قيمة ثابتة</option>
            <option value="formula">معادلة</option>
            <option value="conditional">شرطية</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">المنتجات المستهدفة</label>
          <select v-model="rule.targetProducts" class="form-control" multiple>
            <option value="">اختر المنتجات</option>
            <option v-for="product in products" :key="product.id" :value="product.id">
              {{ product.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">قيمة القاعدة</label>
          <input 
            v-model="rule.value" 
            type="number" 
            step="0.01" 
            class="form-control" 
            placeholder="أدخل القيمة"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">الشروط</label>
          <textarea 
            v-model="rule.conditions" 
            class="form-control" 
            rows="3"
            placeholder="أدخل الشروط (اختياري)"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">
            <input type="checkbox" v-model="rule.active" />
            قاعدة نشطة
          </label>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="$emit('close')">
            <i class="fa-solid fa-times me-2"></i>
            إلغاء
          </button>
          <button type="submit" class="btn-primary" :disabled="loading">
            <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-save'" class="me-2"></i>
            {{ loading ? 'جاري التحديث...' : 'تحديث القاعدة' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  rule: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'updated']);

const loading = ref(false);
const products = ref([]);

const editedRule = ref({ ...props.rule });

const handleSubmit = async () => {
  try {
    loading.value = true;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    emit('updated', { ...editedRule.value });
    emit('close');
  } catch (error) {
    console.error('Error updating rule:', error);
  } finally {
    loading.value = false;
  }
};

const loadProducts = async () => {
  try {
    // Simulate loading products
    products.value = [
      { id: 1, name: 'فينيل ديكوري' },
      { id: 2, name: 'فينيل جدران' },
      { id: 3, name: 'فينيل أرضيات' },
      { id: 4, name: 'فينيل سقف' }
    ];
  } catch (error) {
    console.error('Error loading products:', error);
  }
};

// Watch for prop changes
watch(() => props.rule, (newRule) => {
  editedRule.value = { ...newRule };
}, { deep: true });

onMounted(() => {
  loadProducts();
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid var(--border-light);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-light);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-dim);
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #f44336;
}

.rule-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: #fff;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-control {
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  padding: 12px;
  color: #fff;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-control[multiple] {
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.btn-primary {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4bc 100%);
  color: #000;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-card);
  color: #fff;
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  border-color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}
</style>
