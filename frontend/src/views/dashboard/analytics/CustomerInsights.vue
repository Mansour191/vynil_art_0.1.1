// @\views\dashboard\CustomerInsights.vue

<template>
  <div class="customer-insights">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-users header-icon"></i>
          تحليلات سلوك العملاء
        </h1>
        <p class="header-subtitle">تحليل متقدم لسلوك العملاء وتقسيمهم وتوقع قيمتهم</p>
      </div>

      <div class="header-actions">
        <button class="btn-refresh" @click="refreshAll" :disabled="loading">
          <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
          <span>{{ loading ? 'جاري التحديث...' : 'تحديث البيانات' }}</span>
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
        :class="{ active: activeTab === 'segments' }"
        @click="
          loadSegments();
          activeTab = 'segments';
        "
      >
        <i class="fa-solid fa-layer-group"></i>
        تقسيم العملاء
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'churn' }"
        @click="
          loadChurn();
          activeTab = 'churn';
        "
      >
        <i class="fa-solid fa-exclamation-triangle"></i>
        خطر التوقف
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'value' }"
        @click="
          loadValue();
          activeTab = 'value';
        "
      >
        <i class="fa-solid fa-coins"></i>
        القيمة الدائمة
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'behavior' }"
        @click="
          loadBehavior();
          activeTab = 'behavior';
        "
      >
        <i class="fa-solid fa-chart-line"></i>
        تحليل السلوك
      </button>
    </div>

    <!-- محتوى التبويبات -->
    <div class="tab-content">
      <!-- ===== تبويب النظرة العامة ===== -->
      <div v-if="activeTab === 'overview'" class="overview-tab">
        <!-- بطاقات إحصائيات سريعة -->
        <div class="stats-grid" v-if="analytics">
          <div class="stat-card">
            <div class="stat-icon blue">
              <i class="fa-solid fa-users"></i>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ analytics.total }}</span>
              <span class="stat-label">إجمالي العملاء</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon green">
              <i class="fa-solid fa-user-check"></i>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ analytics.active }}</span>
              <span class="stat-label">نشط (آخر 30 يوم)</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon orange">
              <i class="fa-solid fa-user-plus"></i>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ analytics.new }}</span>
              <span class="stat-label">عملاء جدد</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon red">
              <i class="fa-solid fa-user-slash"></i>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ analytics.churned }}</span>
              <span class="stat-label">متوقفون</span>
            </div>
          </div>
        </div>

        <!-- توزيع العملاء -->
        <div class="chart-card" v-if="analytics">
          <h3><i class="fa-solid fa-chart-pie"></i> توزيع العملاء حسب القيمة</h3>
          <div class="distribution-grid">
            <div
              v-for="(value, segment) in analytics.segments"
              :key="segment"
              class="distribution-item"
            >
              <span class="segment-name">{{ getSegmentName(segment) }}</span>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: value.percentage + '%' }"></div>
              </div>
              <span class="segment-count">{{ value.count }} عميل</span>
            </div>
          </div>
        </div>

        <!-- إحصائيات سريعة -->
        <div class="stats-row" v-if="analytics">
          <div class="stat-box">
            <span class="label">متوسط قيمة الطلب</span>
            <span class="value">{{ formatCurrency(analytics.revenue.averageOrderValue) }}</span>
          </div>
          <div class="stat-box">
            <span class="label">معدل عودة العملاء</span>
            <span class="value">{{ analytics.retention.returningRate.toFixed(1) }}%</span>
          </div>
          <div class="stat-box">
            <span class="label">متوسط الطلبات لكل عميل</span>
            <span class="value">{{ analytics.retention.averageOrdersPerCustomer.toFixed(1) }}</span>
          </div>
        </div>

        <!-- توصيات ذكية -->
        <div class="recommendations-card" v-if="marketingRecs">
          <h3><i class="fa-solid fa-lightbulb"></i> توصيات تسويقية ذكية</h3>
          <div class="rec-list">
            <div
              v-for="rec in marketingRecs"
              :key="rec.title"
              class="rec-item"
              :class="rec.priority"
            >
              <div class="rec-header">
                <span class="rec-title">{{ rec.title }}</span>
                <span class="rec-badge">{{ rec.priority === 'urgent' ? 'عاجل' : 'مهم' }}</span>
              </div>
              <p class="rec-message">{{ rec.message }}</p>
              <div class="rec-actions">
                <span v-for="action in rec.actions" :key="action" class="rec-action">
                  <i class="fa-solid fa-check-circle"></i> {{ action }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب تقسيم العملاء ===== -->
      <div v-if="activeTab === 'segments'" class="segments-tab">
        <div v-if="loadingSegments" class="loading-state">
          <div class="spinner"></div>
          <p>جاري تحميل بيانات العملاء...</p>
        </div>

        <div v-else-if="segments" class="segments-container">
          <!-- شرائح حسب القيمة -->
          <div class="segment-section">
            <h3><i class="fa-solid fa-crown"></i> شرائح العملاء حسب القيمة</h3>
            <div class="segment-cards">
              <div
                v-for="(data, segment) in segments.stats"
                :key="segment"
                class="segment-card"
                :class="segment"
              >
                <div class="segment-icon">
                  <i :class="getSegmentIcon(segment)"></i>
                </div>
                <div class="segment-info">
                  <h4>{{ getSegmentName(segment) }}</h4>
                  <div class="segment-stats">
                    <div class="stat">
                      <span class="label">عدد العملاء</span>
                      <span class="value">{{ data.count }}</span>
                    </div>
                    <div class="stat">
                      <span class="label">نسبة من الإجمالي</span>
                      <span class="value">{{ data.percentage.toFixed(1) }}%</span>
                    </div>
                    <div class="stat">
                      <span class="label">إجمالي الإيرادات</span>
                      <span class="value">{{ formatCurrency(data.revenue) }}</span>
                    </div>
                    <div class="stat">
                      <span class="label">متوسط قيمة الطلب</span>
                      <span class="value">{{ formatCurrency(data.avgOrderValue) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- شرائح حسب التفاعل -->
          <div class="segment-section" v-if="engagementSegments">
            <h3><i class="fa-solid fa-chart-line"></i> شرائح حسب التفاعل</h3>
            <div class="mini-cards">
              <div
                v-for="(data, segment) in engagementSegments.stats"
                :key="segment"
                class="mini-card"
                :class="segment"
              >
                <span class="mini-title">{{ getEngagementName(segment) }}</span>
                <span class="mini-count">{{ data.count }}</span>
                <span class="mini-percent">{{ data.percentage.toFixed(1) }}%</span>
              </div>
            </div>
          </div>

          <!-- شرائح حسب دورة الحياة -->
          <div class="segment-section" v-if="lifecycleSegments">
            <h3><i class="fa-solid fa-life-ring"></i> شرائح حسب دورة الحياة</h3>
            <div class="lifecycle-grid">
              <div
                v-for="(data, segment) in lifecycleSegments.stats"
                :key="segment"
                class="lifecycle-item"
              >
                <span class="lifecycle-name">{{ getLifecycleName(segment) }}</span>
                <span class="lifecycle-value">{{ data.count }} عميل</span>
                <span class="lifecycle-percent">{{ data.percentage.toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب خطر التوقف ===== -->
      <div v-if="activeTab === 'churn'" class="churn-tab">
        <div v-if="loadingChurn" class="loading-state">
          <div class="spinner"></div>
          <p>جاري تحليل خطر التوقف...</p>
        </div>

        <div v-else-if="churnStats" class="churn-container">
          <!-- بطاقات خطر التوقف -->
          <div class="risk-cards">
            <div class="risk-card high">
              <div class="risk-icon">
                <i class="fa-solid fa-exclamation-triangle"></i>
              </div>
              <div class="risk-content">
                <span class="risk-label">خطر مرتفع</span>
                <span class="risk-value">{{ churnStats.highRisk.count }}</span>
                <span class="risk-percent">{{ churnStats.highRisk.percentage }}</span>
              </div>
            </div>

            <div class="risk-card medium">
              <div class="risk-icon">
                <i class="fa-solid fa-exclamation-circle"></i>
              </div>
              <div class="risk-content">
                <span class="risk-label">خطر متوسط</span>
                <span class="risk-value">{{ churnStats.mediumRisk.count }}</span>
                <span class="risk-percent">{{ churnStats.mediumRisk.percentage }}</span>
              </div>
            </div>

            <div class="risk-card low">
              <div class="risk-icon">
                <i class="fa-solid fa-info-circle"></i>
              </div>
              <div class="risk-content">
                <span class="risk-label">خطر منخفض</span>
                <span class="risk-value">{{ churnStats.lowRisk.count }}</span>
                <span class="risk-percent">{{ churnStats.lowRisk.percentage }}</span>
              </div>
            </div>

            <div class="risk-card safe">
              <div class="risk-icon">
                <i class="fa-solid fa-check-circle"></i>
              </div>
              <div class="risk-content">
                <span class="risk-label">آمن</span>
                <span class="risk-value">{{ churnStats.safe.count }}</span>
                <span class="risk-percent">{{ churnStats.safe.percentage }}</span>
              </div>
            </div>
          </div>

          <!-- إحصائيات الخطر -->
          <div class="churn-stats-row">
            <div class="stat-box warning">
              <span class="label">معدل التوقف</span>
              <span class="value">{{ churnStats.churnRate }}</span>
            </div>
            <div class="stat-box danger">
              <span class="label">خسارة محتملة</span>
              <span class="value">{{ formatCurrency(churnStats.highRisk.potentialLoss) }}</span>
            </div>
          </div>

          <!-- قائمة العملاء المعرضين للخطر -->
          <div class="risk-list" v-if="churnPredictions && churnPredictions.highRisk">
            <h3><i class="fa-solid fa-exclamation-triangle"></i> عملاء خطر التوقف مرتفع</h3>
            <div class="customer-cards">
              <div
                v-for="customer in churnPredictions.highRisk.slice(0, 5)"
                :key="customer.id"
                class="customer-card"
              >
                <div class="customer-info">
                  <h4>{{ customer.name }}</h4>
                  <div class="customer-details">
                    <span>آخر طلب: {{ formatDate(customer.lastOrderDate) }}</span>
                    <span>قيمة المشتريات: {{ formatCurrency(customer.totalSpent) }}</span>
                    <span
                      >احتمالية التوقف: {{ (customer.churnProbability * 100).toFixed(0) }}%</span
                    >
                  </div>
                </div>
                <div class="churn-bar">
                  <div
                    class="churn-fill"
                    :style="{ width: customer.churnProbability * 100 + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- توصيات للاحتفاظ -->
          <div class="retention-recs" v-if="retentionRecs">
            <h3><i class="fa-solid fa-life-ring"></i> توصيات للاحتفاظ بالعملاء</h3>
            <div class="recs-list">
              <div v-for="rec in retentionRecs" :key="rec.title" class="rec-card">
                <div class="rec-level" :class="rec.level"></div>
                <div class="rec-content">
                  <h4>{{ rec.title }}</h4>
                  <p>{{ rec.count }} عميل - {{ rec.percentage }}</p>
                  <div class="rec-actions">
                    <span v-for="action in rec.actions" :key="action.type" class="action-tag">
                      {{ action.description }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب القيمة الدائمة ===== -->
      <div v-if="activeTab === 'value'" class="value-tab">
        <div v-if="loadingValue" class="loading-state">
          <div class="spinner"></div>
          <p>جاري حساب القيمة الدائمة للعملاء...</p>
        </div>

        <div v-else-if="valueStats" class="value-container">
          <!-- بطاقات القيمة -->
          <div class="value-cards">
            <div class="value-card total">
              <span class="label">القيمة الدائمة الإجمالية</span>
              <span class="value">{{ formatCurrency(valueStats.totalLTV) }}</span>
            </div>
            <div class="value-card average">
              <span class="label">متوسط القيمة لكل عميل</span>
              <span class="value">{{ formatCurrency(valueStats.averageLTV) }}</span>
            </div>
            <div class="value-card growth">
              <span class="label">نمو محتمل</span>
              <span class="value">{{ formatCurrency(valueStats.potentialGrowth) }}</span>
            </div>
            <div class="value-card atrisk">
              <span class="label">قيمة معرضة للخطر</span>
              <span class="value">{{ formatCurrency(valueStats.atRiskValue) }}</span>
            </div>
          </div>

          <!-- توزيع القيمة -->
          <div class="distribution-chart">
            <h3><i class="fa-solid fa-chart-bar"></i> توزيع العملاء حسب القيمة</h3>
            <div class="distribution-bars">
              <div class="dist-item">
                <span class="dist-label">أقل من 1000</span>
                <div class="dist-bar">
                  <div
                    class="dist-fill"
                    :style="{
                      width: (valueStats.distribution.under1000 / analytics.total) * 100 + '%',
                    }"
                  ></div>
                </div>
                <span class="dist-value">{{ valueStats.distribution.under1000 }}</span>
              </div>
              <div class="dist-item">
                <span class="dist-label">1000 - 5000</span>
                <div class="dist-bar">
                  <div
                    class="dist-fill"
                    :style="{
                      width: (valueStats.distribution.under5000 / analytics.total) * 100 + '%',
                    }"
                  ></div>
                </div>
                <span class="dist-value">{{ valueStats.distribution.under5000 }}</span>
              </div>
              <div class="dist-item">
                <span class="dist-label">5000 - 10000</span>
                <div class="dist-bar">
                  <div
                    class="dist-fill"
                    :style="{
                      width: (valueStats.distribution.under10000 / analytics.total) * 100 + '%',
                    }"
                  ></div>
                </div>
                <span class="dist-value">{{ valueStats.distribution.under10000 }}</span>
              </div>
              <div class="dist-item">
                <span class="dist-label">10000 - 50000</span>
                <div class="dist-bar">
                  <div
                    class="dist-fill"
                    :style="{
                      width: (valueStats.distribution.under50000 / analytics.total) * 100 + '%',
                    }"
                  ></div>
                </div>
                <span class="dist-value">{{ valueStats.distribution.under50000 }}</span>
              </div>
              <div class="dist-item">
                <span class="dist-label">أكثر من 50000</span>
                <div class="dist-bar">
                  <div
                    class="dist-fill"
                    :style="{
                      width: (valueStats.distribution.over50000 / analytics.total) * 100 + '%',
                    }"
                  ></div>
                </div>
                <span class="dist-value">{{ valueStats.distribution.over50000 }}</span>
              </div>
            </div>
          </div>

          <!-- أفضل العملاء -->
          <div class="top-customers" v-if="valueStats.topCustomer">
            <h3><i class="fa-solid fa-crown"></i> أفضل عميل</h3>
            <div class="top-card">
              <div class="top-info">
                <h4>{{ valueStats.topCustomer.customerName }}</h4>
                <p>القيمة التاريخية: {{ formatCurrency(valueStats.topCustomer.historical) }}</p>
                <p>
                  متوقع خلال 3 سنوات: {{ formatCurrency(valueStats.topCustomer.predicted3Years) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== تبويب تحليل السلوك ===== -->
      <div v-if="activeTab === 'behavior'" class="behavior-tab">
        <div v-if="loadingBehavior" class="loading-state">
          <div class="spinner"></div>
          <p>جاري تحليل سلوك العملاء...</p>
        </div>

        <div v-else-if="behaviorStats" class="behavior-container">
          <!-- إحصائيات السلوك -->
          <div class="behavior-stats">
            <div class="stat-item">
              <span class="stat-big">{{ behaviorStats.uniqueVisitors }}</span>
              <span class="stat-small">زوار فريدون</span>
            </div>
            <div class="stat-item">
              <span class="stat-big">{{ behaviorStats.totalViews }}</span>
              <span class="stat-small">إجمالي المشاهدات</span>
            </div>
            <div class="stat-item">
              <span class="stat-big">{{ behaviorStats.activeCarts }}</span>
              <span class="stat-small">سلال نشطة</span>
            </div>
            <div class="stat-item">
              <span class="stat-big">{{ behaviorStats.cartAbandonmentRate.toFixed(1) }}%</span>
              <span class="stat-small">نسبة السلال المتروكة</span>
            </div>
          </div>

          <!-- تحليل الساعات -->
          <div class="time-analysis">
            <h3><i class="fa-solid fa-clock"></i> أوقات الذروة</h3>
            <p>قيد التطوير - سيتم إضافة رسم بياني لتحليل أوقات التصفح</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CustomerAnalyticsService from '@/integration/ai/customers/CustomerAnalyticsService';
import CustomerSegmentation from '@/integration/ai/customers/CustomerSegmentation';
import ChurnPredictor from '@/integration/ai/customers/ChurnPredictor';
import CustomerValue from '@/integration/ai/customers/CustomerValue';
import BehaviorTracker from '@/integration/ai/customers/BehaviorTracker';
import CurrencyService from '@/integration/services/CurrencyService';

export default {
  name: 'CustomerInsights',
  data() {
    return {
      loading: false,
      activeTab: 'overview',

      // بيانات
      analytics: null,
      segments: null,
      engagementSegments: null,
      lifecycleSegments: null,
      churnStats: null,
      churnPredictions: null,
      retentionRecs: null,
      valueStats: null,
      behaviorStats: null,
      marketingRecs: null,

      // حالات التحميل
      loadingSegments: false,
      loadingChurn: false,
      loadingValue: false,
      loadingBehavior: false,
    };
  },
  mounted() {
    this.loadOverview();
  },
  methods: {
    formatCurrency(value) {
      return CurrencyService.formatAmount(value || 0);
    },

    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('ar-SA');
    },

    async loadOverview() {
      this.loading = true;
      try {
        this.analytics = await CustomerAnalyticsService.getCustomerAnalytics();
        this.marketingRecs = await CustomerSegmentation.getMarketingRecommendations();
      } catch (error) {
        console.error('خطأ في تحميل النظرة العامة:', error);
      } finally {
        this.loading = false;
      }
    },

    async loadSegments() {
      this.loadingSegments = true;
      try {
        const allSegments = await CustomerSegmentation.getAllSegments();
        this.segments = allSegments.byValue;
        this.engagementSegments = allSegments.byEngagement;
        this.lifecycleSegments = allSegments.byLifecycle;
      } catch (error) {
        console.error('خطأ في تحميل تقسيم العملاء:', error);
      } finally {
        this.loadingSegments = false;
      }
    },

    async loadChurn() {
      this.loadingChurn = true;
      try {
        this.churnStats = await ChurnPredictor.getChurnStats();
        this.churnPredictions = await ChurnPredictor.predictAllCustomers();
        this.retentionRecs = await ChurnPredictor.getRetentionRecommendations();
      } catch (error) {
        console.error('خطأ في تحميل تحليل التوقف:', error);
      } finally {
        this.loadingChurn = false;
      }
    },

    async loadValue() {
      this.loadingValue = true;
      try {
        this.valueStats = await CustomerValue.getValueStats();
      } catch (error) {
        console.error('خطأ في تحميل القيمة الدائمة:', error);
      } finally {
        this.loadingValue = false;
      }
    },

    async loadBehavior() {
      this.loadingBehavior = true;
      try {
        this.behaviorStats = await BehaviorTracker.getBehaviorStats();
      } catch (error) {
        console.error('خطأ في تحميل تحليل السلوك:', error);
      } finally {
        this.loadingBehavior = false;
      }
    },

    async refreshAll() {
      this.loading = true;
      try {
        await CustomerAnalyticsService.refreshAll();
        await CustomerSegmentation.getAllSegments();
        await ChurnPredictor.refreshAll();
        await CustomerValue.refreshAll();

        await this.loadOverview();
        if (this.activeTab === 'segments') await this.loadSegments();
        if (this.activeTab === 'churn') await this.loadChurn();
        if (this.activeTab === 'value') await this.loadValue();
        if (this.activeTab === 'behavior') await this.loadBehavior();

        this.$toast?.success('تم تحديث جميع البيانات بنجاح');
      } catch (error) {
        console.error('خطأ في تحديث البيانات:', error);
        this.$toast?.error('فشل تحديث البيانات');
      } finally {
        this.loading = false;
      }
    },

    getSegmentName(segment) {
      const names = {
        vip: 'عملاء VIP',
        regular: 'عملاء منتظمون',
        occasional: 'عملاء مناسبيون',
        new: 'عملاء جدد',
        churned: 'عملاء متوقفون',
      };
      return names[segment] || segment;
    },

    getSegmentIcon(segment) {
      const icons = {
        vip: 'fa-solid fa-crown',
        regular: 'fa-solid fa-user-check',
        occasional: 'fa-solid fa-user-clock',
        new: 'fa-solid fa-user-plus',
        churned: 'fa-solid fa-user-slash',
      };
      return icons[segment] || 'fa-solid fa-user';
    },

    getEngagementName(segment) {
      const names = {
        highlyEngaged: 'متفاعلون جداً',
        engaged: 'متفاعلون',
        atRisk: 'معرضون للخطر',
        lost: 'مفقودون',
        new: 'جدد',
      };
      return names[segment] || segment;
    },

    getLifecycleName(segment) {
      const names = {
        acquisition: 'اكتساب',
        growth: 'نمو',
        maturity: 'نضج',
        decline: 'تراجع',
        reactivation: 'إعادة تنشيط',
      };
      return names[segment] || segment;
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.customer-insights {
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

/* ===== التبويبات ===== */
.tabs-container {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 10px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
  flex-wrap: wrap;
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
  min-width: 120px;
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

/* ===== بطاقات الإحصائيات ===== */
.stats-grid {
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

.stat-icon.blue {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.stat-icon.green {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.stat-icon.orange {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.stat-icon.red {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
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

/* ===== توزيع العملاء ===== */
.chart-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.chart-card h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-card h3 i {
  color: var(--gold-1);
}

.distribution-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.segment-name {
  width: 120px;
  color: white;
  font-weight: 600;
}

.progress-bar {
  flex: 1;
  height: 30px;
  background: var(--bg-primary);
  border-radius: 15px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f5e7b2);
  border-radius: 15px;
  transition: width 0.5s;
}

.segment-count {
  width: 80px;
  color: var(--gold-1);
  font-weight: 600;
  text-align: left;
}

/* ===== صف الإحصائيات ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.stat-box {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 15px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.stat-box .label {
  display: block;
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 8px;
}

.stat-box .value {
  display: block;
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
}

.stat-box.warning .value {
  color: #ff9800;
}

.stat-box.danger .value {
  color: #f44336;
}

/* ===== توصيات ذكية ===== */
.recommendations-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.recommendations-card h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recommendations-card h3 i {
  color: var(--gold-1);
}

.rec-list {
  display: grid;
  gap: 15px;
}

.rec-item {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  border-right: 4px solid;
}

.rec-item.urgent {
  border-right-color: #f44336;
}

.rec-item.high {
  border-right-color: #ff9800;
}

.rec-item.medium {
  border-right-color: #2196f3;
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.rec-title {
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.rec-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.rec-message {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.rec-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.rec-action {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-1);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* ===== شرائح العملاء ===== */
.segment-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.segment-section h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.segment-section h3 i {
  color: var(--gold-1);
}

.segment-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.segment-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  gap: 15px;
  border: 1px solid var(--border-light);
  transition: all 0.3s;
}

.segment-card:hover {
  transform: translateY(-3px);
  border-color: var(--gold-1);
}

.segment-card.vip .segment-icon {
  color: #d4af37;
}

.segment-card.regular .segment-icon {
  color: #2196f3;
}

.segment-card.occasional .segment-icon {
  color: #ff9800;
}

.segment-card.new .segment-icon {
  color: #4caf50;
}

.segment-card.churned .segment-icon {
  color: #f44336;
}

.segment-icon {
  font-size: 2rem;
  width: 50px;
  text-align: center;
}

.segment-info {
  flex: 1;
}

.segment-info h4 {
  color: white;
  font-size: 1rem;
  margin-bottom: 15px;
}

.segment-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.segment-stats .stat .label {
  display: block;
  color: var(--text-dim);
  font-size: 0.7rem;
  margin-bottom: 3px;
}

.segment-stats .stat .value {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.mini-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.mini-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 15px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.mini-card.highlyEngaged {
  border-top: 4px solid #4caf50;
}

.mini-card.engaged {
  border-top: 4px solid #2196f3;
}

.mini-card.atRisk {
  border-top: 4px solid #ff9800;
}

.mini-card.lost {
  border-top: 4px solid #f44336;
}

.mini-card.new {
  border-top: 4px solid #d4af37;
}

.mini-title {
  display: block;
  color: white;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.mini-count {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.mini-percent {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.lifecycle-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.lifecycle-item {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
}

.lifecycle-name {
  display: block;
  color: white;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.lifecycle-value {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--gold-1);
  margin-bottom: 3px;
}

.lifecycle-percent {
  color: var(--text-dim);
  font-size: 0.8rem;
}

/* ===== خطر التوقف ===== */
.risk-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.risk-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid var(--border-light);
}

.risk-card.high .risk-icon {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.risk-card.medium .risk-icon {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.risk-card.low .risk-icon {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.risk-card.safe .risk-icon {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.risk-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.risk-content {
  flex: 1;
}

.risk-label {
  display: block;
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 5px;
}

.risk-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 3px;
}

.risk-percent {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.churn-stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.risk-list {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.risk-list h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.risk-list h3 i {
  color: #f44336;
}

.customer-cards {
  display: grid;
  gap: 15px;
}

.customer-card {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid var(--border-light);
}

.customer-info h4 {
  color: white;
  font-size: 0.95rem;
  margin-bottom: 8px;
}

.customer-details {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 10px;
}

.churn-bar {
  height: 6px;
  background: rgba(244, 67, 54, 0.2);
  border-radius: 3px;
  overflow: hidden;
}

.churn-fill {
  height: 100%;
  background: #f44336;
  border-radius: 3px;
  transition: width 0.5s;
}

.retention-recs {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.retention-recs h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.recs-list {
  display: grid;
  gap: 15px;
}

.rec-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  gap: 15px;
  border: 1px solid var(--border-light);
}

.rec-level {
  width: 4px;
  border-radius: 2px;
}

.rec-level.high {
  background: #f44336;
}

.rec-level.medium {
  background: #ff9800;
}

.rec-level.low {
  background: #2196f3;
}

.rec-content {
  flex: 1;
}

.rec-content h4 {
  color: white;
  font-size: 1rem;
  margin-bottom: 5px;
}

.rec-content p {
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.rec-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action-tag {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-1);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
}

/* ===== القيمة الدائمة ===== */
.value-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.value-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.value-card.total .value {
  color: #d4af37;
}

.value-card.average .value {
  color: #2196f3;
}

.value-card.growth .value {
  color: #4caf50;
}

.value-card.atrisk .value {
  color: #f44336;
}

.value-card .label {
  display: block;
  color: var(--text-dim);
  font-size: 0.85rem;
  margin-bottom: 10px;
}

.value-card .value {
  display: block;
  font-size: 1.8rem;
  font-weight: 700;
}

.distribution-chart {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.distribution-chart h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.distribution-bars {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dist-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dist-label {
  width: 100px;
  color: var(--text-dim);
  font-size: 0.85rem;
}

.dist-bar {
  flex: 1;
  height: 20px;
  background: var(--bg-primary);
  border-radius: 10px;
  overflow: hidden;
}

.dist-fill {
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #f5e7b2);
  border-radius: 10px;
  transition: width 0.5s;
}

.dist-value {
  width: 50px;
  color: white;
  font-weight: 600;
  text-align: left;
}

.top-customers {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.top-customers h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.top-customers h3 i {
  color: #d4af37;
}

.top-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--border-light);
}

.top-card h4 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.top-card p {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 5px;
}

/* ===== تحليل السلوك ===== */
.behavior-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.stat-item {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-light);
}

.stat-big {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.stat-small {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.time-analysis {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.time-analysis h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-analysis p {
  color: var(--text-dim);
  font-size: 0.9rem;
  text-align: center;
  padding: 20px;
}

/* ===== حالة التحميل ===== */
.loading-state {
  text-align: center;
  padding: 50px;
  color: var(--text-dim);
}

.spinner {
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

/* ===== استجابة للشاشات الصغيرة ===== */
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
    min-width: 100px;
  }

  .segment-card {
    flex-direction: column;
    text-align: center;
  }

  .segment-stats {
    grid-template-columns: 1fr;
  }

  .distribution-item {
    flex-wrap: wrap;
  }

  .rec-card {
    flex-direction: column;
  }
}
</style>
