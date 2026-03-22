<template>
  <div class="forecast-dashboard">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-chart-line header-icon"></i>
          توقعات المبيعات
        </h1>
        <p class="header-subtitle">توقعات ذكية للمبيعات والطلب باستخدام الذكاء الاصطناعي</p>
      </div>
      <div class="header-actions">
        <button class="btn-refresh" @click="refreshForecast" :disabled="loading">
          <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
          <span>{{ loading ? 'جاري التحديث...' : 'تحديث' }}</span>
        </button>
      </div>
    </div>

    <!-- تبويبات التنقل -->
    <div class="tabs-container">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'overview' }"
        @click="activeTab = 'overview'"
      >
        <i class="fa-solid fa-chart-pie"></i>
        نظرة عامة
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'inventory' }"
        @click="activeTab = 'inventory'"
      >
        <i class="fa-solid fa-boxes"></i>
        المخزون
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'categories' }"
        @click="activeTab = 'categories'"
      >
        <i class="fa-solid fa-tags"></i>
        التصنيفات
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'abc' }" @click="activeTab = 'abc'">
        <i class="fa-solid fa-chart-pie"></i>
        تحليل ABC
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'seasonality' }"
        @click="
          activeTab = 'seasonality';
          loadSeasonalityAnalysis();
        "
      >
        <i class="fa-solid fa-calendar-alt"></i>
        تحليل الموسمية
      </button>
    </div>

    <!-- محتوى حسب التبويب -->
    <div class="tab-content">
      <!-- ===== تبويب النظرة العامة ===== -->
      <div v-if="activeTab === 'overview'">
        <!-- مؤشرات سريعة -->
        <div class="quick-stats" v-if="forecast">
          <div class="stat-card">
            <div class="stat-icon confidence">
              <i class="fa-solid fa-percent"></i>
            </div>
            <div class="stat-content">
              <span class="stat-label">دقة التوقعات</span>
              <span class="stat-value">{{ forecast.confidence }}%</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon total">
              <i class="fa-solid fa-coins"></i>
            </div>
            <div class="stat-content">
              <span class="stat-label">الشهر القادم</span>
              <span class="stat-value">{{ formatCurrency(forecast.details.nextMonth) }}</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon trend" :class="forecast.trends.trend">
              <i :class="getTrendIcon(forecast.trends.trend)"></i>
            </div>
            <div class="stat-content">
              <span class="stat-label">الاتجاه</span>
              <span class="stat-value">{{ getTrendText(forecast.trends) }}</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon data">
              <i class="fa-solid fa-database"></i>
            </div>
            <div class="stat-content">
              <span class="stat-label">بيانات</span>
              <span class="stat-value">{{ forecast.basedOn }}</span>
            </div>
          </div>
        </div>

        <!-- الرسم البياني للتوقعات -->
        <div class="chart-card" v-if="forecast">
          <div class="card-header">
            <h3><i class="fa-solid fa-chart-line"></i> توقعات المبيعات (30 يوم)</h3>
            <div class="chart-legend">
              <span class="legend-item"> <span class="color-dot actual"></span> مبيعات سابقة </span>
              <span class="legend-item"> <span class="color-dot predicted"></span> توقعات </span>
            </div>
          </div>
          <div class="chart-container">
            <canvas ref="forecastChart"></canvas>
          </div>
        </div>
      </div>

      <!-- ===== تبويب المخزون ===== -->
      <div v-if="activeTab === 'inventory'" class="inventory-tab">
        <div class="inventory-forecast" v-if="inventoryForecast">
          <div class="section-header">
            <h3><i class="fa-solid fa-exclamation-triangle"></i> تنبيهات المخزون الحرجة</h3>
          </div>

          <div class="alerts-grid">
            <div
              v-for="item in inventoryForecast.critical"
              :key="item.productId"
              class="alert-card critical"
            >
              <div class="alert-icon">
                <i class="fa-solid fa-exclamation-triangle"></i>
              </div>
              <div class="alert-content">
                <h4>{{ item.productName }}</h4>
                <p>المخزون: {{ item.currentStock }} قطعة</p>
                <p>متوسط المبيعات: {{ Math.round(item.dailyAverage) }}/يوم</p>
                <p class="warning">سينفد خلال {{ item.daysUntilZero }} يوم</p>
              </div>
              <button class="btn-order" @click="orderProduct(item)">
                <i class="fa-solid fa-shopping-cart"></i> طلب
              </button>
            </div>

            <div
              v-for="item in inventoryForecast.warning"
              :key="item.productId"
              class="alert-card warning"
            >
              <div class="alert-icon">
                <i class="fa-solid fa-exclamation"></i>
              </div>
              <div class="alert-content">
                <h4>{{ item.productName }}</h4>
                <p>المخزون: {{ item.currentStock }} قطعة</p>
                <p>ينصح بالشراء خلال {{ item.daysUntilZero }} يوم</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب التصنيفات ===== -->
      <div v-if="activeTab === 'categories'" class="categories-tab">
        <div class="categories-section" v-if="categoryForecasts.length">
          <div class="section-header">
            <h3><i class="fa-solid fa-tags"></i> توقعات حسب التصنيف</h3>
          </div>

          <div class="categories-grid">
            <div v-for="cat in categoryForecasts" :key="cat.category" class="category-card">
              <h4>{{ getCategoryName(cat.category) }}</h4>
              <div class="category-stats">
                <div class="stat">
                  <span>الشهر القادم</span>
                  <strong>{{ formatCurrency(cat.forecast.total) }}</strong>
                </div>
                <div class="trend-badge" :class="cat.trends.trend">
                  <i :class="getTrendIcon(cat.trends.trend)"></i>
                  {{ Math.abs(cat.trends.change) }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب تحليل ABC ===== -->
      <div v-if="activeTab === 'abc'" class="abc-tab">
        <div v-if="loadingABC" class="loading-state">
          <div class="loading-spinner"></div>
          <p>جاري تحليل البيانات...</p>
        </div>

        <div v-else-if="abcData" class="abc-container">
          <!-- بطاقات ملخص ABC -->
          <div class="abc-summary-cards">
            <div class="summary-card class-a">
              <div class="card-header">
                <i class="fa-solid fa-crown"></i>
                <h3>فئة A</h3>
              </div>
              <div class="card-content">
                <div class="stat">
                  <span class="label">عدد المنتجات</span>
                  <span class="value">{{ abcData.stats.A }}</span>
                </div>
                <div class="stat">
                  <span class="label">الإيرادات</span>
                  <span class="value">{{ formatCurrency(abcData.stats.revenueA) }}</span>
                </div>
                <div class="stat">
                  <span class="label">النسبة</span>
                  <span class="value"
                    >{{ ((abcData.stats.revenueA / abcData.totalRevenue) * 100).toFixed(1) }}%</span
                  >
                </div>
              </div>
            </div>

            <div class="summary-card class-b">
              <div class="card-header">
                <i class="fa-solid fa-chart-line"></i>
                <h3>فئة B</h3>
              </div>
              <div class="card-content">
                <div class="stat">
                  <span class="label">عدد المنتجات</span>
                  <span class="value">{{ abcData.stats.B }}</span>
                </div>
                <div class="stat">
                  <span class="label">الإيرادات</span>
                  <span class="value">{{ formatCurrency(abcData.stats.revenueB) }}</span>
                </div>
                <div class="stat">
                  <span class="label">النسبة</span>
                  <span class="value"
                    >{{ ((abcData.stats.revenueB / abcData.totalRevenue) * 100).toFixed(1) }}%</span
                  >
                </div>
              </div>
            </div>

            <div class="summary-card class-c">
              <div class="card-header">
                <i class="fa-solid fa-box"></i>
                <h3>فئة C</h3>
              </div>
              <div class="card-content">
                <div class="stat">
                  <span class="label">عدد المنتجات</span>
                  <span class="value">{{ abcData.stats.C }}</span>
                </div>
                <div class="stat">
                  <span class="label">الإيرادات</span>
                  <span class="value">{{ formatCurrency(abcData.stats.revenueC) }}</span>
                </div>
                <div class="stat">
                  <span class="label">النسبة</span>
                  <span class="value"
                    >{{ ((abcData.stats.revenueC / abcData.totalRevenue) * 100).toFixed(1) }}%</span
                  >
                </div>
              </div>
            </div>
          </div>

          <!-- رسم بياني ABC -->
          <div class="abc-chart-container">
            <div class="chart-header">
              <h3><i class="fa-solid fa-chart-pie"></i> توزيع الإيرادات حسب الفئة</h3>
            </div>
            <div class="abc-bars">
              <div class="bar-item">
                <span class="bar-label">A</span>
                <div class="bar-wrapper">
                  <div
                    class="bar-fill class-a"
                    :style="{ width: (abcData.stats.revenueA / abcData.totalRevenue) * 100 + '%' }"
                  >
                    {{ ((abcData.stats.revenueA / abcData.totalRevenue) * 100).toFixed(1) }}%
                  </div>
                </div>
              </div>
              <div class="bar-item">
                <span class="bar-label">B</span>
                <div class="bar-wrapper">
                  <div
                    class="bar-fill class-b"
                    :style="{ width: (abcData.stats.revenueB / abcData.totalRevenue) * 100 + '%' }"
                  >
                    {{ ((abcData.stats.revenueB / abcData.totalRevenue) * 100).toFixed(1) }}%
                  </div>
                </div>
              </div>
              <div class="bar-item">
                <span class="bar-label">C</span>
                <div class="bar-wrapper">
                  <div
                    class="bar-fill class-c"
                    :style="{ width: (abcData.stats.revenueC / abcData.totalRevenue) * 100 + '%' }"
                  >
                    {{ ((abcData.stats.revenueC / abcData.totalRevenue) * 100).toFixed(1) }}%
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- توصيات ABC -->
          <div
            class="abc-recommendations"
            v-if="abcData.recommendations && abcData.recommendations.length"
          >
            <h3><i class="fa-solid fa-lightbulb"></i> توصيات ذكية</h3>
            <div class="recommendations-grid">
              <div
                v-for="rec in abcData.recommendations"
                :key="rec.type"
                class="recommendation-card"
                :style="{ borderTopColor: rec.color }"
              >
                <div class="rec-header">
                  <i :class="rec.icon" :style="{ color: rec.color }"></i>
                  <h4>{{ rec.title }}</h4>
                </div>
                <p class="rec-message">{{ rec.message }}</p>
                <p class="rec-action">{{ rec.action }}</p>
                <div class="rec-products" v-if="rec.products && rec.products.length">
                  <span class="products-label">أمثلة:</span>
                  <span class="products-list">{{ rec.products.join('، ') }}</span>
                </div>
              </div>
            </div>
            <button
              class="tab-btn"
              :class="{ active: activeTab === 'seasonality' }"
              @click="
                activeTab = 'seasonality';
                loadSeasonalityAnalysis();
              "
            >
              <i class="fa-solid fa-calendar-alt"></i>
              تحليل الموسمية
            </button>
          </div>

          <!-- ===== تبويب تحليل الموسمية ===== -->
          <div v-if="activeTab === 'seasonality'" class="seasonality-tab">
            <div v-if="loadingSeasonality" class="loading-state">
              <div class="loading-spinner"></div>
              <p>جاري تحليل الأنماط الموسمية...</p>
            </div>

            <div
              v-else-if="seasonalityData && seasonalityData.success"
              class="seasonality-container"
            >
              <!-- بطاقات الرؤى -->
              <div class="insights-cards" v-if="seasonalityData.insights?.length">
                <div
                  v-for="insight in seasonalityData.insights"
                  :key="insight.type"
                  class="insight-card"
                >
                  <div class="insight-icon">{{ insight.icon }}</div>
                  <div class="insight-content">
                    <h4>{{ insight.title }}</h4>
                    <p>{{ insight.message }}</p>
                    <small v-if="insight.recommendation">{{ insight.recommendation }}</small>
                  </div>
                </div>
              </div>

              <!-- تحليل شهري -->
              <div class="analysis-section" v-if="seasonalityData.monthly">
                <h3><i class="fa-solid fa-calendar"></i> التحليل الشهري</h3>
                <div class="monthly-grid">
                  <div
                    v-for="(data, month) in seasonalityData.monthly"
                    :key="month"
                    class="month-card"
                    :class="data.peak"
                  >
                    <div class="month-header">
                      <span class="month-name">{{ getMonthName(parseInt(month)) }}</span>
                      <span class="month-badge">{{
                        data.peak === 'high' ? 'نشط' : data.peak === 'low' ? 'هادئ' : 'عادي'
                      }}</span>
                    </div>
                    <div class="month-stats">
                      <div class="stat">
                        <span class="label">المتوسط</span>
                        <span class="value">{{ formatCurrency(data.avg) }}</span>
                      </div>
                      <div class="stat">
                        <span class="label">الإجمالي</span>
                        <span class="value">{{ formatCurrency(data.total) }}</span>
                      </div>
                    </div>
                    <div class="month-bar">
                      <div
                        class="bar-fill"
                        :style="{ width: (data.avg / maxMonthlyAvg) * 100 + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- تحليل أسبوعي -->
              <div class="analysis-section" v-if="seasonalityData.weekly">
                <h3><i class="fa-solid fa-calendar-week"></i> التحليل الأسبوعي</h3>
                <div class="weekly-grid">
                  <div
                    v-for="(data, day) in seasonalityData.weekly"
                    :key="day"
                    class="day-card"
                    :class="{ weekend: data.isWeekend }"
                  >
                    <div class="day-name">{{ data.name }}</div>
                    <div class="day-value">{{ formatCurrency(data.avg) }}</div>
                    <div class="day-bar">
                      <div
                        class="bar-fill"
                        :style="{ width: (data.avg / maxWeeklyAvg) * 100 + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- المواسم الخاصة -->
              <div class="analysis-section" v-if="seasonalityData.specialSeasons">
                <h3><i class="fa-solid fa-star"></i> المواسم الخاصة</h3>
                <div class="seasons-grid">
                  <div
                    v-for="(data, key) in seasonalityData.specialSeasons"
                    :key="key"
                    class="season-card"
                    :class="data.trend"
                  >
                    <div class="season-header">
                      <span class="season-name">{{ data.name }}</span>
                      <span
                        class="season-impact"
                        :class="{ positive: data.impact > 0, negative: data.impact < 0 }"
                      >
                        {{ data.impact > 0 ? '+' : '' }}{{ data.impact }}%
                      </span>
                    </div>
                    <div class="season-details">
                      <p>{{ data.recommendation }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- توصيات موسمية -->
              <div class="recommendations-section" v-if="seasonalityData.recommendations?.length">
                <h3><i class="fa-solid fa-lightbulb"></i> توصيات موسمية</h3>
                <div class="rec-cards">
                  <div
                    v-for="rec in seasonalityData.recommendations"
                    :key="rec.title"
                    class="rec-card"
                    :style="{ borderRightColor: rec.color }"
                  >
                    <div class="rec-icon">
                      <i :class="rec.icon" :style="{ color: rec.color }"></i>
                    </div>
                    <div class="rec-content">
                      <h4>{{ rec.title }}</h4>
                      <p>{{ rec.message }}</p>
                      <small>{{ rec.action }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="seasonalityData && !seasonalityData.success" class="error-state">
              <i class="fa-solid fa-exclamation-triangle"></i>
              <p>{{ seasonalityData.message || 'لا توجد بيانات كافية للتحليل' }}</p>
            </div>
          </div>

          <!-- جدول تفاصيل المنتجات -->
          <div class="abc-products-table">
            <div class="table-header">
              <h3><i class="fa-solid fa-table"></i> تفاصيل المنتجات</h3>
              <div class="filter-buttons">
                <button @click="filterABC = 'all'" :class="{ active: filterABC === 'all' }">
                  الكل
                </button>
                <button @click="filterABC = 'A'" :class="{ active: filterABC === 'A' }">A</button>
                <button @click="filterABC = 'B'" :class="{ active: filterABC === 'B' }">B</button>
                <button @click="filterABC = 'C'" :class="{ active: filterABC === 'C' }">C</button>
              </div>
            </div>

            <table class="products-table">
              <thead>
                <tr>
                  <th>المنتج</th>
                  <th>التصنيف</th>
                  <th>المخزون</th>
                  <th>الإيرادات</th>
                  <th>متوسط يومي</th>
                  <th>الفئة</th>
                  <th>النسبة</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in filteredABCProducts" :key="product.id">
                  <td>
                    <strong>{{ product.name }}</strong>
                  </td>
                  <td>{{ getCategoryName(product.category) }}</td>
                  <td>{{ product.stock }}</td>
                  <td>{{ formatCurrency(product.totalRevenue) }}</td>
                  <td>{{ product.dailyAverage }}</td>
                  <td>
                    <span class="abc-badge" :class="'class-' + product.classification">
                      {{ product.classification }}
                    </span>
                  </td>
                  <td>{{ product.cumulativePercent }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ForecastService from '@/integration/ai/forecasting/ForecastService';
import Chart from 'chart.js/auto';
import CurrencyService from '@/integration/services/CurrencyService';

export default {
  name: 'ForecastDashboard',
  data() {
    return {
      loading: false,
      forecast: null,
      inventoryForecast: null,
      categoryForecasts: [],
      chart: null,
      activeTab: 'overview',
      abcData: null,
      loadingABC: false,
      filterABC: 'all',
      seasonalityData: null,
      loadingSeasonality: false,
      maxMonthlyAvg: 0,
      maxWeeklyAvg: 0,
    };
  },
  computed: {
    filteredABCProducts() {
      if (!this.abcData?.products) return [];
      if (this.filterABC === 'all') return this.abcData.products;
      return this.abcData.products.filter((p) => p.classification === this.filterABC);
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    formatCurrency(value) {
      return CurrencyService.formatAmount(value || 0);
    },

    async loadData() {
      this.loading = true;

      try {
        // توقعات عامة
        this.forecast = await ForecastService.getGeneralForecast(30);

        // توقعات المخزون
        this.inventoryForecast = await ForecastService.getInventoryForecast();

        // توقعات الفئات
        await this.loadCategoryForecasts();

        // تحليل ABC
        await this.loadABCAnalysis();

        this.$nextTick(() => {
          this.initChart();
        });
      } catch (error) {
        console.error('Error loading forecast:', error);
      } finally {
        this.loading = false;
      }
    },

    async loadCategoryForecasts() {
      const categories = ['walls', 'doors', 'cars', 'kitchens'];
      this.categoryForecasts = [];

      for (const cat of categories) {
        const result = await ForecastService.getCategoryForecast(cat, 30);
        if (result.success) {
          this.categoryForecasts.push(result);
        }
      }
    },

    async loadABCAnalysis() {
      this.loadingABC = true;
      try {
        const result = await ForecastService.analyzeABC(365);
        this.abcData = result;
      } catch (error) {
        console.error('خطأ في تحليل ABC:', error);
      } finally {
        this.loadingABC = false;
      }
    },

    initChart() {
      if (!this.forecast || !this.forecast.predictions) return;

      const ctx = this.$refs.forecastChart?.getContext('2d');
      if (!ctx) return;

      if (this.chart) this.chart.destroy();

      // بيانات تاريخية (آخر 30 يوم)
      const historicalData = this.forecast.predictions.slice(-30);
      const forecastData = this.forecast.predictions;

      const labels = [];
      for (let i = 1; i <= 30; i++) {
        labels.push(`يوم ${i}`);
      }

      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'مبيعات سابقة',
              data: historicalData,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.4,
            },
            {
              label: 'توقعات',
              data: forecastData,
              borderColor: '#d4af37',
              backgroundColor: 'rgba(212, 175, 55, 0.1)',
              borderDash: [5, 5],
              tension: 0.4,
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

    async refreshForecast() {
      this.loadData();
    },

    getTrendIcon(trend) {
      const icons = {
        rising: 'fa-solid fa-arrow-up',
        strong_rise: 'fa-solid fa-arrow-up',
        falling: 'fa-solid fa-arrow-down',
        strong_fall: 'fa-solid fa-arrow-down',
        stable: 'fa-solid fa-minus',
      };
      return icons[trend] || 'fa-solid fa-minus';
    },

    getTrendText(trends) {
      if (trends.change > 0) {
        return `ارتفاع ${trends.change}%`;
      } else if (trends.change < 0) {
        return `انخفاض ${Math.abs(trends.change)}%`;
      }
      return 'مستقر';
    },

    getCategoryName(category) {
      const names = {
        walls: 'جدران',
        doors: 'أبواب',
        cars: 'سيارات',
        kitchens: 'مطابخ',
        furniture: 'أثاث',
        ceilings: 'أسقف',
        tiles: 'بلاط',
      };
      return names[category] || category;
    },

    orderProduct(item) {
      alert(`سيتم إنشاء أمر شراء لـ ${item.productName} (${item.suggestedOrder || 0} قطعة)`);
    },

    async loadSeasonalityAnalysis() {
      this.loadingSeasonality = true;
      try {
        const result = await ForecastService.analyzeAdvancedSeasonality();
        this.seasonalityData = result;

        if (result.monthly) {
          this.maxMonthlyAvg = Math.max(...Object.values(result.monthly).map((m) => m.avg));
        }
        if (result.weekly) {
          this.maxWeeklyAvg = Math.max(...Object.values(result.weekly).map((w) => w.avg));
        }
      } catch (error) {
        console.error('خطأ في تحليل الموسمية:', error);
      } finally {
        this.loadingSeasonality = false;
      }
    },

    getMonthName(month) {
      const months = [
        'يناير',
        'فبراير',
        'مارس',
        'إبريل',
        'مايو',
        'يونيو',
        'يوليو',
        'أغسطس',
        'سبتمبر',
        'أكتوبر',
        'نوفمبر',
        'ديسمبر',
      ];
      return months[month] || '';
    },

    watch: {
      activeTab(newVal) {
        if (newVal === 'seasonality' && !this.seasonalityData) {
          this.loadSeasonalityAnalysis();
        }
      },
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.forecast-dashboard {
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

.btn-refresh {
  padding: 12px 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: var(--gold-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-refresh:hover:not(:disabled) {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: translateY(-3px);
}

/* ===== التبويبات ===== */
.tabs-container {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 10px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
}

.tab-btn {
  flex: 1;
  padding: 12px 20px;
  background: transparent;
  border: none;
  border-radius: 16px;
  color: var(--text-dim);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.tab-btn:hover {
  color: var(--gold-1);
  background: rgba(212, 175, 55, 0.1);
}

.tab-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.tab-content {
  animation: fadeIn 0.5s ease;
}

/* ===== مؤشرات سريعة ===== */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.confidence {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.stat-icon.total {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.stat-icon.trend.rising {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.stat-icon.trend.falling {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.stat-icon.trend.stable {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.stat-icon.data {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-1);
}

.stat-content {
  flex: 1;
}

.stat-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  color: white;
  font-size: 1.2rem;
  font-weight: 700;
}

/* ===== الرسم البياني ===== */
.chart-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  color: white;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header h3 i {
  color: var(--gold-1);
}

.chart-legend {
  display: flex;
  gap: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-dim);
  font-size: 0.85rem;
}

.color-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.color-dot.actual {
  background: #2196f3;
}

.color-dot.predicted {
  background: #d4af37;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* ===== المخزون ===== */
.inventory-forecast {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.section-header {
  margin-bottom: 20px;
}

.section-header h3 {
  color: white;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h3 i {
  color: var(--gold-1);
}

.alerts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.alert-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 16px;
  border: 1px solid;
}

.alert-card.critical {
  background: rgba(244, 67, 54, 0.1);
  border-color: #f44336;
}

.alert-card.warning {
  background: rgba(255, 152, 0, 0.1);
  border-color: #ff9800;
}

.alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.alert-card.critical .alert-icon {
  background: #f44336;
  color: white;
}

.alert-card.warning .alert-icon {
  background: #ff9800;
  color: white;
}

.alert-content {
  flex: 1;
}

.alert-content h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.alert-content p {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin: 2px 0;
}

.alert-content .warning {
  color: #f44336;
  font-weight: 600;
}

.btn-order {
  padding: 6px 12px;
  background: var(--gold-gradient);
  border: none;
  border-radius: 8px;
  color: var(--bg-deep);
  cursor: pointer;
  font-size: 0.8rem;
  white-space: nowrap;
  transition: all 0.3s;
}

.btn-order:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

/* ===== التصنيفات ===== */
.categories-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.category-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.category-card:hover {
  transform: translateY(-3px);
  border-color: var(--gold-1);
}

.category-card h4 {
  color: white;
  font-size: 1rem;
  margin-bottom: 10px;
}

.category-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat span {
  display: block;
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 3px;
}

.stat strong {
  color: white;
  font-size: 1.1rem;
}

.trend-badge {
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 3px;
}

.trend-badge.rising {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.trend-badge.falling {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.trend-badge.stable {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

/* ===== تحليل ABC ===== */
.loading-state {
  text-align: center;
  padding: 50px;
  color: var(--text-dim);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(212, 175, 55, 0.3);
  border-top-color: var(--gold-1);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.abc-summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.summary-card.class-a {
  border-top: 4px solid #d4af37;
}

.summary-card.class-b {
  border-top: 4px solid #2196f3;
}

.summary-card.class-c {
  border-top: 4px solid #4caf50;
}

.summary-card .card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.summary-card .card-header i {
  font-size: 1.5rem;
}

.summary-card.class-a i {
  color: #d4af37;
}

.summary-card.class-b i {
  color: #2196f3;
}

.summary-card.class-c i {
  color: #4caf50;
}

.summary-card .card-header h3 {
  color: white;
  font-size: 1.1rem;
}

.summary-card .stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.summary-card .stat .label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.summary-card .stat .value {
  color: white;
  font-weight: 600;
}

.abc-chart-container {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 30px;
  border: 1px solid var(--border-light);
}

.abc-bars {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.bar-label {
  width: 30px;
  color: white;
  font-weight: 600;
}

.bar-wrapper {
  flex: 1;
  height: 40px;
  background: var(--bg-primary);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 15px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: width 0.5s;
}

.bar-fill.class-a {
  background: linear-gradient(90deg, #d4af37, #f5e7b2);
}

.bar-fill.class-b {
  background: linear-gradient(90deg, #2196f3, #90caf9);
}

.bar-fill.class-c {
  background: linear-gradient(90deg, #4caf50, #a5d6a7);
}

.abc-recommendations {
  margin-bottom: 30px;
}

.abc-recommendations h3 {
  color: white;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.recommendation-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid var(--border-light);
  border-top-width: 4px;
  transition: all 0.3s;
}

.recommendation-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-gold);
}

.rec-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.rec-header i {
  font-size: 1.5rem;
}

.rec-header h4 {
  color: white;
  font-size: 1rem;
}

.rec-message {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 8px;
  line-height: 1.4;
}

.rec-action {
  color: var(--gold-1);
  font-size: 0.85rem;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px dashed var(--border-light);
}

.rec-products {
  background: var(--bg-primary);
  padding: 10px;
  border-radius: 12px;
}

.products-label {
  color: var(--text-dim);
  font-size: 0.8rem;
  display: block;
  margin-bottom: 5px;
}

.products-list {
  color: white;
  font-size: 0.9rem;
  line-height: 1.4;
}

.abc-products-table {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-buttons {
  display: flex;
  gap: 8px;
}

.filter-buttons button {
  padding: 6px 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.3s;
}

.filter-buttons button.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.abc-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.abc-badge.class-a {
  background: rgba(212, 175, 55, 0.2);
  color: #d4af37;
  border: 1px solid #d4af37;
}

.abc-badge.class-b {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid #2196f3;
}

.abc-badge.class-c {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
}

@media (max-width: 768px) {
  .tabs-container {
    flex-wrap: wrap;
  }

  .tab-btn {
    flex: auto;
    min-width: 120px;
  }

  .abc-summary-cards {
    grid-template-columns: 1fr;
  }

  .table-header {
    flex-direction: column;
    gap: 15px;
  }

  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .alerts-grid {
    grid-template-columns: 1fr;
  }
}

/* ===== تحليل الموسمية ===== */
.seasonality-tab {
  padding: 20px 0;
}

.insights-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.insight-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
}

.insight-icon {
  font-size: 2rem;
}

.insight-content h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.insight-content p {
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 3px;
}

.insight-content small {
  color: var(--gold-1);
  font-size: 0.75rem;
}

.analysis-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.analysis-section h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.analysis-section h3 i {
  color: var(--gold-1);
}

.monthly-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.month-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.month-card.high {
  border-right: 4px solid #4caf50;
}

.month-card.low {
  border-right: 4px solid #f44336;
}

.month-card.normal {
  border-right: 4px solid #ff9800;
}

.month-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.month-name {
  color: white;
  font-weight: 600;
}

.month-badge {
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 20px;
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-1);
}

.month-stats {
  margin-bottom: 10px;
}

.stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.stat .label {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.stat .value {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.month-bar {
  height: 6px;
  background: var(--bg-card);
  border-radius: 3px;
  overflow: hidden;
}

.month-bar .bar-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 3px;
}

.weekly-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
}

.day-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.day-card.weekend {
  background: rgba(212, 175, 55, 0.05);
  border-color: var(--gold-1);
}

.day-name {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.day-value {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.day-bar {
  height: 4px;
  background: var(--bg-card);
  border-radius: 2px;
  overflow: hidden;
}

.day-bar .bar-fill {
  height: 100%;
  background: var(--gold-gradient);
  border-radius: 2px;
}

.seasons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.season-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  border: 1px solid var(--border-light);
}

.season-card.high {
  border-right: 4px solid #4caf50;
}

.season-card.low {
  border-right: 4px solid #f44336;
}

.season-card.normal {
  border-right: 4px solid #ff9800;
}

.season-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.season-name {
  color: white;
  font-weight: 600;
}

.season-impact {
  font-weight: 600;
  font-size: 0.9rem;
}

.season-impact.positive {
  color: #4caf50;
}

.season-impact.negative {
  color: #f44336;
}

.season-details p {
  color: var(--text-dim);
  font-size: 0.85rem;
  line-height: 1.4;
}

.rec-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.rec-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  display: flex;
  gap: 12px;
  border: 1px solid var(--border-light);
  border-right-width: 4px;
}

.rec-icon i {
  font-size: 1.5rem;
}

.rec-content h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.rec-content p {
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 5px;
}

.rec-content small {
  color: var(--gold-1);
  font-size: 0.75rem;
}

.error-state {
  text-align: center;
  padding: 50px;
  color: var(--text-dim);
}

.error-state i {
  font-size: 3rem;
  color: #f44336;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .weekly-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .insights-cards {
    grid-template-columns: 1fr;
  }
}
</style>
