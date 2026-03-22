<template>
  <div class="table-container">
    <table class="products-table">
      <thead>
        <tr>
          <th @click="$emit('sort', 'name')" class="sortable">
            المنتج
            <i v-if="sortKey === 'name'" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th @click="$emit('sort', 'category')" class="sortable">
            التصنيف
            <i v-if="sortKey === 'category'" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th @click="$emit('sort', 'price')" class="sortable">
            السعر
            <i v-if="sortKey === 'price'" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th @click="$emit('sort', 'stock')" class="sortable">
            المخزون
            <i v-if="sortKey === 'stock'" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th @click="$emit('sort', 'sales')" class="sortable">
            المبيعات
            <i v-if="sortKey === 'sales'" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th>الحالة</th>
          <th class="col-actions">الإجراءات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id" @click="$emit('view', product)">
          <td>
            <div class="product-cell">
              <img :src="product.image" :alt="product.name" class="product-img" />
              <div class="product-info">
                <span class="product-name">{{ product.name }}</span>
                <span class="product-sku">{{ product.sku }}</span>
              </div>
            </div>
          </td>
          <td>
            <span class="category-badge">{{ getCategoryLabel(product.category) }}</span>
          </td>
          <td>
            <span class="price">{{ formatAmount(product.price) }}</span>
          </td>
          <td>
            <span :class="['stock-status', getStockClass(product.stock)]">
              {{ product.stock }} قطعة
            </span>
          </td>
          <td>{{ product.sales || 0 }}</td>
          <td>
            <span :class="['status-badge', product.active ? 'active' : 'inactive']">
              {{ product.active ? 'نشط' : 'غير نشط' }}
            </span>
          </td>
          <td class="col-actions" @click.stop>
            <div class="action-buttons">
              <button class="btn-icon view" title="عرض" @click="$emit('view', product)">
                <i class="fa-solid fa-eye"></i>
              </button>
              <button class="btn-icon edit" title="تعديل" @click="$emit('edit', product)">
                <i class="fa-solid fa-edit"></i>
              </button>
              <button class="btn-icon delete" title="حذف" @click="$emit('delete', product)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import CurrencyService from '@/integration/services/CurrencyService';

defineProps({
  products: { type: Array, required: true },
  sortKey: { type: String, default: 'name' },
  sortOrder: { type: String, default: 'asc' },
});

defineEmits(['sort', 'view', 'edit', 'delete']);

const formatAmount = (amount) => CurrencyService.formatAmount(amount);

const getCategoryLabel = (category) => {
  const map = {
    furniture: 'أثاث',
    doors: 'أبواب',
    walls: 'جدران',
    ceilings: 'أسقف',
    tiles: 'بلاط',
    kitchens: 'مطابخ',
    cars: 'سيارات',
  };
  return map[category] || category;
};

const getStockClass = (stock) => {
  if (stock === 0) return 'out-of-stock';
  if (stock <= 10) return 'low-stock';
  return 'in-stock';
};
</script>

<style scoped>
.table-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
}

.products-table th {
  padding: 16px;
  background: #f8f9fa;
  color: #1a1a2e;
  font-weight: 700;
  font-size: 14px;
  border-bottom: 2px solid #eee;
}

.products-table th.sortable {
  cursor: pointer;
}

.products-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.products-table tr:hover {
  background: #fcfcfc;
  cursor: pointer;
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
}

.product-info {
  display: flex;
  flex-direction: column;
}

.product-name {
  font-weight: 600;
  color: #1a1a2e;
}

.product-sku {
  font-size: 12px;
  color: #6c757d;
}

.category-badge {
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 20px;
  font-size: 12px;
  color: #444;
}

.stock-status.out-of-stock { color: #f44336; font-weight: 700; }
.stock-status.low-stock { color: #ff9800; font-weight: 600; }
.stock-status.in-stock { color: #4caf50; }

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.active { background: #e8f5e9; color: #2e7d32; }
.status-badge.inactive { background: #ffebee; color: #c62828; }

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8f9fa;
  color: #6c757d;
}

.btn-icon:hover { background: #eee; color: #1a1a2e; }
.btn-icon.delete:hover { color: #f44336; background: rgba(244, 67, 54, 0.1); }
</style>
