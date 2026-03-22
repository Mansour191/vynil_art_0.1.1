<template>
  <div class="dashboard-home">
    <!-- بطاقات الإحصائيات المتحركة -->
    <div class="stats-grid">
      <div
        class="stat-card"
        v-for="(stat, index) in stats"
        :key="stat.title"
        :style="{ animationDelay: index * 0.1 + 's' }"
      >
        <div class="stat-icon" :style="{ background: stat.color + '20' }">
          <i :class="stat.icon" :style="{ color: stat.color }"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stat.value }}</h3>
          <p>{{ stat.title }}</p>
          <div class="stat-trend">
            <i :class="stat.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
            <span :class="{ positive: stat.trend > 0, negative: stat.trend < 0 }">
              {{ Math.abs(stat.trend) }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- الرسوم البيانية والمحتوى -->
    <div class="content-grid">
      <!-- الرسم البياني للمبيعات -->
      <div class="chart-card">
        <div class="card-header">
          <h3 v-ai-t>المبيعات الشهرية</h3>
          <select class="chart-filter">
            <option v-ai-t>آخر 7 أيام</option>
            <option v-ai-t>آخر 30 يوم</option>
            <option v-ai-t>آخر 3 شهور</option>
          </select>
        </div>
        <div class="chart-container">
          <!-- يمكن إضافة رسم بياني لاحقاً -->
          <div class="chart-placeholder">
            <div class="bar-chart">
              <div v-for="n in 7" :key="n" class="bar-wrapper">
                <div class="bar" :style="{ height: Math.random() * 150 + 50 + 'px' }"></div>
                <span>يوم {{ n }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- المنتجات الأكثر مبيعاً -->
      <div class="top-products-card">
        <div class="card-header">
          <h3 v-ai-t>المنتجات الأكثر مبيعاً</h3>
          <a href="#" class="view-all" v-ai-t>عرض الكل</a>
        </div>
        <div class="products-list">
          <div v-for="product in topProducts" :key="product.id" class="product-item">
            <div class="product-info">
              <img :src="product.image" :alt="product.name" />
              <div>
                <h4 v-ai-t>{{ product.name }}</h4>
                <p class="product-category" v-ai-t>{{ product.category }}</p>
              </div>
            </div>
            <div class="product-stats">
              <span class="sales-count" v-ai-t>{{ product.sales }} مبيعات</span>
              <span class="revenue">{{ product.revenue }} ر.س</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- الطلبات الأخيرة -->
    <div class="recent-orders-card">
      <div class="card-header">
        <h3>الطلبات الأخيرة</h3>
        <a href="#" class="view-all">عرض الكل</a>
      </div>

      <div class="table-responsive">
        <table class="orders-table">
          <thead>
            <tr>
              <th>رقم الطلب</th>
              <th>العميل</th>
              <th>التاريخ</th>
              <th>المبلغ</th>
              <th>الحالة</th>
              <th>الإجراءات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in recentOrders" :key="order.id">
              <td>
                <span class="order-id">#{{ order.id }}</span>
              </td>
              <td>{{ order.customer }}</td>
              <td>{{ order.date }}</td>
              <td>
                <span class="amount">{{ order.amount }} ر.س</span>
              </td>
              <td>
                <span :class="['status-badge', order.status]">
                  {{ order.statusText }}
                </span>
              </td>
              <td>
                <button class="action-btn" @click="viewOrder(order.id)">
                  <i class="fa-solid fa-eye"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import DashboardService from '@/services/DashboardService';

// State
const loading = ref(true);
const error = ref(null);
const stats = ref([]);
const topProducts = ref([]);
const recentOrders = ref([]);
const salesData = ref([]);
const selectedPeriod = ref('7days');

// Computed
const formattedStats = computed(() => {
  return stats.value.map(stat => ({
    title: stat.title,
    value: formatValue(stat.value, stat.type),
    icon: stat.icon,
    color: stat.color,
    trend: stat.trend || 0,
  }));
});

// Methods
const formatValue = (value, type = 'number') => {
  switch (type) {
    case 'currency':
      return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'DZD'
      }).format(value);
    case 'percentage':
      return `${value}%`;
    default:
      return value.toLocaleString('ar-SA');
  }
};

const fetchDashboardData = async () => {
  try {
    loading.value = true;
    error.value = null;

    // Fetch all dashboard data in parallel
    const [
      statsData,
      productsData,
      ordersData,
      salesChartData
    ] = await Promise.all([
        DashboardService.getDashboardStats(),
        DashboardService.getTopProducts(5),
        DashboardService.getRecentOrders(5),
        DashboardService.getSalesData(selectedPeriod.value)
      ]);

    stats.value = statsData;
    topProducts.value = productsData;
    recentOrders.value = ordersData;
    salesData.value = salesChartData;

  } catch (err) {
    console.error('Error fetching dashboard data:', err);
    error.value = 'فشل في تحميل بيانات لوحة التحكم';
    
    // Fallback to mock data if backend fails
    stats.value = [
      {
        title: 'إجمالي المبيعات',
        value: 45280,
        type: 'currency',
        icon: 'fa-solid fa-wallet',
        color: '#D4AF37',
        trend: 12.5,
      },
      {
        title: 'الطلبات الجديدة',
        value: 156,
        type: 'number',
        icon: 'fa-solid fa-shopping-bag',
        color: '#2196F3',
        trend: 8.2,
      },
      {
        title: 'العملاء النشطون',
        value: 2420,
        type: 'number',
        icon: 'fa-solid fa-users',
        color: '#4CAF50',
        trend: -2.4,
      },
      {
        title: 'متوسط قيمة الطلب',
        value: 290,
        type: 'currency',
        icon: 'fa-solid fa-chart-line',
        color: '#9C27B0',
        trend: 5.1,
      },
    ];
  } finally {
    loading.value = false;
  }
};

const handlePeriodChange = async (period) => {
  selectedPeriod.value = period;
  try {
    const salesChartData = await DashboardService.getSalesData(period);
    salesData.value = salesChartData;
  } catch (err) {
    console.error('Error fetching sales data:', err);
  }
};

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await DashboardService.updateOrderStatus(orderId, newStatus);
    // Refresh orders list
    const ordersData = await DashboardService.getRecentOrders(5);
    recentOrders.value = ordersData;
  } catch (err) {
    console.error('Error updating order status:', err);
  }
};

// Lifecycle
onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
.dashboard-home {
  padding: 20px;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* بطاقات الإحصائيات */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
  animation: slideUp 0.5s ease forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-primary);
  box-shadow: var(--shadow-gold);
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.stat-info h3 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 5px;
}

.stat-info p {
  color: var(--text-muted);
  margin-bottom: 8px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.9rem;
}

.stat-trend .positive {
  color: var(--success);
}

.stat-trend .negative {
  color: var(--danger);
}

/* شبكة المحتوى */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

/* بطاقة الرسم البياني */
.chart-card,
.top-products-card,
.recent-orders-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid var(--border-light);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card-header h3 {
  color: white;
  font-size: 1.2rem;
}

.chart-filter {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
  padding: 8px 15px;
  border-radius: 10px;
  font-size: 0.9rem;
  cursor: pointer;
}

.view-all {
  color: var(--gold-primary);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.view-all:hover {
  color: var(--gold-light);
}

/* الرسم البياني التجريبي */
.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 20px;
  height: 100%;
  width: 100%;
}

.bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.bar {
  width: 100%;
  background: var(--gold-gradient);
  border-radius: 10px 10px 0 0;
  min-height: 30px;
  transition: height 0.3s;
  animation: barGrow 1s ease;
}

@keyframes barGrow {
  from {
    height: 30px;
  }
  to {
    height: var(--height);
  }
}

.bar-wrapper span {
  color: var(--text-muted);
  font-size: 0.8rem;
}

/* قائمة المنتجات */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.product-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border-radius: 12px;
  transition: background 0.3s;
}

.product-item:hover {
  background: var(--bg-primary);
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-info img {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  object-fit: cover;
  border: 1px solid var(--border-light);
}

.product-info h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 3px;
}

.product-category {
  color: var(--text-muted);
  font-size: 0.8rem;
}

.product-stats {
  text-align: left;
}

.sales-count {
  display: block;
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 3px;
}

.revenue {
  color: var(--gold-primary);
  font-weight: 600;
}

/* جدول الطلبات */
.recent-orders-card {
  overflow-x: auto;
}

.table-responsive {
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  text-align: right;
  padding: 15px;
  color: var(--text-muted);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--border-light);
}

.orders-table td {
  padding: 12px 15px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.order-id {
  color: var(--gold-primary);
  font-weight: 600;
}

.amount {
  color: white;
  font-weight: 600;
}

.status-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.completed {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-badge.processing {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
}

.status-badge.pending {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.action-btn {
  width: 35px;
  height: 35px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--gold-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: var(--gold-primary);
  color: var(--bg-primary);
  border-color: var(--gold-primary);
}

/* استجابة للشاشات الصغيرة */
@media (max-width: 992px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .product-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .product-stats {
    text-align: right;
    width: 100%;
  }
}
</style>
