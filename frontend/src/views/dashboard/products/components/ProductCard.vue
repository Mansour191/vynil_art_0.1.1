<template>
  <div class="product-card">
    <div class="card-image">
      <img :src="product.image" :alt="product.name" />
      <div class="card-actions">
        <button class="btn-circle" @click="$emit('view', product)" title="عرض">
          <i class="fa-solid fa-eye"></i>
        </button>
        <button class="btn-circle" @click="$emit('edit', product)" title="تعديل">
          <i class="fa-solid fa-edit"></i>
        </button>
        <button class="btn-circle danger" @click="$emit('delete', product)" title="حذف">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-header">
        <span class="sku">{{ product.sku }}</span>
        <span :class="['status-dot', product.active ? 'active' : 'inactive']"></span>
      </div>
      <h3>{{ product.name }}</h3>
      <p class="category">{{ categoryLabel }}</p>
      <div class="card-footer">
        <span class="price">{{ formatAmount(product.price) }}</span>
        <span :class="['stock', getStockClass(product.stock)]">{{ product.stock }} قطعة</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import CurrencyService from '@/integration/services/CurrencyService';

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  categoryLabel: {
    type: String,
    default: ''
  }
});

defineEmits(['view', 'edit', 'delete']);

const formatAmount = (val) => CurrencyService.formatAmount(val);
const getStockClass = (stock) => stock === 0 ? 'out' : (stock <= 10 ? 'low' : 'in');
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.card-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-actions {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 26, 46, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.3s;
}

.product-card:hover .card-actions {
  opacity: 1;
}

.btn-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: white;
  cursor: pointer;
  transition: transform 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-circle:hover {
  transform: scale(1.1);
}

.btn-circle.danger {
  color: #f44336;
}

.card-body {
  padding: 16px;
  text-align: right;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.sku {
  font-size: 12px;
  color: #6c757d;
  font-family: monospace;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.active {
  background: #4caf50;
}

.status-dot.inactive {
  background: #f44336;
}

.card-body h3 {
  font-size: 16px;
  margin: 0 0 4px;
  color: #1a1a2e;
}

.category {
  font-size: 13px;
  color: #6c757d;
  margin-bottom: 12px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #eee;
  padding-top: 12px;
}

.price {
  font-weight: 700;
  color: #d4af37;
  font-size: 18px;
}

.stock {
  font-size: 12px;
  font-weight: 600;
}

.stock.in {
  color: #4caf50;
}

.stock.low {
  color: #ff9800;
}

.stock.out {
  color: #f44336;
}
</style>
