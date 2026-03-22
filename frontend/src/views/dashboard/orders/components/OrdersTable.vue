<template>
  <div class="table-container">
    <table class="orders-table">
      <thead>
        <tr>
          <th class="col-select">
            <input type="checkbox" :checked="selectAll" @change="$emit('toggle-select-all')" />
          </th>
          <th v-for="col in columns" :key="col.key" @click="$emit('sort', col.key)" class="sortable">
            {{ col.label }}
            <i v-if="sortKey === col.key" :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"></i>
          </th>
          <th class="col-actions">الإجراءات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id" @click="$emit('view', order)">
          <td class="col-select" @click.stop>
            <input
              type="checkbox"
              :checked="selectedOrders.includes(order.id)"
              @change="$emit('toggle-select', order.id)"
            />
          </td>
          <td v-for="col in columns" :key="col.key">
            <template v-if="col.key === 'id'">
              <span class="order-id">#{{ order.id }}</span>
            </template>
            <template v-else-if="col.key === 'customer'">
              <div class="customer-info">
                <span class="customer-name">{{ order.customer }}</span>
                <span class="customer-email">{{ order.email }}</span>
              </div>
            </template>
            <template v-else-if="col.key === 'date'">
              <div class="date-info">
                <span class="date">{{ formatDate(order.date) }}</span>
                <span class="time">{{ formatTime(order.date) }}</span>
              </div>
            </template>
            <template v-else-if="col.key === 'total'">
              <span class="order-total">{{ formatAmount(order.total) }}</span>
            </template>
            <template v-else-if="col.key === 'status'">
              <span :class="['status-badge', order.status]">
                {{ getStatusText(order.status) }}
              </span>
            </template>
            <template v-else-if="col.key === 'paymentMethod'">
              <div class="payment-info">
                <i :class="getPaymentIcon(order.paymentMethod)"></i>
                <span>{{ getPaymentMethodText(order.paymentMethod) }}</span>
              </div>
            </template>
            <template v-else>
              {{ order[col.key] }}
            </template>
          </td>
          <td class="col-actions" @click.stop>
            <div class="action-buttons">
              <button class="btn-icon view" title="عرض" @click="$emit('view', order)">
                <i class="fa-solid fa-eye"></i>
              </button>
              <button class="btn-icon edit" title="تعديل" @click="$emit('edit', order)">
                <i class="fa-solid fa-edit"></i>
              </button>
              <div class="dropdown">
                <button class="btn-icon more" @click="$emit('toggle-menu', order.id)">
                  <i class="fa-solid fa-ellipsis-v"></i>
                </button>
                <div v-if="activeOrderMenu === order.id" class="dropdown-menu">
                  <button @click="$emit('update-status', order, 'processing')">تجهيز الطلب</button>
                  <button @click="$emit('update-status', order, 'shipped')">تم الشحن</button>
                  <button @click="$emit('update-status', order, 'delivered')">تم التوصيل</button>
                  <div class="divider"></div>
                  <button class="danger" @click="$emit('update-status', order, 'cancelled')">إلغاء الطلب</button>
                </div>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { formatDate, formatTime } from '@/integration/utils/helpers';
import CurrencyService from '@/integration/services/CurrencyService';

defineProps({
  orders: { type: Array, required: true },
  columns: { type: Array, required: true },
  selectedOrders: { type: Array, required: true },
  selectAll: { type: Boolean, default: false },
  sortKey: { type: String, default: 'id' },
  sortOrder: { type: String, default: 'desc' },
  activeOrderMenu: { type: [String, Number], default: null },
});

defineEmits([
  'sort',
  'view',
  'edit',
  'toggle-select',
  'toggle-select-all',
  'toggle-menu',
  'update-status',
]);

const formatAmount = (amount) => CurrencyService.formatAmount(amount);

const getStatusText = (status) => {
  const map = {
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التوصيل',
    cancelled: 'ملغي',
    refunded: 'مسترجع',
  };
  return map[status] || status;
};

const getPaymentMethodText = (method) => {
  const map = {
    cash: 'الدفع عند الاستلام',
    card: 'بطاقة ائتمان',
    bank: 'تحويل بنكي',
    wallet: 'محفظة إلكترونية',
  };
  return map[method] || method;
};

const getPaymentIcon = (method) => {
  const map = {
    cash: 'fa-solid fa-money-bill-wave',
    card: 'fa-solid fa-credit-card',
    bank: 'fa-solid fa-university',
    wallet: 'fa-solid fa-wallet',
  };
  return map[method] || 'fa-solid fa-money-bill';
};
</script>

<style scoped>
.table-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  text-align: right;
}

.orders-table th {
  padding: 16px;
  background: #f8f9fa;
  color: #1a1a2e;
  font-weight: 700;
  font-size: 14px;
  border-bottom: 2px solid #eee;
}

.orders-table th.sortable {
  cursor: pointer;
  transition: background 0.2s;
}

.orders-table th.sortable:hover {
  background: #eee;
}

.orders-table td {
  padding: 16px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.orders-table tr {
  transition: background 0.2s;
  cursor: pointer;
}

.orders-table tr:hover {
  background: #fcfcfc;
}

.order-id {
  font-weight: 700;
  color: #d4af37;
}

.customer-info {
  display: flex;
  flex-direction: column;
}

.customer-name {
  font-weight: 600;
  color: #1a1a2e;
}

.customer-email {
  font-size: 12px;
  color: #6c757d;
}

.date-info {
  display: flex;
  flex-direction: column;
}

.time {
  font-size: 12px;
  color: #6c757d;
}

.order-total {
  font-weight: 700;
  color: #1a1a2e;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.pending { background: #fff8e1; color: #ff8f00; }
.status-badge.processing { background: #e3f2fd; color: #1565c0; }
.status-badge.shipped { background: #f3e5f5; color: #7b1fa2; }
.status-badge.delivered { background: #e8f5e9; color: #2e7d32; }
.status-badge.cancelled { background: #ffebee; color: #c62828; }

.payment-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #444;
}

.payment-info i {
  color: #6c757d;
}

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

.btn-icon:hover {
  background: #eee;
  color: #1a1a2e;
}

.btn-icon.view:hover { color: #2196f3; background: rgba(33, 150, 243, 0.1); }
.btn-icon.edit:hover { color: #4caf50; background: rgba(76, 175, 80, 0.1); }

.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-width: 160px;
  padding: 8px;
  z-index: 100;
}

.dropdown-menu button {
  width: 100%;
  padding: 10px 16px;
  border: none;
  background: none;
  text-align: right;
  font-size: 13px;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.2s;
}

.dropdown-menu button:hover {
  background: #f8f9fa;
}

.dropdown-menu button.danger {
  color: #f44336;
}

.divider {
  height: 1px;
  background: #eee;
  margin: 8px 0;
}
</style>
