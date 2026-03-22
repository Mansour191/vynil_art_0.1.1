<template>
  <div class="advanced-analytics">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-chart-line header-icon"></i>
          التحليلات المتقدمة
        </h1>
        <p class="header-subtitle">تحليلات ذكية ورؤى عميقة لأداء المتجر</p>
      </div>
      <div class="header-actions">
        <button class="btn-export" @click="exportAnalytics">
          <i class="fa-solid fa-download"></i>
          <span>تصدير التقرير</span>
        </button>
        <button class="btn-refresh" @click="refreshData">
          <i class="fa-solid fa-sync-alt"></i>
          <span>تحديث</span>
        </button>
      </div>
    </div>

    <!-- مؤشرات الأداء الرئيسية (KPIs) -->
    <div class="kpi-grid">
      <div class="kpi-card" v-for="kpi in kpis" :key="kpi.title">
        <div class="kpi-icon" :style="{ background: kpi.color + '20' }">
          <i :class="kpi.icon" :style="{ color: kpi.color }"></i>
        </div>
        <div class="kpi-content">
          <span class="kpi-label">{{ kpi.title }}</span>
          <span class="kpi-value">{{ kpi.value }}</span>
          <div class="kpi-trend" :class="{ up: kpi.trend > 0, down: kpi.trend < 0 }">
            <i :class="kpi.trend > 0 ? 'fa-solid fa-arrow-up' : 'fa-solid fa-arrow-down'"></i>
            {{ Math.abs(kpi.trend) }}%
            <span class="kpi-period">مقارنة بالشهر الماضي</span>
          </div>
        </div>
      </div>
    </div>

    <!-- فلاتر الوقت -->
    <div class="filters-bar">
      <div class="date-range">
        <button
          v-for="range in dateRanges"
          :key="range.value"
          class="range-btn"
          :class="{ active: selectedRange === range.value }"
          @click="setDateRange(range.value)"
        >
          {{ range.label }}
        </button>
      </div>
      <div class="custom-date" v-if="selectedRange === 'custom'">
        <input type="date" v-model="customDate.from" />
        <span>إلى</span>
        <input type="date" v-model="customDate.to" />
        <button class="btn-apply" @click="applyCustomRange">تطبيق</button>
      </div>
    </div>

    <!-- شبكة التحليلات -->
    <div class="analytics-grid">
      <!-- المبيعات اليومية -->
      <div class="analytics-card large">
        <div class="card-header">
          <h3><i class="fa-solid fa-chart-line"></i> المبيعات اليومية</h3>
          <div class="card-actions">
            <select v-model="salesChartType">
              <option value="line">خطي</option>
              <option value="bar">أعمدة</option>
            </select>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="salesChart"></canvas>
        </div>
      </div>

      <!-- توزيع المبيعات حسب التصنيف -->
      <div class="analytics-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-chart-pie"></i> المبيعات حسب التصنيف</h3>
        </div>
        <div class="chart-container pie-chart">
          <canvas ref="categoryChart"></canvas>
        </div>
        <div class="chart-legend">
          <div v-for="item in categorySales" :key="item.category" class="legend-item">
            <span class="legend-color" :style="{ background: item.color }"></span>
            <span class="legend-label">{{ item.category }}</span>
            <span class="legend-value">{{ item.percentage }}%</span>
          </div>
        </div>
      </div>

      <!-- المنتجات الأكثر مبيعاً -->
      <div class="analytics-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-crown"></i> أفضل المنتجات</h3>
        </div>
        <div class="top-products">
          <div v-for="(product, index) in topProducts" :key="product.id" class="top-product">
            <div class="product-rank" :class="getRankClass(index)">#{{ index + 1 }}</div>
            <div class="product-info">
              <h4>{{ product.name }}</h4>
              <p>{{ product.category }}</p>
            </div>
            <div class="product-stats">
              <span class="product-sales">{{ product.sales }} مبيعات</span>
              <span class="product-revenue">{{ product.revenue }} ر.س</span>
            </div>
          </div>
        </div>
      </div>

      <!-- تحليل العملاء -->
      <div class="analytics-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-users"></i> تحليل العملاء</h3>
        </div>
        <div class="customer-stats">
          <div class="stat-row">
            <span>عملاء جدد</span>
            <strong>{{ customerStats.new }}</strong>
          </div>
          <div class="stat-row">
            <span>عملاء متكررون</span>
            <strong>{{ customerStats.returning }}</strong>
          </div>
          <div class="stat-row">
            <span>متوسط قيمة الطلب</span>
            <strong>{{ formatCurrency(customerStats.avgOrder) }}</strong>
          </div>
          <div class="stat-row">
            <span>القيمة الدائمة للعميل</span>
            <strong>{{ formatCurrency(customerStats.ltv) }}</strong>
          </div>
        </div>
        <div class="retention-rate">
          <div class="rate-header">
            <span>معدل الاحتفاظ بالعملاء</span>
            <strong>{{ customerStats.retention }}%</strong>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: customerStats.retention + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- توقعات المبيعات (AI) -->
      <div class="analytics-card prediction-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-robot"></i> توقعات المبيعات (AI)</h3>
          <span class="prediction-badge">ذكي</span>
        </div>
        <div class="prediction-content">
          <div class="prediction-item">
            <span>الشهر القادم</span>
            <strong>{{ formatCurrency(predictions.nextMonth) }}</strong>
            <span class="prediction-confidence">ثقة {{ predictions.confidence }}%</span>
          </div>
          <div class="prediction-item">
            <span>الربع القادم</span>
            <strong>{{ formatCurrency(predictions.nextQuarter) }}</strong>
          </div>
          <div class="prediction-item">
            <span>العام القادم</span>
            <strong>{{ formatCurrency(predictions.nextYear) }}</strong>
          </div>
        </div>
        <div class="prediction-insight">
          <i class="fa-solid fa-lightbulb"></i>
          <p>{{ predictions.insight }}</p>
        </div>
      </div>

      <!-- تحليل سلة الشراء -->
      <div class="analytics-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-shopping-basket"></i> تحليل سلة الشراء</h3>
        </div>
        <div class="basket-analysis">
          <div class="basket-metrics">
            <div class="metric">
              <span>متوسط حجم السلة</span>
              <strong>{{ basketAnalysis.avgItems }} منتج</strong>
            </div>
            <div class="metric">
              <span>متوسط قيمة السلة</span>
              <strong>{{ formatCurrency(basketAnalysis.avgValue) }}</strong>
            </div>
          </div>
          <h4>المنتجات المشتراة معاً</h4>
          <div v-for="pair in basketAnalysis.productPairs" :key="pair.id" class="product-pair">
            <span>{{ pair.products.join(' + ') }}</span>
            <span class="pair-frequency">{{ pair.frequency }}%</span>
          </div>
        </div>
      </div>

      <!-- تحليل أوقات الذروة -->
      <div class="analytics-card">
        <div class="card-header">
          <h3><i class="fa-solid fa-clock"></i> أوقات الذروة</h3>
        </div>
        <div class="peak-hours">
          <div v-for="hour in peakHours" :key="hour.time" class="hour-row">
            <span class="hour-label">{{ hour.time }}</span>
            <div class="hour-bar">
              <div class="bar-fill" :style="{ width: hour.percentage + '%' }"></div>
            </div>
            <span class="hour-value">{{ hour.orders }} طلب</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
import moment from 'moment';
import CurrencyService from '@/integration/services/CurrencyService';

Chart.register(...registerables);

export default {
  name: 'AdvancedAnalytics',
  data() {
    return {
      selectedRange: 'month',
      dateRanges: [
        { label: 'اليوم', value: 'today' },
        { label: 'أسبوع', value: 'week' },
        { label: 'شهر', value: 'month' },
        { label: 'سنة', value: 'year' },
        { label: 'مخصص', value: 'custom' },
      ],
      customDate: {
        from: moment().subtract(30, 'days').format('YYYY-MM-DD'),
        to: moment().format('YYYY-MM-DD'),
      },
      salesChartType: 'line',

      // مؤشرات الأداء
      kpis: [
        {
          title: 'إجمالي المبيعات',
          value: '845,000 ر.س',
          icon: 'fa-solid fa-chart-line',
          color: '#d4af37',
          trend: 12.5,
        },
        {
          title: 'عدد الطلبات',
          value: '1,234',
          icon: 'fa-solid fa-shopping-cart',
          color: '#2196F3',
          trend: 8.3,
        },
        { title: 'عدد العملاء', value: '892', icon: 'fa-solid fa-users', color: '#4CAF50', trend: 15.7 },
        {
          title: 'متوسط قيمة الطلب',
          value: '450 ر.س',
          icon: 'fa-solid fa-calculator',
          color: '#FF9800',
          trend: -2.1,
        },
      ],

      // المبيعات حسب التصنيف
      categorySales: [
        { category: 'جدران', percentage: 35, color: '#d4af37' },
        { category: 'أبواب', percentage: 25, color: '#2196F3' },
        { category: 'سيارات', percentage: 20, color: '#4CAF50' },
        { category: 'أثاث', percentage: 12, color: '#FF9800' },
        { category: 'مطابخ', percentage: 8, color: '#9C27B0' },
      ],

      // أفضل المنتجات
      topProducts: [
        { id: 1, name: 'ملصق حائط زهور', category: 'جدران', sales: 234, revenue: 10530 },
        { id: 2, name: 'ملصق باب خشبي', category: 'أبواب', sales: 187, revenue: 16643 },
        { id: 3, name: 'إطار سيارة رياضي', category: 'سيارات', sales: 156, revenue: 18720 },
        { id: 4, name: 'ملصق مطبخ فواكه', category: 'مطابخ', sales: 98, revenue: 6370 },
        { id: 5, name: 'ملصق جدار ثلاثي أبعاد', category: 'جدران', sales: 87, revenue: 17400 },
      ],

      // تحليل العملاء
      customerStats: {
        new: 156,
        returning: 234,
        avgOrder: 450,
        ltv: 1850,
        retention: 68,
      },

      // توقعات الذكاء الاصطناعي
      predictions: {
        nextMonth: 95000,
        nextQuarter: 320000,
        nextYear: 1250000,
        confidence: 85,
        insight: 'من المتوقع زيادة المبيعات في فصل الصيف بسبب الطلب على ديكورات المنازل',
      },

      // تحليل سلة الشراء
      basketAnalysis: {
        avgItems: 2.4,
        avgValue: 450,
        productPairs: [
          { id: 1, products: ['ملصق حائط + ملصق باب'], frequency: 35 },
          { id: 2, products: ['إطار سيارة + ملصق جدار'], frequency: 28 },
          { id: 3, products: ['ملصق مطبخ + ملصق أرضيات'], frequency: 22 },
        ],
      },

      // أوقات الذروة
      peakHours: [
        { time: '10-12 صباحاً', orders: 234, percentage: 75 },
        { time: '4-6 مساءً', orders: 312, percentage: 100 },
        { time: '8-10 مساءً', orders: 198, percentage: 63 },
      ],

      charts: {
        sales: null,
        category: null,
      },
    };
  },
  mounted() {
    this.initCharts();
  },
  methods: {
    formatCurrency(value) {
      return CurrencyService.formatAmount(value);
    },

    getRankClass(index) {
      if (index === 0) return 'gold';
      if (index === 1) return 'silver';
      if (index === 2) return 'bronze';
      return '';
    },

    setDateRange(range) {
      this.selectedRange = range;
      if (range !== 'custom') {
        this.updateCharts();
      }
    },

    applyCustomRange() {
      this.updateCharts();
    },

    initCharts() {
      this.initSalesChart();
      this.initCategoryChart();
    },

    initSalesChart() {
      const ctx = this.$refs.salesChart?.getContext('2d');
      if (!ctx) return;

      if (this.charts.sales) {
        this.charts.sales.destroy();
      }

      const labels = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'];
      const data = [4500, 5200, 4800, 6100, 7800, 8200, 6700];

      this.charts.sales = new Chart(ctx, {
        type: this.salesChartType,
        data: {
          labels: labels,
          datasets: [
            {
              label: 'المبيعات',
              data: data,
              backgroundColor: 'rgba(212, 175, 55, 0.2)',
              borderColor: '#d4af37',
              borderWidth: 2,
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(255,255,255,0.1)' },
              ticks: {
                color: '#fff',
                callback: (value) => value.toLocaleString() + ' ر.س',
              },
            },
            x: {
              grid: { display: false },
              ticks: { color: '#fff' },
            },
          },
        },
      });
    },

    initCategoryChart() {
      const ctx = this.$refs.categoryChart?.getContext('2d');
      if (!ctx) return;

      if (this.charts.category) {
        this.charts.category.destroy();
      }

      const data = this.categorySales.map((c) => c.percentage);
      const labels = this.categorySales.map((c) => c.category);
      const colors = this.categorySales.map((c) => c.color);

      this.charts.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: colors,
              borderWidth: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          cutout: '70%',
        },
      });
    },

    updateCharts() {
      // تحديث البيانات من الخادم
      this.initSalesChart();
    },

    refreshData() {
      this.updateCharts();
      this.$toast?.success('تم تحديث البيانات');
    },

    exportAnalytics() {
      // تصدير التحليلات
      this.$toast?.info('جاري تصدير التقرير...');
    },
  },
  watch: {
    salesChartType() {
      this.initSalesChart();
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.advanced-analytics {
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

/* مؤشرات الأداء */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.kpi-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.kpi-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.kpi-content {
  flex: 1;
}

.kpi-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.kpi-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.kpi-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.85rem;
}

.kpi-trend.up {
  color: #4caf50;
}

.kpi-trend.down {
  color: #f44336;
}

.kpi-period {
  color: var(--text-dim);
  font-size: 0.75rem;
  margin-right: 5px;
}

/* فلاتر الوقت */
.filters-bar {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.date-range {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.range-btn {
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 30px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.range-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
}

.range-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.custom-date {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid var(--border-light);
}

.custom-date input {
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

/* شبكة التحليلات */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
}

.analytics-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.analytics-card.large {
  grid-column: span 2;
}

.analytics-card:hover {
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-light);
}

.card-header h3 {
  color: white;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h3 i {
  color: var(--gold-1);
}

.card-actions select {
  padding: 5px 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
}

/* الرسوم البيانية */
.chart-container {
  height: 250px;
  position: relative;
}

.chart-container.pie-chart {
  height: 200px;
}

.chart-legend {
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.legend-label {
  flex: 1;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.legend-value {
  color: white;
  font-weight: 600;
}

/* أفضل المنتجات */
.top-products {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.top-product {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  background: var(--bg-primary);
  border-radius: 12px;
  transition: all 0.3s;
}

.top-product:hover {
  transform: translateX(-5px);
  background: var(--bg-hover);
}

.product-rank {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.product-rank.gold {
  background: linear-gradient(135deg, #ffd700, #ffa500);
  color: #000;
}

.product-rank.silver {
  background: linear-gradient(135deg, #c0c0c0, #a0a0a0);
  color: #000;
}

.product-rank.bronze {
  background: linear-gradient(135deg, #cd7f32, #8b4513);
  color: white;
}

.product-info {
  flex: 1;
}

.product-info h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 3px;
}

.product-info p {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.product-stats {
  text-align: left;
}

.product-sales {
  display: block;
  color: var(--text-dim);
  font-size: 0.8rem;
}

.product-revenue {
  color: var(--gold-1);
  font-weight: 600;
}

/* تحليل العملاء */
.customer-stats {
  margin-bottom: 20px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed var(--border-light);
}

.stat-row span {
  color: var(--text-dim);
}

.stat-row strong {
  color: white;
}

.retention-rate {
  margin-top: 15px;
}

.rate-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-bar {
  height: 8px;
  background: var(--bg-primary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 4px;
  transition: width 0.3s;
}

/* بطاقة التوقعات */
.prediction-card {
  background: linear-gradient(135deg, var(--bg-card), rgba(212, 175, 55, 0.1));
  border-color: var(--gold-1);
}

.prediction-badge {
  padding: 4px 10px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-radius: 30px;
  font-size: 0.7rem;
  font-weight: 700;
}

.prediction-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.prediction-item {
  text-align: center;
  padding: 10px;
  background: var(--bg-primary);
  border-radius: 12px;
}

.prediction-item span {
  display: block;
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.prediction-item strong {
  display: block;
  color: white;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.prediction-confidence {
  color: #4caf50 !important;
  font-size: 0.7rem !important;
}

.prediction-insight {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid #2196f3;
  border-radius: 12px;
}

.prediction-insight i {
  color: #2196f3;
  font-size: 1.2rem;
}

.prediction-insight p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* تحليل سلة الشراء */
.basket-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.metric {
  text-align: center;
  padding: 15px;
  background: var(--bg-primary);
  border-radius: 12px;
}

.metric span {
  display: block;
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.metric strong {
  color: white;
  font-size: 1.1rem;
}

.product-pair {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed var(--border-light);
}

.pair-frequency {
  color: var(--gold-1);
  font-weight: 600;
}

/* أوقات الذروة */
.peak-hours {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hour-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hour-label {
  width: 80px;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.hour-bar {
  flex: 1;
  height: 8px;
  background: var(--bg-primary);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 4px;
  transition: width 0.3s;
}

.hour-value {
  width: 60px;
  color: white;
  font-size: 0.9rem;
  text-align: left;
}

/* استجابة للشاشات الصغيرة */
@media (max-width: 1200px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }

  .analytics-card.large {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .date-range {
    justify-content: center;
  }

  .custom-date {
    flex-direction: column;
  }

  .prediction-content {
    grid-template-columns: 1fr;
  }
}
</style>
