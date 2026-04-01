<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-card variant="elevated" class="mb-6">
      <v-card-text class="pa-4">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold mb-2">إدارة الطلبات</h1>
            <p class="text-body-2 text-medium-emphasis mb-0">متابعة ومعالجة طلبات العملاء والمبيعات</p>
          </div>
          <div class="d-flex ga-2">
            <v-btn
              @click="exportOrders"
              variant="tonal"
              prepend-icon="mdi-file-export"
            >
              تصدير
            </v-btn>
            <v-btn
              @click="openNewOrderModal"
              variant="elevated"
              color="primary"
              prepend-icon="mdi-plus"
            >
              طلب جديد
            </v-btn>
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Stats -->
    <v-row class="mb-6">
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="primary">
          <v-card-text class="pa-4 text-center">
            <v-icon size="32" color="primary" class="mb-2">mdi-shopping-basket</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.totalOrders }}</div>
            <div class="text-caption text-medium-emphasis">إجمالي الطلبات</div>
            <v-chip size="small" :color="stats.totalOrdersTrend > 0 ? 'success' : 'error'" class="mt-2">
              {{ stats.totalOrdersTrend > 0 ? '+' : '' }}{{ stats.totalOrdersTrend }}%
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="info">
          <v-card-text class="pa-4 text-center">
            <v-icon size="32" color="info" class="mb-2">mdi-calendar-day</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.todayOrders }}</div>
            <div class="text-caption text-medium-emphasis">طلبات اليوم</div>
            <v-chip size="small" :color="stats.todayOrdersTrend > 0 ? 'success' : 'error'" class="mt-2">
              {{ stats.todayOrdersTrend > 0 ? '+' : '' }}{{ stats.todayOrdersTrend }}%
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="warning">
          <v-card-text class="pa-4 text-center">
            <v-icon size="32" color="warning" class="mb-2">mdi-cogs</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.processingOrders }}</div>
            <div class="text-caption text-medium-emphasis">قيد المعالجة</div>
            <v-chip size="small" :color="stats.processingOrdersTrend > 0 ? 'success' : 'error'" class="mt-2">
              {{ stats.processingOrdersTrend > 0 ? '+' : '' }}{{ stats.processingOrdersTrend }}%
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="success">
          <v-card-text class="pa-4 text-center">
            <v-icon size="32" color="success" class="mb-2">mdi-check-double</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.deliveredOrders }}</div>
            <div class="text-caption text-medium-emphasis">تم التوصيل</div>
            <v-chip size="small" :color="stats.deliveredOrdersTrend > 0 ? 'success' : 'error'" class="mt-2">
              {{ stats.deliveredOrdersTrend > 0 ? '+' : '' }}{{ stats.deliveredOrdersTrend }}%
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-card variant="elevated" class="mb-6">
      <v-card-title class="pa-4">
        <v-icon color="primary" class="me-2">mdi-filter</v-icon>
        البحث والتصفية
      </v-card-title>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="searchQuery"
              label="البحث عن طلب"
              placeholder="رقم الطلب، اسم العميل، أو البريد الإلكتروني..."
              prepend-inner-icon="mdi-magnify"
              clearable
              @click:clear="clearSearch"
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="statusFilter"
              label="الحالة"
              :items="statusOptions"
              item-title="text"
              item-value="value"
              clearable
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-select
              v-model="paymentFilter"
              label="طريقة الدفع"
              :items="paymentOptions"
              item-title="text"
              item-value="value"
              clearable
              variant="outlined"
              density="compact"
            />
          </v-col>
          <v-col cols="12" md="2">
            <v-btn
              @click="resetFilters"
              variant="tonal"
              prepend-icon="mdi-refresh"
              block
            >
              إعادة تعيين
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Orders Table -->
    <v-card variant="elevated" class="mb-6">
      <v-card-text class="pa-0">
        <v-data-table
          :headers="tableHeaders"
          :items="paginatedOrders"
          :loading="loading"
          :sort-by="sortKey"
          :sort-desc="sortOrder === 'desc'"
          @update:sort-by="handleSort"
          show-select
          v-model="selectedOrders"
          item-value="id"
          density="comfortable"
        >
          <template v-slot:item.status="{ item }">
            <v-chip
              :color="getStatusColor(item.status)"
              size="small"
              variant="tonal"
            >
              {{ getStatusText(item.status) }}
            </v-chip>
          </template>
          
          <template v-slot:item.paymentMethod="{ item }">
            <v-icon
              :icon="getPaymentIcon(item.paymentMethod)"
              :color="getPaymentColor(item.paymentMethod)"
              size="small"
              class="me-2"
            />
            {{ getPaymentText(item.paymentMethod) }}
          </template>
          
          <template v-slot:item.total="{ item }">
            <div class="font-weight-bold">
              {{ formatCurrency(item.total) }}
            </div>
          </template>
          
          <template v-slot:item.actions="{ item }">
            <v-btn
              @click="viewOrder(item)"
              icon="mdi-eye"
              variant="text"
              size="small"
              class="me-1"
            />
            <v-btn
              @click="editOrder(item)"
              icon="mdi-pencil"
              variant="text"
              size="small"
              class="me-1"
            />
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  icon="mdi-dots-vertical"
                  variant="text"
                  size="small"
                />
              </template>
              <v-list>
                <v-list-item @click="updateOrderStatus(item, 'shipped')">
                  <template v-slot:prepend>
                    <v-icon>mdi-truck</v-icon>
                  </template>
                  تم الشحن
                </v-list-item>
                <v-list-item @click="sendInvoice(item)">
                  <template v-slot:prepend>
                    <v-icon>mdi-email</v-icon>
                  </template>
                  إرسال فاتورة
                </v-list-item>
                <v-list-item @click="printOrder(item)">
                  <template v-slot:prepend>
                    <v-icon>mdi-printer</v-icon>
                  </template>
                  طباعة
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Pagination -->
    <v-card variant="tonal">
      <v-card-text class="pa-4">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :items-per-page="itemsPerPage"
          :total-visible="7"
          @update:model-value="handlePageChange"
        />
      </v-card-text>
    </v-card>

    <!-- Order Details Modal -->
    <v-dialog v-model="showOrderModal" max-width="800">
      <v-card>
        <v-card-title class="pa-4">
          <div class="d-flex align-center">
            <v-icon color="primary" class="me-2">mdi-receipt</v-icon>
            تفاصيل الطلب
          </div>
          <v-spacer />
          <v-btn
            @click="closeOrderModal"
            icon="mdi-close"
            variant="text"
          />
        </v-card-title>
        
        <v-card-text v-if="selectedOrder" class="pa-4">
          <v-row>
            <v-col cols="12" md="6">
              <v-card variant="tonal" class="mb-4">
                <v-card-title class="text-subtitle-1">معلومات العميل</v-card-title>
                <v-card-text>
                  <div class="mb-2">
                    <strong>الاسم:</strong> {{ selectedOrder.customer }}
                  </div>
                  <div class="mb-2">
                    <strong>البريد:</strong> {{ selectedOrder.email }}
                  </div>
                  <div class="mb-2">
                    <strong>الهاتف:</strong> {{ selectedOrder.phone }}
                  </div>
                  <div>
                    <strong>العنوان:</strong><br>
                    {{ selectedOrder.shippingAddress?.street }}<br>
                    {{ selectedOrder.shippingAddress?.city }}, {{ selectedOrder.shippingAddress?.country }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-card variant="tonal" class="mb-4">
                <v-card-title class="text-subtitle-1">معلومات الطلب</v-card-title>
                <v-card-text>
                  <div class="mb-2">
                    <strong>رقم الطلب:</strong> {{ selectedOrder.id }}
                  </div>
                  <div class="mb-2">
                    <strong>التاريخ:</strong> {{ formatDate(selectedOrder.date) }}
                  </div>
                  <div class="mb-2">
                    <strong>الحالة:</strong>
                    <v-chip
                      :color="getStatusColor(selectedOrder.status)"
                      size="small"
                      variant="tonal"
                    >
                      {{ getStatusText(selectedOrder.status) }}
                    </v-chip>
                  </div>
                  <div class="mb-2">
                    <strong>طريقة الدفع:</strong>
                    <v-icon
                      :icon="getPaymentIcon(selectedOrder.paymentMethod)"
                      :color="getPaymentColor(selectedOrder.paymentMethod)"
                      size="small"
                      class="me-2"
                    />
                    {{ getPaymentText(selectedOrder.paymentMethod) }}
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          
          <v-divider class="my-4" />
          
          <!-- Order Products -->
          <v-card variant="tonal">
            <v-card-title class="text-subtitle-1 mb-4">المنتجات</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item v-for="product in selectedOrder.products" :key="product.id">
                  <template v-slot:prepend>
                    <v-avatar size="40" :image="product.image" />
                  </template>
                  <v-list-item-title>
                    {{ product.name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    SKU: {{ product.sku }} | الكمية: {{ product.quantity }}
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <div class="text-end">
                      <div class="font-weight-bold">{{ formatCurrency(product.price) }}</div>
                      <div class="text-caption text-medium-emphasis">
                        {{ formatCurrency(product.price * product.quantity) }}
                      </div>
                    </div>
                  </template>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
          
          <!-- Order Summary -->
          <v-row class="mt-4">
            <v-col cols="12" md="6" offset-md="6">
              <v-card variant="tonal" color="primary">
                <v-card-title class="text-subtitle-1">ملخص الطلب</v-card-title>
                <v-card-text>
                  <div class="d-flex justify-space-between mb-2">
                    <span>الإجمالي الفرعي:</span>
                    <span>{{ formatCurrency(selectedOrder.subtotal) }}</span>
                  </div>
                  <div class="d-flex justify-space-between mb-2">
                    <span>الشحن:</span>
                    <span>{{ formatCurrency(selectedOrder.shipping || 0) }}</span>
                  </div>
                  <div class="d-flex justify-space-between mb-2">
                    <span>الضريبة:</span>
                    <span>{{ formatCurrency(selectedOrder.tax || 0) }}</span>
                  </div>
                  <v-divider class="my-2" />
                  <div class="d-flex justify-space-between">
                    <strong class="text-h6">الإجمالي:</strong>
                    <strong class="text-h6 text-primary">{{ formatCurrency(selectedOrder.total) }}</strong>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn @click="closeOrderModal" variant="tonal">إغلاق</v-btn>
          <v-btn @click="printOrder(selectedOrder)" color="primary" prepend-icon="mdi-printer">
            طباعة
          </v-btn>
          <v-btn @click="sendInvoice(selectedOrder)" color="success" prepend-icon="mdi-email">
            إرسال فاتورة
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { debounce } from 'lodash';

// State
const loading = ref(false);
const orders = ref([]);
const searchQuery = ref('');
const statusFilter = ref('');
const paymentFilter = ref('');
const sortKey = ref('date');
const sortOrder = ref('desc');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const selectedOrders = ref([]);
const showOrderModal = ref(false);
const selectedOrder = ref(null);

// Stats - will be loaded from API
const stats = ref({
  totalOrders: 0,
  totalOrdersTrend: 0,
  todayOrders: 0,
  todayOrdersTrend: 0,
  processingOrders: 0,
  processingOrdersTrend: 0,
  deliveredOrders: 0,
  deliveredOrdersTrend: 0
});

// Options
const statusOptions = [
  { text: 'جميع الحالات', value: '' },
  { text: 'قيد الانتظار', value: 'pending' },
  { text: 'قيد المعالجة', value: 'processing' },
  { text: 'تم الشحن', value: 'shipped' },
  { text: 'تم التوصيل', value: 'delivered' },
  { text: 'ملغي', value: 'cancelled' }
];

const paymentOptions = [
  { text: 'جميع طرق الدفع', value: '' },
  { text: 'الدفع عند الاستلام', value: 'cash' },
  { text: 'بطاقة ائتمان', value: 'card' },
  { text: 'تحويل بنكي', value: 'bank' },
  { text: 'الدفع الإلكتروني', value: 'electronic' }
];

// Table Headers
const tableHeaders = [
  { title: 'رقم الطلب', key: 'id', sortable: true },
  { title: 'العميل', key: 'customer', sortable: true },
  { title: 'التاريخ', key: 'date', sortable: true },
  { title: 'الإجمالي', key: 'total', sortable: true },
  { title: 'الحالة', key: 'status', sortable: true },
  { title: 'الدفع', key: 'paymentMethod', sortable: true },
  { title: 'الإجراءات', key: 'actions', sortable: false }
];

// Computed
const filteredOrders = computed(() => {
  return orders.value.filter(order => {
    const matchesSearch = !searchQuery.value || 
      order.id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      order.customer.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesStatus = !statusFilter.value || order.status === statusFilter.value;
    const matchesPayment = !paymentFilter.value || order.paymentMethod === paymentFilter.value;
    
    return matchesSearch && matchesStatus && matchesPayment;
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

const totalPages = computed(() => {
  return Math.ceil(filteredOrders.value.length / itemsPerPage.value);
});

// Methods
const handleSort = (column) => {
  if (sortKey.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = column;
    sortOrder.value = 'asc';
  }
};

const handlePageChange = (page) => {
  currentPage.value = page;
};

const clearSearch = () => {
  searchQuery.value = '';
  currentPage.value = 1;
};

const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  paymentFilter.value = '';
  currentPage.value = 1;
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

const updateOrderStatus = async (order, status) => {
  try {
    // Import OrdersService dynamically
    const { default: OrdersService } = await import('./OrdersService.js');
    
    // Update status via API
    const response = await OrdersService.updateOrderStatus(order.id, status);
    
    if (response.success) {
      // Update local state
      const index = orders.value.findIndex(o => o.id === order.id);
      if (index !== -1) {
        orders.value[index].status = status;
        orders.value[index].timeline.push({
          status,
          date: new Date().toISOString(),
          note: `تم تحديث الحالة إلى ${status}`
        });
      }
    } else {
      console.error('Failed to update order status:', response.error);
      // Fallback to local update
      const index = orders.value.findIndex(o => o.id === order.id);
      if (index !== -1) {
        orders.value[index].status = status;
        orders.value[index].timeline.push({
          status,
          date: new Date().toISOString(),
          note: `تم تحديث الحالة إلى ${status}`
        });
      }
    }
  } catch (error) {
    console.error('Error updating order status:', error);
    // Fallback to local update
    const index = orders.value.findIndex(o => o.id === order.id);
    if (index !== -1) {
      orders.value[index].status = status;
      orders.value[index].timeline.push({
        status,
        date: new Date().toISOString(),
        note: `تم تحديث الحالة إلى ${status}`
      });
    }
  }
};

const printOrder = (order) => {
  window.print();
};

const sendInvoice = async (order) => {
  try {
    // Import OrdersService dynamically
    const { default: OrdersService } = await import('./OrdersService.js');
    
    // Send invoice via API
    const response = await OrdersService.sendInvoice(order.id, {
      email: order.email,
      customerName: order.customer
    });
    
    if (response.success) {
      console.log('Invoice sent successfully:', response.message);
      // Show success notification
      // TODO: Add notification system
    } else {
      console.error('Failed to send invoice:', response.error);
      // Show error notification
      // TODO: Add notification system
    }
  } catch (error) {
    console.error('Error sending invoice:', error);
    // Show error notification
    // TODO: Add notification system
  }
};

const exportOrders = async () => {
  try {
    // Import OrdersService dynamically
    const { default: OrdersService } = await import('./OrdersService.js');
    
    // Export orders via API
    const response = await OrdersService.exportOrders({
      search: searchQuery.value,
      status: statusFilter.value,
      paymentMethod: paymentFilter.value,
      sortBy: sortKey.value,
      sortOrder: sortOrder.value
    });
    
    if (response.success) {
      console.log('Orders exported successfully:', response.message);
      // TODO: Handle file download
      if (response.data.downloadUrl) {
        window.open(response.data.downloadUrl, '_blank');
      }
    } else {
      console.error('Failed to export orders:', response.error);
      // Show error notification
      // TODO: Add notification system
    }
  } catch (error) {
    console.error('Error exporting orders:', error);
    // Show error notification
    // TODO: Add notification system
  }
};

const openNewOrderModal = () => {
  console.log('Open new order modal');
};

// Helper Functions
const getStatusColor = (status) => {
  const colors = {
    pending: 'warning',
    processing: 'info',
    shipped: 'primary',
    delivered: 'success',
    cancelled: 'error'
  };
  return colors[status] || 'grey';
};

const getStatusText = (status) => {
  const texts = {
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التوصيل',
    cancelled: 'ملغي'
  };
  return texts[status] || status;
};

const getPaymentIcon = (method) => {
  const icons = {
    cash: 'mdi-cash',
    card: 'mdi-credit-card',
    bank: 'mdi-bank',
    electronic: 'mdi-wallet'
  };
  return icons[method] || 'mdi-help-circle';
};

const getPaymentColor = (method) => {
  const colors = {
    cash: 'success',
    card: 'primary',
    bank: 'info',
    electronic: 'warning'
  };
  return colors[method] || 'grey';
};

const getPaymentText = (method) => {
  const texts = {
    cash: 'الدفع عند الاستلام',
    card: 'بطاقة ائتمان',
    bank: 'تحويل بنكي',
    electronic: 'الدفع الإلكتروني'
  };
  return texts[method] || method;
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('ar-DZ', {
    style: 'currency',
    currency: 'DZD'
  }).format(amount);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ar-DZ', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Load data from API
const loadOrders = async () => {
  loading.value = true;
  try {
    // Import OrdersService dynamically
    const { default: OrdersService } = await import('./OrdersService.js');
    
    // Load orders from API
    try {
      const ordersResponse = await OrdersService.getOrders({
        page: currentPage.value,
        limit: itemsPerPage.value,
        search: searchQuery.value,
        status: statusFilter.value,
        paymentMethod: paymentFilter.value,
        sortBy: sortKey.value,
        sortOrder: sortOrder.value
      });
      
      if (ordersResponse.success) {
        orders.value = ordersResponse.data.orders || [];
      } else {
        console.error('Failed to load orders:', ordersResponse.error);
        // Try direct API as fallback
        orders.value = await fetchOrders();
      }
    } catch (ordersError) {
      console.error('OrdersService failed:', ordersError);
      // Final fallback to direct API
      orders.value = await fetchOrders();
    }
    
    // Load statistics from API
    try {
      const statsResponse = await OrdersService.getOrderStats();
      if (statsResponse.success) {
        stats.value = statsResponse.data;
      } else {
        console.error('Failed to load stats:', statsResponse.error);
        // Try direct API for stats
        const statsData = await fetch('/api/orders/statistics');
        if (statsData.ok) {
          stats.value = await statsData.json();
        } else {
          // Fallback to calculated stats
          stats.value = calculateStatsFromOrders();
        }
      }
    } catch (statsError) {
      console.error('Stats API failed:', statsError);
      // Fallback to calculated stats
      stats.value = calculateStatsFromOrders();
    }
  } catch (error) {
    console.error('Error loading orders:', error);
    // Fallback to mock data if API fails
    orders.value = getMockOrders();
    stats.value = calculateStatsFromOrders();
  } finally {
    loading.value = false;
  }
};

// Dynamic data functions
const fetchOrders = async () => {
  try {
    const response = await fetch('/api/orders');
    if (response.ok) {
      const data = await response.json();
      return data.map(order => ({
        id: order.order_number || `ORD-${order.id}`,
        customer: order.customer?.name || 'عميل غير معروف',
        email: order.customer?.email || '',
        phone: order.customer?.phone || '',
        date: order.created_at,
        total: order.total_amount,
        subtotal: order.subtotal,
        shipping: order.shipping_amount || 0,
        tax: order.tax_amount || 0,
        status: order.status,
        paymentMethod: order.payment_method,
        paymentStatus: order.payment_status,
        shippingAddress: {
          street: order.shipping_address?.street || '',
          city: order.shipping_address?.city || '',
          country: order.shipping_address?.country || '',
          zipCode: order.shipping_address?.zip_code || ''
        },
        products: order.items?.map(item => ({
          id: item.product_id,
          name: item.product_name,
          price: item.price,
          quantity: item.quantity,
          sku: item.sku || '',
          image: item.product_image || 'https://via.placeholder.com/50'
        })) || [],
        timeline: order.timeline || [
          { status: order.status, date: order.created_at, note: 'تم إنشاء الطلب بنجاح' }
        ]
      }));
    }
  } catch (error) {
    console.error('Failed to fetch orders:', error);
  }
  
  // Fallback to mock data
  return getMockOrders();
};

// Mock data fallback
const getMockOrders = () => {
  return [
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
  ];
};

// Calculate stats from orders
const calculateStatsFromOrders = () => {
  const today = new Date().toDateString();
  const todayOrders = orders.value.filter(order => 
    new Date(order.date).toDateString() === today
  );
  
  return {
    totalOrders: orders.value.length,
    totalOrdersTrend: 12,
    todayOrders: todayOrders.length,
    todayOrdersTrend: 8,
    processingOrders: orders.value.filter(o => o.status === 'processing').length,
    processingOrdersTrend: -3,
    deliveredOrders: orders.value.filter(o => o.status === 'delivered').length,
    deliveredOrdersTrend: 15
  };
};

// Lifecycle
onMounted(() => {
  loadOrders();
});
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
}

.v-dialog .v-card {
  overflow-y: auto;
  max-height: 90vh;
}

@media print {
  .v-btn {
    display: none !important;
  }
}
</style>
