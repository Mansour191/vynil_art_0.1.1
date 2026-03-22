<template>
  <div class="orders-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="orders-container">
      <div class="glass-card">
        <!-- Header -->
        <div class="orders-header">
          <div class="header-content">
            <h1 class="page-title">
              <i class="fa-solid fa-shopping-bag"></i>
              طلباتي
            </h1>
            <p class="page-subtitle">تتبع جميع طلباتك وحالتها</p>
          </div>
          <div class="header-actions">
            <div class="filter-dropdown">
              <select v-model="selectedFilter" class="filter-select">
                <option value="all">جميع الطلبات</option>
                <option value="pending">قيد الانتظار</option>
                <option value="processing">قيد المعالجة</option>
                <option value="shipped">تم الشحن</option>
                <option value="delivered">تم التسليم</option>
                <option value="cancelled">ملغي</option>
              </select>
            </div>
            <button class="search-btn" @click="toggleSearch">
              <i class="fa-solid fa-search"></i>
            </button>
          </div>
        </div>

        <!-- Search Bar -->
        <div v-if="showSearch" class="search-bar">
          <div class="search-input-wrapper">
            <i class="fa-solid fa-search search-icon"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="ابحث عن طلباتك..."
              class="search-input"
            />
            <button class="search-close" @click="toggleSearch">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner">
            <i class="fa-solid fa-spinner fa-spin"></i>
          </div>
          <p class="loading-text">جاري تحميل الطلبات...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="fa-solid fa-shopping-cart"></i>
          </div>
          <h3 class="empty-title">لا توجد طلبات</h3>
          <p class="empty-text">لم تقم بإنشاء أي طلبات بعد</p>
          <router-link to="/products" class="browse-products-btn">
            <i class="fa-solid fa-shopping-bag"></i>
            تصفح المنتجات
          </router-link>
        </div>

        <!-- Orders List -->
        <div v-else class="orders-list">
          <div 
            v-for="order in filteredOrders" 
            :key="order.id" 
            class="order-card"
            @click="viewOrderDetails(order.id)"
          >
            <div class="order-header">
              <div class="order-info">
                <h3 class="order-number">طلب #{{ order.id }}</h3>
                <p class="order-date">{{ formatDate(order.createdAt) }}</p>
              </div>
              <div class="order-status">
                <span :class="['status-badge', order.status]">
                  {{ getStatusText(order.status) }}
                </span>
              </div>
            </div>

            <div class="order-items">
              <div 
                v-for="item in order.items" 
                :key="item.id" 
                class="order-item"
              >
                <img 
                  :src="item.image || '/images/placeholder.jpg'" 
                  :alt="item.name"
                  class="item-image"
                />
                <div class="item-details">
                  <h4 class="item-name">{{ item.name }}</h4>
                  <p class="item-quantity">الكمية: {{ item.quantity }}</p>
                  <p class="item-price">{{ formatPrice(item.price) }}</p>
                </div>
              </div>
            </div>

            <div class="order-footer">
              <div class="order-total">
                <span class="total-label">الإجمالي:</span>
                <span class="total-amount">{{ formatPrice(order.total) }}</span>
              </div>
              <div class="order-actions">
                <button class="action-btn primary" @click.stop="viewOrderDetails(order.id)">
                  <i class="fa-solid fa-eye"></i>
                  التفاصيل
                </button>
                <button 
                  v-if="order.status === 'delivered'" 
                  class="action-btn secondary" 
                  @click.stop="reorderItems(order)"
                >
                  <i class="fa-solid fa-redo"></i>
                  إعادة الطلب
                </button>
                <button 
                  v-if="['pending', 'processing'].includes(order.status)" 
                  class="action-btn danger" 
                  @click.stop="cancelOrder(order.id)"
                >
                  <i class="fa-solid fa-times"></i>
                  إلغاء
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button 
            v-if="currentPage > 1" 
            @click="changePage(currentPage - 1)"
            class="pagination-btn"
          >
            <i class="fa-solid fa-chevron-right"></i>
            السابق
          </button>
          
          <div class="pagination-numbers">
            <button 
              v-for="page in visiblePages" 
              :key="page"
              :class="['pagination-number', { active: page === currentPage }]"
              @click="changePage(page)"
            >
              {{ page }}
            </button>
          </div>
          
          <button 
            v-if="currentPage < totalPages" 
            @click="changePage(currentPage + 1)"
            class="pagination-btn"
          >
            التالي
            <i class="fa-solid fa-chevron-left"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';

const router = useRouter();
const authStore = useAuthStore();

const loading = ref(true);
const showSearch = ref(false);
const searchQuery = ref('');
const selectedFilter = ref('all');
const currentPage = ref(1);
const totalPages = ref(1);
const ordersPerPage = 10;

const orders = ref([]);

// Mock data - في الواقع سيتم جلبها من GraphQL
const mockOrders = [
  {
    id: 'ORD001',
    status: 'delivered',
    createdAt: '2024-01-15T10:30:00Z',
    total: 1250.00,
    items: [
      {
        id: 1,
        name: 'خلفية فنية ذهبية',
        quantity: 2,
        price: 625.00,
        image: '/images/products/product1.jpg'
      }
    ]
  },
  {
    id: 'ORD002',
    status: 'shipped',
    createdAt: '2024-01-20T14:15:00Z',
    total: 890.00,
    items: [
      {
        id: 2,
        name: 'ديكور حائط أزرق',
        quantity: 1,
        price: 890.00,
        image: '/images/products/product2.jpg'
      }
    ]
  },
  {
    id: 'ORD003',
    status: 'processing',
    createdAt: '2024-01-25T09:45:00Z',
    total: 2100.00,
    items: [
      {
        id: 3,
        name: 'ورق جدران كلاسيكي',
        quantity: 3,
        price: 700.00,
        image: '/images/products/product3.jpg'
      }
    ]
  }
];

const filteredOrders = computed(() => {
  let filtered = orders.value;

  // Apply status filter
  if (selectedFilter.value !== 'all') {
    filtered = filtered.filter(order => order.status === selectedFilter.value);
  }

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(order => 
      order.id.toLowerCase().includes(query) ||
      order.items.some(item => item.name.toLowerCase().includes(query))
    );
  }

  return filtered;
});

const visiblePages = computed(() => {
  const pages = [];
  const maxVisible = 5;
  let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
  let end = Math.min(totalPages.value, start + maxVisible - 1);
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1);
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  
  return pages;
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatPrice = (price) => {
  return new Intl.NumberFormat('ar-SA', {
    style: 'currency',
    currency: 'DZD'
  }).format(price);
};

const getStatusText = (status) => {
  const statusMap = {
    pending: 'قيد الانتظار',
    processing: 'قيد المعالجة',
    shipped: 'تم الشحن',
    delivered: 'تم التسليم',
    cancelled: 'ملغي'
  };
  return statusMap[status] || status;
};

const toggleSearch = () => {
  showSearch.value = !showSearch.value;
  if (!showSearch.value) {
    searchQuery.value = '';
  }
};

const changePage = (page) => {
  currentPage.value = page;
  loadOrders();
};

const viewOrderDetails = (orderId) => {
  router.push(`/profile/orders/${orderId}`);
};

const cancelOrder = async (orderId) => {
  if (confirm('هل أنت متأكد من إلغاء هذا الطلب؟')) {
    try {
      // TODO: Implement cancel order API call
      console.log('Cancel order:', orderId);
      // Update order status locally
      const order = orders.value.find(o => o.id === orderId);
      if (order) {
        order.status = 'cancelled';
      }
    } catch (error) {
      console.error('Error cancelling order:', error);
    }
  }
};

const reorderItems = async (order) => {
  try {
    // TODO: Implement reorder functionality
    console.log('Reorder items:', order);
    // Add items to cart and redirect to cart
    router.push('/cart');
  } catch (error) {
    console.error('Error reordering:', error);
  }
};

const loadOrders = async () => {
  try {
    loading.value = true;
    // TODO: Implement GraphQL query to fetch orders
    // const data = await graphqlQuery(GET_ORDERS_QUERY, {
    //   page: currentPage.value,
    //   limit: ordersPerPage
    // });
    
    // Mock loading
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    orders.value = mockOrders;
    totalPages.value = Math.ceil(mockOrders.length / ordersPerPage);
  } catch (error) {
    console.error('Error loading orders:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadOrders();
});
</script>

<style scoped>
/* ===== Orders Page ===== */
.orders-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

/* Background Effects */
.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 20%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(212, 175, 55, 0.12) 0%, transparent 50%);
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.1) 50%, transparent 100%);
  filter: blur(2px);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-20px) scale(1.05); }
}

/* Orders Container */
.orders-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 1000px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.08),
              inset 0 0 30px rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

/* Header */
.orders-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.page-title i {
  color: #d4af37;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-dropdown {
  position: relative;
}

.filter-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 16px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.filter-select:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.3);
}

.filter-select:focus {
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.filter-select option {
  background: #1a1a2e;
  color: #ffffff;
}

.search-btn {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.3);
  color: #d4af37;
}

/* Search Bar */
.search-bar {
  margin-bottom: 30px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0 16px;
}

.search-icon {
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  margin-right: 12px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 16px;
  padding: 12px 0;
  outline: none;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.search-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 8px;
  transition: color 0.3s ease;
}

.search-close:hover {
  color: #ffffff;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  font-size: 48px;
  color: #d4af37;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 18px;
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.empty-icon {
  font-size: 64px;
  color: rgba(255, 255, 255, 0.3);
  margin-bottom: 24px;
}

.empty-title {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.empty-text {
  font-size: 16px;
  margin: 0 0 32px 0;
}

.browse-products-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.browse-products-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

/* Orders List */
.orders-list {
  display: grid;
  gap: 20px;
}

.order-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.order-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.order-info {
  flex: 1;
}

.order-number {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.order-date {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.order-status {
  margin-left: 16px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.pending {
  background: rgba(108, 117, 125, 0.2);
  color: #6c757d;
}

.status-badge.processing {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-badge.shipped {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
}

.status-badge.delivered {
  background: rgba(0, 200, 81, 0.2);
  color: #00c851;
}

.status-badge.cancelled {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
}

/* Order Items */
.order-items {
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  background: rgba(255, 255, 255, 0.05);
}

.item-details {
  flex: 1;
}

.item-name {
  color: #ffffff;
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.item-quantity {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0 0 4px 0;
}

.item-price {
  color: #d4af37;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

/* Order Footer */
.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.order-total {
  display: flex;
  align-items: center;
  gap: 8px;
}

.total-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.total-amount {
  color: #d4af37;
  font-size: 20px;
  font-weight: 700;
}

.order-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  color: #d4af37;
  border-color: rgba(212, 175, 55, 0.3);
}

.action-btn.danger {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.action-btn.danger:hover {
  background: rgba(220, 53, 69, 0.3);
  color: #ffffff;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.3);
  color: #d4af37;
}

.pagination-numbers {
  display: flex;
  gap: 8px;
}

.pagination-number {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pagination-number:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.3);
  color: #d4af37;
}

.pagination-number.active {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border-color: #d4af37;
  color: #1a1a2e;
}

/* Responsive Design */
@media (max-width: 768px) {
  .orders-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .orders-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .order-card {
    padding: 16px;
  }
  
  .order-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .order-status {
    margin-left: 0;
  }
  
  .order-footer {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .order-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
  }
  
  .pagination {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .pagination-btn {
    flex: 1;
    min-width: 100px;
  }
}
</style>
