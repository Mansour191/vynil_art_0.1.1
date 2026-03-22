<template>
  <div class="unified-reports">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-chart-pie header-icon"></i>
          التقارير الموحدة
        </h1>
        <p class="header-subtitle">تحليلات متكاملة من موقعك و ERPNext</p>
      </div>
      <div class="header-actions">
        <button class="btn-export" @click="exportReport">
          <i class="fa-solid fa-download"></i>
          <span>تصدير التقرير</span>
        </button>
        <button class="btn-refresh" @click="refreshData">
          <i class="fa-solid fa-sync-alt"></i>
          <span>تحديث</span>
        </button>
      </div>
    </div>

    <!-- تبويبات التقارير -->
    <div class="reports-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.name }}</span>
      </button>
    </div>

    <!-- محتوى التقرير حسب التبويب -->
    <div class="tab-content">
      <!-- ===== تقرير المبيعات ===== -->
      <div v-if="activeTab === 'sales'" class="report-section">
        <div class="section-header">
          <h2>📈 تقرير المبيعات الموحد</h2>
          <div class="date-range">
            <input type="date" v-model="dateRange.from" />
            <span>إلى</span>
            <input type="date" v-model="dateRange.to" />
            <button class="btn-apply" @click="loadSalesData">تطبيق</button>
          </div>
        </div>

        <!-- بطاقات الملخص -->
        <div class="summary-cards">
          <div class="summary-card">
            <div class="card-icon site">
              <i class="fa-solid fa-store"></i>
            </div>
            <div class="card-content">
              <span class="card-label">مبيعات الموقع</span>
              <span class="card-value">{{ formatCurrency(sales.site.total) }}</span>
              <span
                class="card-trend"
                :class="{ up: sales.site.trend > 0, down: sales.site.trend < 0 }"
              >
                <i :class="sales.site.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
                {{ Math.abs(sales.site.trend) }}%
              </span>
            </div>
          </div>

          <div class="summary-card">
            <div class="card-icon erpnext">
              <i class="fa-solid fa-database"></i>
            </div>
            <div class="card-content">
              <span class="card-label">مبيعات ERPNext</span>
              <span class="card-value">{{ formatCurrency(sales.erpnext.total) }}</span>
              <span
                class="card-trend"
                :class="{ up: sales.erpnext.trend > 0, down: sales.erpnext.trend < 0 }"
              >
                <i :class="sales.erpnext.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
                {{ Math.abs(sales.erpnext.trend) }}%
              </span>
            </div>
          </div>

          <div class="summary-card total">
            <div class="card-icon">
              <i class="fa-solid fa-chart-line"></i>
            </div>
            <div class="card-content">
              <span class="card-label">إجمالي موحد</span>
              <span class="card-value">{{ formatCurrency(sales.total) }}</span>
              <span class="card-trend" :class="{ up: sales.trend > 0, down: sales.trend < 0 }">
                <i :class="sales.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
                {{ Math.abs(sales.trend) }}%
              </span>
            </div>
          </div>
        </div>

        <!-- الرسم البياني للمبيعات -->
        <div class="chart-card">
          <h3>مقارنة المبيعات اليومية</h3>
          <div class="chart-container">
            <canvas ref="salesChart"></canvas>
          </div>
        </div>

        <!-- جدول المبيعات -->
        <div class="table-card">
          <h3>تفاصيل المبيعات</h3>
          <table class="reports-table">
            <thead>
              <tr>
                <th>التاريخ</th>
                <th>موقعك</th>
                <th>ERPNext</th>
                <th>الإجمالي</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in sales.details" :key="item.date">
                <td>{{ item.date }}</td>
                <td>{{ formatCurrency(item.site) }}</td>
                <td>{{ formatCurrency(item.erpnext) }}</td>
                <td>
                  <strong>{{ formatCurrency(item.total) }}</strong>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== تقرير المخزون ===== -->
      <div v-if="activeTab === 'inventory'" class="report-section">
        <div class="section-header">
          <h2>📦 تقرير المخزون الموحد</h2>
        </div>

        <!-- بطاقات المخزون -->
        <div class="inventory-summary">
          <div class="inventory-card">
            <h4>إجمالي المنتجات</h4>
            <span class="inventory-value">{{ inventory.totalProducts }}</span>
          </div>
          <div class="inventory-card">
            <h4>قيمة المخزون</h4>
            <span class="inventory-value">{{ formatCurrency(inventory.totalValue) }}</span>
          </div>
          <div class="inventory-card warning">
            <h4>منتجات منخفضة</h4>
            <span class="inventory-value">{{ inventory.lowStock }}</span>
          </div>
          <div class="inventory-card danger">
            <h4>نافدة</h4>
            <span class="inventory-value">{{ inventory.outOfStock }}</span>
          </div>
        </div>

        <!-- جدول المخزون -->
        <div class="table-card">
          <h3>حالة المخزون</h3>
          <table class="reports-table">
            <thead>
              <tr>
                <th>المنتج</th>
                <th>SKU</th>
                <th>مخزون الموقع</th>
                <th>مخزون ERPNext</th>
                <th>الفرق</th>
                <th>الحالة</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in inventory.details" :key="item.sku">
                <td>{{ item.name }}</td>
                <td>{{ item.sku }}</td>
                <td>{{ item.siteStock }}</td>
                <td>{{ item.erpnextStock }}</td>
                <td :class="{ 'text-danger': item.diff !== 0 }">{{ item.diff }}</td>
                <td>
                  <span class="status-badge" :class="getStockStatus(item.siteStock)">
                    {{ getStockStatusText(item.siteStock) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== تقرير العملاء ===== -->
      <div v-if="activeTab === 'customers'" class="report-section">
        <div class="section-header">
          <h2>👥 تقرير العملاء الموحد</h2>
        </div>

        <!-- بطاقات العملاء -->
        <div class="customers-summary">
          <div class="customer-card">
            <h4>إجمالي العملاء</h4>
            <span class="customer-value">{{ customers.total }}</span>
          </div>
          <div class="customer-card">
            <h4>عملاء جدد (30 يوم)</h4>
            <span class="customer-value">{{ customers.new }}</span>
          </div>
          <div class="customer-card">
            <h4>عملاء نشطين</h4>
            <span class="customer-value">{{ customers.active }}</span>
          </div>
          <div class="customer-card">
            <h4>متوسط المشتريات</h4>
            <span class="customer-value">{{ formatCurrency(customers.avgPurchase) }}</span>
          </div>
        </div>

        <!-- أفضل العملاء -->
        <div class="table-card">
          <h3>أفضل العملاء</h3>
          <table class="reports-table">
            <thead>
              <tr>
                <th>العميل</th>
                <th>البريد الإلكتروني</th>
                <th>عدد الطلبات</th>
                <th>إجمالي المشتريات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="customer in customers.top" :key="customer.id">
                <td>{{ customer.name }}</td>
                <td>{{ customer.email }}</td>
                <td>{{ customer.orders }}</td>
                <td>{{ formatCurrency(customer.total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== تقرير الأداء المالي ===== -->
      <div v-if="activeTab === 'financial'" class="report-section">
        <div class="section-header">
          <h2>💰 التقرير المالي الموحد</h2>
        </div>

        <!-- بطاقات مالية -->
        <div class="financial-grid">
          <div class="financial-card">
            <h4>الإيرادات</h4>
            <span class="financial-value">{{ formatCurrency(financial.revenue) }}</span>
          </div>
          <div class="financial-card">
            <h4>المصروفات</h4>
            <span class="financial-value">{{ formatCurrency(financial.expenses) }}</span>
          </div>
          <div class="financial-card profit">
            <h4>صافي الربح</h4>
            <span class="financial-value">{{ formatCurrency(financial.profit) }}</span>
          </div>
          <div class="financial-card">
            <h4>الهامش</h4>
            <span class="financial-value">{{ financial.margin }}%</span>
          </div>
        </div>

        <!-- الضرائب -->
        <div class="tax-card">
          <h3>ملخص الضرائب</h3>
          <div class="tax-details">
            <div class="tax-item">
              <span>ضريبة المبيعات</span>
              <span>{{ formatCurrency(financial.taxCollected) }}</span>
            </div>
            <div class="tax-item">
              <span>ضريبة المشتريات</span>
              <span>{{ formatCurrency(financial.taxPaid) }}</span>
            </div>
            <div class="tax-item total">
              <span>صافي الضريبة المستحقة</span>
              <span>{{ formatCurrency(financial.taxNet) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';

export default {
  name: 'UnifiedReports',
  data() {
    return {
      // بيانات التقارير
      activeTab: 'sales',
      tabs: [
        { id: 'sales', name: 'المبيعات', icon: 'fa-solid fa-chart-line' },
        { id: 'inventory', name: 'المخزون', icon: 'fa-solid fa-boxes' },
        { id: 'customers', name: 'العملاء', icon: 'fa-solid fa-users' },
        { id: 'financial', name: 'المالي', icon: 'fa-solid fa-coins' },
      ],
      dateRange: {
        from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        to: new Date().toISOString().split('T')[0],
      },
      sales: {
        site: { total: 45600, trend: 12.5 },
        erpnext: { total: 38900, trend: 8.3 },
        total: 84500,
        trend: 10.2,
        details: [
          { date: '2024-03-01', site: 1200, erpnext: 980, total: 2180 },
          { date: '2024-03-02', site: 1350, erpnext: 1050, total: 2400 },
          { date: '2024-03-03', site: 1100, erpnext: 870, total: 1970 },
          { date: '2024-03-04', site: 1400, erpnext: 1120, total: 2520 },
          { date: '2024-03-05', site: 1250, erpnext: 1000, total: 2250 },
          { date: '2024-03-06', site: 1300, erpnext: 1080, total: 2380 },
          { date: '2024-03-07', site: 1150, erpnext: 920, total: 2070 },
        ],
      },
      inventory: {
        totalProducts: 156,
        totalValue: 45600,
        lowStock: 12,
        outOfStock: 5,
        details: [
          { name: 'ملصق حائط زهور', sku: 'WAL-001', siteStock: 23, erpnextStock: 23, diff: 0 },
          { name: 'ملصق باب خشبي', sku: 'DR-002', siteStock: 5, erpnextStock: 8, diff: -3 },
          { name: 'إطار سيارة رياضي', sku: 'CAR-003', siteStock: 0, erpnextStock: 2, diff: -2 },
          { name: 'ملصق مطبخ فواكه', sku: 'KIT-004', siteStock: 12, erpnextStock: 10, diff: 2 },
        ],
      },
      customers: {
        total: 892,
        new: 45,
        active: 234,
        avgPurchase: 450,
        top: [
          { id: 1, name: 'أحمد محمد', email: 'ahmed@example.com', orders: 12, total: 5400 },
          { id: 2, name: 'سارة أحمد', email: 'sara@example.com', orders: 8, total: 3200 },
          { id: 3, name: 'محمد علي', email: 'mohammed@example.com', orders: 5, total: 2100 },
        ],
      },
      financial: {
        revenue: 84500,
        expenses: 51200,
        profit: 33300,
        margin: 39.4,
        taxCollected: 12675,
        taxPaid: 7680,
        taxNet: 4995,
      },
      salesChart: null,
    };
  },
  mounted() {
    this.initSalesChart();
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('ar-SA', {
        style: 'currency',
        currency: 'SAR',
        minimumFractionDigits: 0,
      }).format(value);
    },

    getStockStatus(stock) {
      if (stock === 0) return 'out';
      if (stock <= 10) return 'low';
      return 'good';
    },

    getStockStatusText(stock) {
      if (stock === 0) return 'نافد';
      if (stock <= 10) return 'منخفض';
      return 'متوفر';
    },

    initSalesChart() {
      const ctx = this.$refs.salesChart?.getContext('2d');
      if (!ctx) return;

      this.salesChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.sales.details.map((d) => d.date),
          datasets: [
            {
              label: 'موقعك',
              data: this.sales.details.map((d) => d.site),
              borderColor: '#d4af37',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              tension: 0.4,
            },
            {
              label: 'ERPNext',
              data: this.sales.details.map((d) => d.erpnext),
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: { color: '#fff' },
            },
          },
          scales: {
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#fff' },
            },
            x: {
              grid: { display: false },
              ticks: { color: '#fff' },
            },
          },
        },
      });
    },

    loadSalesData() {
      // هنا هنجلب البيانات من الخدمات
      console.log('Loading sales data for:', this.dateRange);
      // تحديث الرسم البياني
      if (this.salesChart) {
        this.salesChart.destroy();
        this.initSalesChart();
      }
    },

    refreshData() {
      this.loadSalesData();
      this.$toast?.success('تم تحديث البيانات');
    },

    exportReport() {
      const data = {
        report: this.activeTab,
        dateRange: this.dateRange,
        data: this[this.activeTab],
      };

      console.log('Exporting:', data);

      // تصدير كـ CSV
      let csv = '';
      if (this.activeTab === 'sales') {
        csv =
          'التاريخ,موقعك,ERPNext,الإجمالي\n' +
          this.sales.details.map((d) => `${d.date},${d.site},${d.erpnext},${d.total}`).join('\n');
      }

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `تقرير-${this.activeTab}-${this.dateRange.from}.csv`;
      a.click();

      this.$toast?.success('تم تصدير التقرير');
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.unified-reports {
  padding: 25px;
  min-height: 100vh;
  background: var(--bg-primary);
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

/* رأس الصفحة */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 25px 30px;
  border-radius: 24px;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-md);
}

.header-title h1 {
  font-size: 2rem;
  color: white;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: var(--gold-1);
  font-size: 2rem;
  animation: iconPulse 2s ease infinite;
}

@keyframes iconPulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.header-subtitle {
  color: var(--text-dim);
  font-size: 0.95rem;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-export,
.btn-refresh {
  padding: 12px 24px;
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s;
}

.btn-export {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-refresh {
  background: var(--bg-card);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-export:hover,
.btn-refresh:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* تبويبات التقارير */
.reports-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 15px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
}

.tab-btn {
  flex: 1;
  padding: 12px 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.tab-btn i {
  color: var(--gold-1);
}

.tab-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
}

.tab-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.tab-btn.active i {
  color: var(--bg-deep);
}

/* رأس كل قسم */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h2 {
  color: white;
  font-size: 1.3rem;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-range input {
  padding: 8px 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
}

.btn-apply {
  padding: 8px 16px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 10px;
  color: var(--bg-deep);
  cursor: pointer;
  font-weight: 600;
}

/* بطاقات الملخص */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.summary-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.summary-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.summary-card.total {
  background: var(--gold-gradient-soft);
  border-color: var(--gold-1);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.card-icon.site {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.card-icon.erpnext {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.card-content {
  flex: 1;
}

.card-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.card-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.card-trend {
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 3px;
}

.card-trend.up {
  color: #4caf50;
}

.card-trend.down {
  color: #f44336;
}

/* بطاقات المخزون */
.inventory-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.inventory-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.inventory-card.warning {
  border-color: #ff9800;
}

.inventory-card.danger {
  border-color: #f44336;
}

.inventory-card h4 {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.inventory-value {
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
}

/* بطاقات العملاء */
.customers-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.customer-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.customer-card h4 {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.customer-value {
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
}

/* بطاقات مالية */
.financial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.financial-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.financial-card.profit {
  background: rgba(76, 175, 80, 0.1);
  border-color: #4caf50;
}

.financial-card h4 {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.financial-value {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
}

/* بطاقة الضرائب */
.tax-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.tax-card h3 {
  color: var(--gold-1);
  margin-bottom: 20px;
}

.tax-details {
  max-width: 400px;
}

.tax-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.tax-item.total {
  border-bottom: none;
  margin-top: 10px;
  padding-top: 15px;
  border-top: 2px solid var(--border-light);
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
}

/* بطاقات الجداول */
.chart-card,
.table-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.chart-card h3,
.table-card h3 {
  color: var(--gold-1);
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* الجداول */
.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  text-align: right;
  padding: 12px;
  color: var(--text-dim);
  font-weight: 600;
  border-bottom: 2px solid var(--border-light);
}

.reports-table td {
  padding: 12px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.reports-table tr:hover td {
  background: var(--bg-primary);
}

.text-danger {
  color: #f44336;
  font-weight: 600;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.status-badge.good {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.status-badge.low {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.status-badge.out {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

/* استجابة */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .reports-tabs {
    flex-direction: column;
  }

  .section-header {
    flex-direction: column;
    gap: 15px;
  }

  .date-range {
    flex-wrap: wrap;
    justify-content: center;
  }

  .summary-cards,
  .inventory-summary,
  .customers-summary,
  .financial-grid {
    grid-template-columns: 1fr;
  }

  .reports-table {
    display: block;
    overflow-x: auto;
  }
}
</style>
