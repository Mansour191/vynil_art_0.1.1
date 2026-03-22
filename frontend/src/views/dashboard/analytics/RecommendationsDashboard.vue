<template>
  <div class="recommendations-dashboard">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-star header-icon"></i>
          نظام التوصيات الذكي
        </h1>
        <p class="header-subtitle">توصيات مخصصة للمنتجات بناءً على تحليل سلوك العملاء</p>
      </div>

      <div class="header-actions">
        <button class="btn-refresh" @click="refreshModels" :disabled="loading">
          <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
          <span>{{ loading ? 'جاري التحديث...' : 'تحديث النماذج' }}</span>
        </button>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="stats-cards" v-if="analytics">
      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(212, 175, 55, 0.1); color: #d4af37">
          <i class="fa-solid fa-percent"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ (analytics.clickThroughRate * 100).toFixed(1) }}%</span>
          <span class="stat-label">نسبة النقر</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(76, 175, 80, 0.1); color: #4caf50">
          <i class="fa-solid fa-shopping-cart"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ (analytics.conversionRate * 100).toFixed(1) }}%</span>
          <span class="stat-label">نسبة التحويل</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(33, 150, 243, 0.1); color: #2196f3">
          <i class="fa-solid fa-coins"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ formatCurrency(analytics.averageOrderValue) }}</span>
          <span class="stat-label">متوسط الطلب</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: rgba(156, 39, 176, 0.1); color: #9c27b0">
          <i class="fa-solid fa-box"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ analytics.totalRecommendations }}</span>
          <span class="stat-label">إجمالي التوصيات</span>
        </div>
      </div>
    </div>

    <!-- تبويبات -->
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
        :class="{ active: activeTab === 'general' }"
        @click="
          loadGeneralRecommendations();
          activeTab = 'general';
        "
      >
        <i class="fa-solid fa-fire"></i>
        الأكثر مبيعاً
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'trending' }"
        @click="
          loadTrendingProducts();
          activeTab = 'trending';
        "
      >
        <i class="fa-solid fa-chart-line"></i>
        رائج الآن
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'advanced' }"
        @click="activeTab = 'advanced'"
      >
        <i class="fa-solid fa-analytics"></i>
        تحليلات متقدمة
      </button>

      <!--  زر جديد -->
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'performance' }"
        @click="
          loadPerformance();
          activeTab = 'performance';
        "
      >
        <i class="fa-solid fa-chart-bar"></i>
        أداء التوصيات
      </button>

      <!-- محتوى التبويب -->
      <div v-if="activeTab === 'performance'" class="performance-tab">
        <div class="performance-header">
          <h3><i class="fa-solid fa-chart-line"></i> أداء التوصيات (آخر 30 يوم)</h3>
        </div>

        <div class="performance-stats" v-if="performance">
          <div class="stat-card">
            <div class="stat-value">{{ performance.total.clicks }}</div>
            <div class="stat-label">إجمالي النقرات</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ performance.total.conversions }}</div>
            <div class="stat-label">تحويلات</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ (performance.total.ctr * 100).toFixed(1) }}%</div>
            <div class="stat-label">معدل التحويل</div>
          </div>
        </div>

        <div class="performance-by-type" v-if="performance">
          <h4>الأداء حسب نوع التوصية</h4>
          <div class="type-grid">
            <div v-for="(stat, type) in performance.byType" :key="type" class="type-card">
              <div class="type-name">{{ getTypeName(type) }}</div>
              <div class="type-stats">
                <span>نقرات: {{ stat.clicks }}</span>
                <span>تحويلات: {{ stat.conversions }}</span>
                <span>نسبة: {{ ((stat.conversions / stat.clicks) * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- محتوى التبويبات -->
    <div class="tab-content">
      <!-- تبويب النظرة العامة -->
      <div v-if="activeTab === 'overview'" class="overview-tab">
        <!-- أفضل الفئات -->
        <div class="category-performance" v-if="analytics">
          <h3><i class="fa-solid fa-trophy"></i> أفضل الفئات أداءً</h3>
          <div class="category-list">
            <div
              v-for="cat in analytics.topPerformingCategories"
              :key="cat.category"
              class="category-item"
            >
              <span class="category-name">{{ getCategoryName(cat.category) }}</span>
              <div class="category-bar">
                <div class="bar-fill" :style="{ width: (cat.revenue / 50000) * 100 + '%' }"></div>
              </div>
              <span class="category-revenue">{{ formatCurrency(cat.revenue) }}</span>
            </div>
          </div>
        </div>

        <!-- توصيات عامة -->
        <div class="recommendations-section">
          <h3><i class="fa-solid fa-fire"></i> الأكثر مبيعاً</h3>
          <RecommendationsWidget
            :products="generalRecommendations"
            :loading="loadingGeneral"
            horizontal
            viewAllLink="/dashboard/recommendations?tab=general"
          />
        </div>

        <!-- رائج الآن -->
        <div class="recommendations-section">
          <h3><i class="fa-solid fa-chart-line"></i> رائج الآن</h3>
          <RecommendationsWidget
            :products="trendingProducts"
            :loading="loadingTrending"
            horizontal
            viewAllLink="/dashboard/recommendations?tab=trending"
          />
        </div>
      </div>

      <!-- تبويب الأكثر مبيعاً -->
      <div v-if="activeTab === 'general'" class="general-tab">
        <RecommendationsWidget
          :products="generalRecommendations"
          :loading="loadingGeneral"
          title="المنتجات الأكثر مبيعاً"
          icon="fa-solid fa-crown"
        />
      </div>

      <!-- تبويب رائج الآن -->
      <div v-if="activeTab === 'trending'" class="trending-tab">
        <RecommendationsWidget
          :products="trendingProducts"
          :loading="loadingTrending"
          title="المنتجات الرائجة هذا الأسبوع"
          icon="fa-solid fa-fire"
        />
      </div>

      <!-- تبويب تحليلات متقدمة -->
      <div v-if="activeTab === 'advanced'" class="advanced-tab">
        <div class="advanced-grid">
          <!-- بطاقة أداء التوصيات -->
          <div class="analytics-card">
            <h4><i class="fa-solid fa-chart-line"></i> أداء التوصيات</h4>
            <canvas ref="performanceChart"></canvas>
          </div>

          <!-- بطاقة الفئات الأكثر توصية -->
          <div class="analytics-card">
            <h4><i class="fa-solid fa-tags"></i> الفئات الأكثر توصية</h4>
            <div class="category-list">
              <div v-for="cat in categoryPerformance" :key="cat.name" class="category-stat">
                <span>{{ cat.name }}</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: cat.percentage + '%' }"></div>
                </div>
                <span>{{ cat.count }} توصية</span>
              </div>
            </div>
          </div>

          <!-- بطاقة أنماط الشراء -->
          <div class="analytics-card">
            <h4><i class="fa-solid fa-clock"></i> أنماط الشراء</h4>
            <div class="patterns-list">
              <div class="pattern-item">
                <i class="fa-solid fa-clock"></i>
                <span>أوقات الذروة: الخميس والجمعة</span>
              </div>
              <div class="pattern-item">
                <i class="fa-solid fa-sun"></i>
                <span>الموسم النشط: الصيف</span>
              </div>
              <div class="pattern-item">
                <i class="fa-solid fa-gift"></i>
                <span>أعلى مبيعات: نهاية السنة</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- قسم توصيات المخصصة (للمدير) -->
    <div class="personalized-section" v-if="recommendationStats">
      <h2>
        <i class="fa-solid fa-chart-line"></i>
        أداء نظام التوصيات
      </h2>

      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">إجمالي التوصيات</span>
          <span class="stat-value">{{ recommendationStats.total }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">نسبة النقر</span>
          <span class="stat-value">{{ recommendationStats.ctr }}%</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">نسبة التحويل</span>
          <span class="stat-value">{{ recommendationStats.conversionRate }}%</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">إيرادات التوصيات</span>
          <span class="stat-value">{{ formatCurrency(recommendationStats.revenue) }}</span>
        </div>
      </div>

      <div class="top-recommendations">
        <h3><i class="fa-solid fa-star"></i> أفضل التوصيات أداءً</h3>
        <div class="recommendations-list">
          <div v-for="rec in topPerformingRecommendations" :key="rec.id" class="rec-item">
            <span class="rec-name">{{ rec.productName }}</span>
            <span class="rec-clicks">{{ rec.clicks }} نقرة</span>
            <span class="rec-conversions">{{ rec.conversions }} تحويل</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RecommendationService from '@/integration/ai/recommendations/RecommendationService';
import CurrencyService from '@/integration/services/CurrencyService';
import RecommendationsWidget from '@/components/RecommendationsWidget.vue';
import Chart from 'chart.js/auto';

export default {
  name: 'RecommendationsDashboard',
  components: {
    RecommendationsWidget,
  },
  data() {
    return {
      performance: null,
      loadingPerformance: false,
      recommendationStats: null,
      topPerformingRecommendations: [],
      loading: false,
      loadingGeneral: false,
      loadingTrending: false,
      loadingPersonalized: false,
      activeTab: 'overview',
      analytics: null,
      generalRecommendations: [],
      trendingProducts: [],
      personalizedRecommendations: [],
      user: {
        id: 1,
        name: 'أحمد محمد',
      },
      categoryPerformance: [
        { name: 'جدران', count: 145, percentage: 35 },
        { name: 'أبواب', count: 98, percentage: 24 },
        { name: 'سيارات', count: 87, percentage: 21 },
        { name: 'مطابخ', count: 42, percentage: 10 },
        { name: 'أثاث', count: 38, percentage: 9 },
      ],
      charts: {
        performance: null,
      },
    };
  },
  mounted() {
    this.loadData();
    this.loadRecommendationStats();
  },
  methods: {
    formatCurrency(value) {
      return CurrencyService.formatAmount(value || 0);
    },

    async loadData() {
      await this.loadAnalytics();
      await this.loadGeneralRecommendations();
      await this.loadTrendingProducts();
      await this.loadPersonalizedRecommendations();
    },

    async loadAnalytics() {
      try {
        this.analytics = await RecommendationService.getRecommendationsAnalytics();
        this.$nextTick(() => {
          this.initCharts();
        });
      } catch (error) {
        console.error('خطأ في تحميل التحليلات:', error);
      }
    },

    async loadGeneralRecommendations() {
      this.loadingGeneral = true;
      try {
        this.generalRecommendations = await RecommendationService.getTopSellingProducts(20);
      } catch (error) {
        console.error('خطأ في تحميل التوصيات العامة:', error);
      } finally {
        this.loadingGeneral = false;
      }
    },

    async loadTrendingProducts() {
      this.loadingTrending = true;
      try {
        this.trendingProducts = await RecommendationService.getTrendingProducts(20);
      } catch (error) {
        console.error('خطأ في تحميل المنتجات الرائجة:', error);
      } finally {
        this.loadingTrending = false;
      }
    },

    async loadPersonalizedRecommendations() {
      this.loadingPersonalized = true;
      try {
        this.personalizedRecommendations =
          await RecommendationService.getPersonalizedRecommendations(this.user.id, 15);
      } catch (error) {
        console.error('خطأ في تحميل التوصيات المخصصة:', error);
      } finally {
        this.loadingPersonalized = false;
      }
    },

    async refreshModels() {
      this.loading = true;
      try {
        await RecommendationService.refreshAll();
        await this.loadData();
        this.$toast?.success('تم تحديث نماذج التوصيات بنجاح');
      } catch (error) {
        console.error('خطأ في تحديث النماذج:', error);
        this.$toast?.error('فشل تحديث النماذج');
      } finally {
        this.loading = false;
      }
    },

    async loadPerformance() {
      this.loadingPerformance = true;
      try {
        this.performance = await RecommendationService.getRecommendationPerformance(30);
      } catch (error) {
        console.error('خطأ في تحميل أداء التوصيات:', error);
      } finally {
        this.loadingPerformance = false;
      }
    },

    getTypeName(type) {
      const names = {
        collaborative: 'توصيات تعاونية',
        seasonal: 'موسمية',
        event: 'مناسبات',
        similar: 'منتجات مشابهة',
        together: 'تُشترى معاً',
        lowStock: 'مخزون محدود',
        general: 'عامة',
      };
      return names[type] || type;
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

    initCharts() {
      // رسم بياني لأداء التوصيات
      const perfCtx = this.$refs.performanceChart?.getContext('2d');
      if (perfCtx) {
        if (this.charts.performance) this.charts.performance.destroy();

        this.charts.performance = new Chart(perfCtx, {
          type: 'line',
          data: {
            labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
            datasets: [
              {
                label: 'نسبة النقر',
                data: [32, 35, 38, 40, 42, 45],
                borderColor: '#2196f3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.4,
                fill: true,
              },
              {
                label: 'نسبة التحويل',
                data: [8, 9, 10, 11, 12, 13],
                borderColor: '#4caf50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                tension: 0.4,
                fill: true,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: true,
                position: 'bottom',
                labels: { color: '#fff' },
              },
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: {
                  color: '#fff',
                  callback: (v) => v + '%',
                },
              },
              x: {
                grid: { display: false },
                ticks: { color: '#fff' },
              },
            },
          },
        });
      }
    },
    async loadRecommendationStats() {
      try {
        const performance = await RecommendationService.getRecommendationPerformance(30);

        // حساب الإحصائيات
        this.recommendationStats = {
          total: performance.total.clicks,
          ctr: (performance.total.ctr * 100).toFixed(1),
          conversionRate: (
            (performance.total.conversions / performance.total.clicks) *
            100
          ).toFixed(1),
          revenue: performance.total.conversions * 850, // متوسط قيمة الطلب
        };

        // أفضل التوصيات
        this.topPerformingRecommendations = Object.entries(performance.byType)
          .map(([type, data]) => ({
            id: type,
            productName: this.getTypeName(type),
            clicks: data.clicks,
            conversions: data.conversions,
          }))
          .sort((a, b) => b.clicks - a.clicks)
          .slice(0, 5);
      } catch (error) {
        console.error('خطأ في تحميل إحصائيات التوصيات:', error);
      }
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.recommendations-dashboard {
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

.header-actions {
  display: flex;
  gap: 12px;
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

.stats-cards {
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

.stat-content {
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.stat-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

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

.category-performance {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.category-performance h3 {
  color: white;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-performance h3 i {
  color: var(--gold-1);
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.category-name {
  width: 80px;
  color: white;
  font-weight: 600;
}

.category-bar {
  flex: 1;
  height: 30px;
  background: var(--bg-primary);
  border-radius: 15px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f5e7b2);
  border-radius: 15px;
  transition: width 0.5s;
}

.category-revenue {
  width: 100px;
  color: var(--gold-1);
  font-weight: 600;
  text-align: left;
}

.recommendations-section {
  margin-bottom: 30px;
}

.recommendations-section h3 {
  color: white;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recommendations-section h3 i {
  color: var(--gold-1);
}

.personalized-section {
  margin-top: 30px;
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.personalized-section h2 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.personalized-section h2 i {
  color: var(--gold-1);
}

.advanced-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 25px;
}

.analytics-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.analytics-card h4 {
  color: white;
  font-size: 1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.analytics-card h4 i {
  color: var(--gold-1);
}

.category-stat {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.category-stat span {
  color: white;
  font-size: 0.9rem;
  min-width: 80px;
}

.progress-bar {
  flex: 1;
  height: 20px;
  background: var(--bg-primary);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f5e7b2);
  border-radius: 10px;
  transition: width 0.5s;
}

.patterns-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.pattern-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-size: 0.95rem;
  padding: 10px;
  background: var(--bg-primary);
  border-radius: 12px;
}

.pattern-item i {
  color: var(--gold-1);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .tabs-container {
    flex-wrap: wrap;
  }

  .tab-btn {
    flex: auto;
    min-width: 120px;
  }

  .category-item {
    flex-wrap: wrap;
  }

  .advanced-grid {
    grid-template-columns: 1fr;
  }
}

.personalized-section {
  margin-top: 30px;
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.personalized-section h2 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.personalized-section h2 i {
  color: var(--gold-1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-item {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  text-align: center;
}

.stat-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
}

.top-recommendations h3 {
  color: white;
  font-size: 1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-recommendations h3 i {
  color: var(--gold-1);
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rec-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  background: var(--bg-primary);
  border-radius: 12px;
}

.rec-name {
  flex: 2;
  color: white;
  font-weight: 600;
}

.rec-clicks {
  flex: 1;
  color: var(--gold-1);
  font-size: 0.9rem;
}

.rec-conversions {
  flex: 1;
  color: #4caf50;
  font-size: 0.9rem;
}
</style>
