<template>
  <div class="orders-manager">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <h1>إدارة الطلبات</h1>
        <p>متابعة ومعالجة طلبات العملاء والمبيعات</p>
      </div>
      <div class="header-actions">
        <button class="btn-export" @click="exportOrders">
          <i class="fa-solid fa-file-export"></i> تصدير
        </button>
        <button class="btn-primary" @click="openNewOrderModal">
          <i class="fa-solid fa-plus"></i> طلب جديد
        </button>
      </div>
    </header>

    <!-- Stats -->
    <StatCards :stats="orderStats" />

    <!-- Filters -->
    <div class="filters-card">
      <div class="search-bar">
        <i class="fa-solid fa-search search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="البحث برقم الطلب، اسم العميل، أو البريد الإلكتروني..."
          @input="debouncedSearch"
        />
        <button v-if="searchQuery" class="clear-search" @click="clearSearch">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>

      <div class="quick-filters">
        <select v-model="statusFilter" class="filter-select">
          <option value="">جميع الحالات</option>
          <option value="pending">قيد الانتظار</option>
          <option value="processing">قيد المعالجة</option>
          <option value="shipped">تم الشحن</option>
          <option value="delivered">تم التوصيل</option>
          <option value="cancelled">ملغي</option>
        </select>

        <select v-model="paymentFilter" class="filter-select">
          <option value="">جميع طرق الدفع</option>
          <option value="cash">الدفع عند الاستلام</option>
          <option value="card">بطاقة ائتمان</option>
          <option value="bank">تحويل بنكي</option>
        </select>

        <button class="btn-advanced" @click="showAdvancedFilters = !showAdvancedFilters">
          <i class="fa-solid fa-sliders-h"></i>
          فلترة متقدمة
        </button>

        <button class="btn-reset" @click="resetFilters">
          <i class="fa-solid fa-undo"></i>
        </button>
      </div>

      <!-- Advanced Filters Dropdown -->
      <transition name="slide-fade">
        <div v-if="showAdvancedFilters" class="advanced-filters-panel">
          <div class="filter-grid">
            <div class="filter-group">
              <label>نطاق السعر</label>
              <div class="range-inputs">
                <input v-model.number="priceRange.min" type="number" placeholder="من" />
                <input v-model.number="priceRange.max" type="number" placeholder="إلى" />
              </div>
            </div>
            <div class="filter-group">
              <label>المدينة</label>
              <input v-model="cityFilter" type="text" placeholder="مثلاً: سطيف" />
            </div>
          </div>
          <div class="filter-actions">
            <button class="btn-apply" @click="applyAdvancedFilters">تطبيق</button>
            <button class="btn-link" @click="resetAdvancedFilters">إعادة تعيين</button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Bulk Actions -->
    <div v-if="selectedOrders.length > 0" class="bulk-actions-bar">
      <div class="selection-info">
        <i class="fa-solid fa-check-double"></i>
        تم تحديد {{ selectedOrders.length }} طلب
      </div>
      <div class="bulk-buttons">
        <button @click="bulkUpdateStatus('processing')">تجهيز المحدد</button>
        <button @click="bulkUpdateStatus('shipped')">شحن المحدد</button>
        <button class="danger" @click="bulkUpdateStatus('cancelled')">إلغاء المحدد</button>
        <div class="divider"></div>
        <button class="secondary" @click="clearSelection">إلغاء التحديد</button>
      </div>
    </div>

    <!-- Orders Table -->
    <OrdersTable
      :orders="paginatedOrders"
      :columns="columns"
      :selected-orders="selectedOrders"
      :select-all="selectAll"
      :sort-key="sortKey"
      :sort-order="sortOrder"
      :active-order-menu="activeOrderMenu"
      @sort="handleSort"
      @view="viewOrder"
      @edit="editOrder"
      @toggle-select="toggleOrderSelection"
      @toggle-select-all="toggleSelectAll"
      @toggle-menu="toggleOrderMenu"
      @update-status="updateOrderStatus"
    />

    <!-- Pagination -->
    <Pagination
      v-model:current-page="currentPage"
      v-model:items-per-page="itemsPerPage"
      :total-items="filteredOrders.length"
    />

    <!-- Order Details Modal -->
    <OrderDetailsModal
      v-if="showOrderModal"
      :order="selectedOrder"
      @close="closeOrderModal"
      @update-status="updateOrderStatus"
      @print="printOrder"
      @send-invoice="sendInvoice"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { debounce } from 'lodash';
import StatCards from '@/components/common/StatCards.vue';
import Pagination from '@/components/common/Pagination.vue';
import OrdersTable from './components/OrdersTable.vue';
import OrderDetailsModal from './components/OrderDetailsModal.vue';
import CurrencyService from '@/integration/services/CurrencyService';

// State
const orders = ref([
  {
    id: 'ORD-1001',
    customer: 'أحمد محمد',
    email: 'ahmed@example.com',
    phone: '0663140341',
    date: '2024-03-15T10:30:00',
    total: 450,
    subtotal: 380,
    shipping: 20,
    tax: 50,
    status: 'pending',
    paymentMethod: 'cash',
    paymentStatus: 'unpaid',
    shippingAddress: { street: 'حي 100 مسكن', city: 'سطيف', country: 'الجزائر', zipCode: '19000' },
    products: [
      { id: 1, name: 'ملصق حائط زهور', price: 45, quantity: 2, sku: 'WAL-001', image: 'https://via.placeholder.com/50' },
      { id: 2, name: 'ملصق باب خشبي', price: 89, quantity: 1, sku: 'DR-002', image: 'https://via.placeholder.com/50' }
    ],
    timeline: [
      { status: 'pending', date: '2024-03-15T10:30:00', note: 'تم إنشاء الطلب بنجاح' }
    ]
  },
  {
    id: 'ORD-1002',
    customer: 'سارة أحمد',
    email: 'sara@example.com',
    phone: '0555987654',
    date: '2024-03-14T15:45:00',
    total: 280,
    subtotal: 240,
    shipping: 0,
    tax: 40,
    status: 'processing',
    paymentMethod: 'card',
    paymentStatus: 'paid',
    shippingAddress: { street: 'شارع الحرية', city: 'الجزائر العاصمة', country: 'الجزائر', zipCode: '16000' },
    products: [
      { id: 4, name: 'ملصق مطبخ فواكه', price: 65, quantity: 3, sku: 'KIT-004', image: 'https://via.placeholder.com/50' }
    ],
    timeline: [
      { status: 'pending', date: '2024-03-14T15:45:00', note: 'تم إنشاء الطلب بنجاح' },
      { status: 'processing', date: '2024-03-14T16:00:00', note: 'الطلب قيد التجهيز' }
    ]
  }
]);

const orderStats = ref([
  { label: 'إجمالي الطلبات', value: '1,284', icon: 'fa-solid fa-shopping-basket', color: '#1a1a2e', trend: 12 },
  { label: 'طلبات اليوم', value: '48', icon: 'fa-solid fa-calendar-day', color: '#d4af37', trend: 8 },
  { label: 'قيد المعالجة', value: '124', icon: 'fa-solid fa-spinner', color: '#2196f3', trend: -3 },
  { label: 'تم التوصيل', value: '1,056', icon: 'fa-solid fa-check-double', color: '#4caf50', trend: 15 }
]);

const columns = ref([
  { key: 'id', label: 'رقم الطلب', visible: true },
  { key: 'customer', label: 'العميل', visible: true },
  { key: 'date', label: 'التاريخ', visible: true },
  { key: 'total', label: 'الإجمالي', visible: true },
  { key: 'status', label: 'الحالة', visible: true },
  { key: 'paymentMethod', label: 'الدفع', visible: true }
]);

// Filters State
const searchQuery = ref('');
const statusFilter = ref('');
const paymentFilter = ref('');
const cityFilter = ref('');
const showAdvancedFilters = ref(false);
const priceRange = reactive({ min: null, max: null });

// Table State
const sortKey = ref('date');
const sortOrder = ref('desc');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const selectedOrders = ref([]);
const selectAll = ref(false);
const activeOrderMenu = ref(null);
const showOrderModal = ref(false);
const selectedOrder = ref(null);

// Computed
const filteredOrders = computed(() => {
  return orders.value.filter(order => {
    const matchesSearch = !searchQuery.value || 
      order.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      order.customer.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesStatus = !statusFilter.value || order.status === statusFilter.value;
    const matchesPayment = !paymentFilter.value || order.paymentMethod === paymentFilter.value;
    const matchesPrice = (!priceRange.min || order.total >= priceRange.min) && 
                         (!priceRange.max || order.total <= priceRange.max);
    const matchesCity = !cityFilter.value || 
                        order.shippingAddress?.city.toLowerCase().includes(cityFilter.value.toLowerCase());

    return matchesSearch && matchesStatus && matchesPayment && matchesPrice && matchesCity;
  });
});

const sortedOrders = computed(() => {
  const sorted = [...filteredOrders.value];
  sorted.sort((a, b) => {
    let aVal = a[sortKey.value];
    let bVal = b[sortKey.value];

    if (sortKey.value === 'total') return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal;
    if (sortKey.value === 'date') return sortOrder.value === 'asc' ? new Date(aVal) - new Date(bVal) : new Date(bVal) - new Date(aVal);

    aVal = String(aVal).toLowerCase();
    bVal = String(bVal).toLowerCase();
    return sortOrder.value === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
  });
  return sorted;
});

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  return sortedOrders.value.slice(start, start + itemsPerPage.value);
});

// Methods
const handleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const debouncedSearch = debounce(() => {
  currentPage.value = 1;
}, 300);

const clearSearch = () => {
  searchQuery.value = '';
  currentPage.value = 1;
};

const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  paymentFilter.value = '';
  priceRange.min = null;
  priceRange.max = null;
  cityFilter.value = '';
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const applyAdvancedFilters = () => {
  showAdvancedFilters.value = false;
  currentPage.value = 1;
};

const resetAdvancedFilters = () => {
  priceRange.min = null;
  priceRange.max = null;
  cityFilter.value = '';
  showAdvancedFilters.value = false;
};

const toggleOrderSelection = (id) => {
  const index = selectedOrders.value.indexOf(id);
  if (index === -1) selectedOrders.value.push(id);
  else selectedOrders.value.splice(index, 1);
  selectAll.value = selectedOrders.value.length === paginatedOrders.value.length;
};

const toggleSelectAll = () => {
  selectAll.value = !selectAll.value;
  selectedOrders.value = selectAll.value ? paginatedOrders.value.map(o => o.id) : [];
};

const clearSelection = () => {
  selectedOrders.value = [];
  selectAll.value = false;
};

const bulkUpdateStatus = (status) => {
  selectedOrders.value.forEach(id => {
    const order = orders.value.find(o => o.id === id);
    if (order) updateOrderStatus(order, status);
  });
  clearSelection();
};

const viewOrder = (order) => {
  selectedOrder.value = { ...order };
  showOrderModal.value = true;
};

const closeOrderModal = () => {
  showOrderModal.value = false;
  selectedOrder.value = null;
};

const editOrder = (order) => {
  console.log('Edit order:', order);
};

const updateOrderStatus = (order, status) => {
  order.status = status;
  order.timeline.push({
    status,
    date: new Date().toISOString(),
    note: `تم تحديث الحالة إلى ${status}`
  });
  activeOrderMenu.value = null;
};

const toggleOrderMenu = (id) => {
  activeOrderMenu.value = activeOrderMenu.value === id ? null : id;
};

const exportOrders = () => {
  alert('تم تصدير الطلبات بنجاح');
};

const openNewOrderModal = () => {
  alert('ميزة إنشاء طلب جديد قيد التطوير');
};

const printOrder = (order) => {
  alert(`طباعة الطلب #${order.id}`);
};

const sendInvoice = (order) => {
  alert(`إرسال فاتورة الطلب #${order.id}`);
};
</script>

<style scoped>
.orders-manager {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-content h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}

.header-content p {
  color: #6c757d;
  margin: 4px 0 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary, .btn-export {
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--gold-gradient);
  color: #1a1a2e;
  border: none;
}

.btn-export {
  background: white;
  color: #1a1a2e;
  border: 1px solid #dee2e6;
}

.filters-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.search-bar {
  position: relative;
  margin-bottom: 20px;
}

.search-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #adb5bd;
}

.search-bar input {
  width: 100%;
  padding: 12px 48px 12px 16px;
  border-radius: 12px;
  border: 1px solid #dee2e6;
  font-size: 15px;
  transition: all 0.3s;
}

.search-bar input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.1);
}

.clear-search {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  color: #adb5bd;
  cursor: pointer;
}

.quick-filters {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-select {
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid #dee2e6;
  font-size: 14px;
  cursor: pointer;
}

.btn-advanced, .btn-reset {
  padding: 10px 16px;
  border-radius: 10px;
  border: 1px solid #dee2e6;
  background: white;
  cursor: pointer;
}

.bulk-actions-bar {
  background: #1a1a2e;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  animation: slideIn 0.3s ease;
}

.bulk-buttons {
  display: flex;
  gap: 8px;
}

.bulk-buttons button {
  padding: 6px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  font-size: 13px;
}

.bulk-buttons button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.bulk-buttons button.danger { color: #ff5252; }
.bulk-buttons button.secondary { opacity: 0.7; }

.advanced-filters-panel {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.filter-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

.range-inputs {
  display: flex;
  gap: 8px;
}

.range-inputs input {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.filter-actions {
  margin-top: 20px;
  display: flex;
  gap: 12px;
}

.btn-apply {
  background: #1a1a2e;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 8px;
  cursor: pointer;
}

@keyframes slideIn {
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
