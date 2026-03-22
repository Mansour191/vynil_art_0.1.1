<template>
  <transition name="modal">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-container view-modal">
        <div class="modal-header">
          <h2><i class="fa-solid fa-file-invoice"></i> تفاصيل الطلب #{{ order?.id }}</h2>
          <button class="close-modal" @click="$emit('close')">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>

        <div v-if="order" class="modal-body">
          <!-- معلومات العميل -->
          <div class="order-details-grid">
            <div class="detail-card">
              <h3><i class="fa-solid fa-user"></i> معلومات العميل</h3>
              <div class="detail-content">
                <p><strong>الاسم:</strong> {{ order.customer }}</p>
                <p><strong>البريد:</strong> {{ order.email }}</p>
                <p><strong>الهاتف:</strong> {{ order.phone }}</p>
              </div>
            </div>

            <div class="detail-card">
              <h3><i class="fa-solid fa-map-marker-alt"></i> عنوان الشحن</h3>
              <div class="detail-content">
                <p>{{ order.shippingAddress?.street }}</p>
                <p>
                  {{ order.shippingAddress?.city }},
                  {{ order.shippingAddress?.country }}
                </p>
                <p>{{ order.shippingAddress?.zipCode }}</p>
              </div>
            </div>

            <div class="detail-card">
              <h3><i class="fa-solid fa-credit-card"></i> معلومات الدفع</h3>
              <div class="detail-content">
                <p>
                  <strong>طريقة الدفع:</strong>
                  {{ getPaymentMethodText(order.paymentMethod) }}
                </p>
                <p>
                  <strong>حالة الدفع:</strong>
                  <span :class="['payment-status', order.paymentStatus]">{{
                    getPaymentStatusText(order.paymentStatus)
                  }}</span>
                </p>
                <p><strong>تاريخ الطلب:</strong> {{ formatDate(order.date) }}</p>
              </div>
            </div>
          </div>

          <!-- منتجات الطلب -->
          <div class="order-products">
            <h3>
              <i class="fa-solid fa-box"></i> المنتجات ({{ order.products?.length || 0 }})
            </h3>
            <table class="products-table">
              <thead>
                <tr>
                  <th>المنتج</th>
                  <th>السعر</th>
                  <th>الكمية</th>
                  <th>الإجمالي</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in order.products" :key="item.id">
                  <td>
                    <div class="product-info">
                      <img :src="item.image" :alt="item.name" />
                      <div>
                        <div class="product-name">{{ item.name }}</div>
                        <div class="product-sku">{{ item.sku }}</div>
                      </div>
                    </div>
                  </td>
                  <td>{{ item.price }} ر.س</td>
                  <td>{{ item.quantity }}</td>
                  <td>{{ item.price * item.quantity }} ر.س</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="3" class="text-left">المجموع الفرعي</td>
                  <td>{{ order.subtotal }} ر.س</td>
                </tr>
                <tr>
                  <td colspan="3" class="text-left">الشحن</td>
                  <td>{{ order.shipping }} ر.س</td>
                </tr>
                <tr>
                  <td colspan="3" class="text-left">الضريبة</td>
                  <td>{{ order.tax }} ر.س</td>
                </tr>
                <tr class="total-row">
                  <td colspan="3" class="text-left">الإجمالي</td>
                  <td>{{ order.total }} ر.س</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- سجل حالة الطلب -->
          <div class="order-timeline">
            <h3><i class="fa-solid fa-history"></i> سجل الحالة</h3>
            <div class="timeline">
              <div
                v-for="(event, index) in order.timeline"
                :key="index"
                class="timeline-item"
              >
                <div class="timeline-icon" :class="event.status">
                  <i :class="getTimelineIcon(event.status)"></i>
                </div>
                <div class="timeline-content">
                  <div class="timeline-header">
                    <span class="timeline-status">{{ getStatusText(event.status) }}</span>
                    <span class="timeline-date">{{ formatDateTime(event.date) }}</span>
                  </div>
                  <p class="timeline-note">{{ event.note }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="footer-actions">
            <select
              v-model="orderStatus"
              class="status-select"
              @change="$emit('update-status', order, orderStatus)"
            >
              <option value="pending">قيد الانتظار</option>
              <option value="processing">قيد المعالجة</option>
              <option value="shipped">تم الشحن</option>
              <option value="delivered">تم التوصيل</option>
              <option value="cancelled">ملغي</option>
            </select>
            <button class="btn-print" @click="$emit('print', order)">
              <i class="fa-solid fa-print"></i> طباعة
            </button>
            <button class="btn-invoice" @click="$emit('send-invoice', order)">
              <i class="fa-solid fa-envelope"></i> إرسال الفاتورة
            </button>
          </div>
          <button class="btn-close" @click="$emit('close')">إغلاق</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue';
import { formatDate, formatDateTime } from '@/integration/utils/helpers';

const props = defineProps({
  order: { type: Object, default: null },
});

const emit = defineEmits(['close', 'update-status', 'print', 'send-invoice']);

const orderStatus = ref(props.order?.status || 'pending');

watch(() => props.order?.status, (newStatus) => {
  if (newStatus) orderStatus.value = newStatus;
});

const getStatusText = (status) => {
  const texts = {
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التوصيل',
    cancelled: 'ملغي',
    refunded: 'مسترجع',
  };
  return texts[status] || status;
};

const getPaymentStatusText = (status) => {
  const texts = {
    paid: 'مدفوع',
    unpaid: 'غير مدفوع',
    partial: 'مدفوع جزئياً',
    refunded: 'مسترجع',
  };
  return texts[status] || status;
};

const getPaymentMethodText = (method) => {
  const texts = {
    cash: 'الدفع عند الاستلام',
    card: 'بطاقة ائتمان',
    bank: 'تحويل بنكي',
    wallet: 'محفظة إلكترونية',
  };
  return texts[method] || method;
};

const getTimelineIcon = (status) => {
  const icons = {
    pending: 'fa-solid fa-clock',
    processing: 'fa-solid fa-spinner',
    shipped: 'fa-solid fa-truck',
    delivered: 'fa-solid fa-check-circle',
    cancelled: 'fa-solid fa-ban',
    refunded: 'fa-solid fa-undo',
  };
  return icons[status] || 'fa-solid fa-info-circle';
};
</script>

<style scoped>
/* Styles extracted from OrdersManager.vue for modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: white;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  border-radius: 20px;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  font-size: 20px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #1a1a2e;
}

.close-modal {
  background: #f8f9fa;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}

.close-modal:hover {
  background: #eee;
  transform: rotate(90deg);
}

.modal-body {
  padding: 24px;
}

.order-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.detail-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.detail-card h3 {
  font-size: 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
}

.detail-content p {
  margin-bottom: 8px;
  font-size: 14px;
  color: #444;
}

.payment-status {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.payment-status.paid { background: #e8f5e9; color: #2e7d32; }
.payment-status.unpaid { background: #ffebee; color: #c62828; }

.order-products table {
  width: 100%;
  border-collapse: collapse;
}

.order-products th {
  text-align: right;
  padding: 12px;
  border-bottom: 2px solid #eee;
  font-size: 14px;
}

.order-products td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-info img {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.total-row td {
  font-weight: 700;
  font-size: 18px;
  color: #1a1a2e;
  border-top: 2px solid #eee;
}

.order-timeline {
  margin-top: 30px;
}

.timeline {
  margin-top: 20px;
  border-right: 2px solid #eee;
  padding-right: 20px;
}

.timeline-item {
  position: relative;
  margin-bottom: 24px;
}

.timeline-icon {
  position: absolute;
  right: -31px;
  top: 0;
  width: 20px;
  height: 20px;
  background: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
}

.timeline-icon.delivered { border-color: #4caf50; color: #4caf50; }
.timeline-icon.processing { border-color: #2196f3; color: #2196f3; }

.modal-footer {
  padding: 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  bottom: 0;
  background: white;
}

.footer-actions {
  display: flex;
  gap: 12px;
}

.status-select {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.btn-print, .btn-invoice, .btn-close {
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-print { background: #f8f9fa; border: 1px solid #ddd; }
.btn-invoice { background: #1a1a2e; color: white; border: none; }
.btn-close { background: #eee; border: none; }
</style>
