<template>
  <div class="alerts-center">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-bell header-icon"></i>
          مركز التنبيهات
        </h1>
        <p class="header-subtitle">إدارة ومتابعة جميع التنبيهات والإشعارات الذكية</p>
      </div>

      <div class="header-actions">
        <button class="btn-refresh" @click="loadAlerts" :disabled="loading">
          <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
          <span>{{ loading ? 'جاري التحديث...' : 'تحديث' }}</span>
        </button>
        <button class="btn-mark-read" @click="markAllAsRead" v-if="unreadCount > 0">
          <i class="fa-solid fa-check-double"></i>
          <span>تحديد الكل كمقروء</span>
        </button>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="stats-cards" v-if="alerts.length">
      <div class="stat-card critical">
        <div class="stat-icon">
          <i class="fa-solid fa-exclamation-triangle"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ priorityCounts.critical }}</span>
          <span class="stat-label">حرج</span>
        </div>
      </div>

      <div class="stat-card high">
        <div class="stat-icon">
          <i class="fa-solid fa-exclamation-circle"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ priorityCounts.high }}</span>
          <span class="stat-label">عالي</span>
        </div>
      </div>

      <div class="stat-card medium">
        <div class="stat-icon">
          <i class="fa-solid fa-exclamation"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ priorityCounts.medium }}</span>
          <span class="stat-label">متوسط</span>
        </div>
      </div>

      <div class="stat-card low">
        <div class="stat-icon">
          <i class="fa-solid fa-info-circle"></i>
        </div>
        <div class="stat-content">
          <span class="stat-value">{{ priorityCounts.low }}</span>
          <span class="stat-label">منخفض</span>
        </div>
      </div>
    </div>

    <!-- تبويبات التصفية -->
    <div class="filters-tabs">
      <button
        class="filter-tab"
        :class="{ active: currentFilter === 'all' }"
        @click="currentFilter = 'all'"
      >
        الكل
        <span class="badge">{{ alerts.length }}</span>
      </button>
      <button
        class="filter-tab"
        :class="{ active: currentFilter === 'unread' }"
        @click="currentFilter = 'unread'"
      >
        غير مقروء
        <span class="badge">{{ unreadCount }}</span>
      </button>
      <button
        class="filter-tab"
        :class="{ active: currentFilter === 'critical' }"
        @click="currentFilter = 'critical'"
      >
        حرج
        <span class="badge critical">{{ priorityCounts.critical }}</span>
      </button>
    </div>

    <!-- تصنيفات التنبيهات -->
    <div class="category-tabs">
      <button
        v-for="cat in categories"
        :key="cat.value"
        class="category-tab"
        :class="{ active: currentCategory === cat.value }"
        @click="currentCategory = cat.value"
      >
        <i :class="cat.icon"></i>
        <span>{{ cat.label }}</span>
        <span class="badge" :style="{ background: cat.color }">{{
          categoryCounts[cat.value] || 0
        }}</span>
      </button>
    </div>

    <!-- قائمة التنبيهات -->
    <div class="alerts-list" v-if="filteredAlerts.length > 0">
      <transition-group name="alert" tag="div">
        <div
          v-for="alert in filteredAlerts"
          :key="alert.id"
          class="alert-item"
          :class="[`severity-${alert.severity || 'low'}`, { 'alert-read': alert.read }]"
        >
          <div class="alert-icon" :style="{ background: getCategoryColor(alert.category) + '20' }">
            <i
              :class="alert.icon || getDefaultIcon(alert)"
              :style="{ color: getCategoryColor(alert.category) }"
            ></i>
          </div>

          <div class="alert-content">
            <div class="alert-header">
              <h3 class="alert-title">{{ alert.title }}</h3>
              <span class="alert-time">{{ formatTime(alert.timestamp) }}</span>
            </div>

            <p class="alert-message">{{ alert.message }}</p>

            <div class="alert-meta">
              <span
                class="alert-category"
                :style="{
                  background: getCategoryColor(alert.category) + '20',
                  color: getCategoryColor(alert.category),
                }"
              >
                <i :class="getCategoryIcon(alert.category)"></i>
                {{ getCategoryLabel(alert.category) }}
              </span>

              <span class="alert-severity" :class="alert.severity">
                <i :class="getSeverityIcon(alert.severity)"></i>
                {{ getSeverityLabel(alert.severity) }}
              </span>

              <span
                v-if="alert.data?.daysRemaining"
                class="alert-days"
                :class="{ urgent: alert.data.daysRemaining < 7 }"
              >
                <i class="fa-solid fa-clock"></i>
                {{ alert.data.daysRemaining }} يوم متبقي
              </span>
            </div>

            <!-- بيانات إضافية حسب النوع -->
            <div v-if="alert.data" class="alert-data">
              <div v-if="alert.data.productName" class="data-item">
                <i class="fa-solid fa-box"></i>
                <span>{{ alert.data.productName }}</span>
              </div>
              <div v-if="alert.data.currentStock" class="data-item">
                <i class="fa-solid fa-warehouse"></i>
                <span>المخزون: {{ alert.data.currentStock }}</span>
              </div>
              <div v-if="alert.data.dailyAverage" class="data-item">
                <i class="fa-solid fa-chart-line"></i>
                <span>المتوسط: {{ alert.data.dailyAverage }}/يوم</span>
              </div>
            </div>
          </div>

          <div class="alert-actions">
            <button
              v-if="!alert.read"
              class="action-btn mark-read"
              @click="markAsRead(alert.id)"
              title="تحديد كمقروء"
            >
              <i class="fa-solid fa-check"></i>
            </button>

            <button
              v-if="alert.actionable"
              class="action-btn view"
              @click="handleAction(alert)"
              title="عرض التفاصيل"
            >
              <i class="fa-solid fa-eye"></i>
            </button>

            <button class="action-btn delete" @click="deleteAlert(alert.id)" title="حذف">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      </transition-group>

      <!-- زر تحميل المزيد -->
      <div class="load-more" v-if="hasMore">
        <button @click="loadMore">تحميل المزيد</button>
      </div>
    </div>

    <!-- حالة عدم وجود تنبيهات -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <i class="fa-solid fa-bell-slash"></i>
      </div>
      <h3>لا توجد تنبيهات</h3>
      <p>كل شيء هادئ، لا توجد تنبيهات جديدة</p>
    </div>
  </div>
</template>

<script>
import AlertService from '@/integration/services/AlertService';

export default {
  name: 'AlertsCenter',
  data() {
    return {
      alerts: [],
      loading: false,
      currentFilter: 'all',
      currentCategory: 'all',
      pageSize: 20,
      currentPage: 1,
      categories: [
        { value: 'all', label: 'الكل', icon: 'fa-solid fa-bell', color: '#d4af37' },
        { value: 'inventory', label: 'المخزون', icon: 'fa-solid fa-box', color: '#2196F3' },
        { value: 'forecast', label: 'التوقعات', icon: 'fa-solid fa-chart-line', color: '#9c27b0' },
        { value: 'seasonal', label: 'موسمي', icon: 'fa-solid fa-calendar-alt', color: '#ff9800' },
        { value: 'abc', label: 'تحليل ABC', icon: 'fa-solid fa-chart-pie', color: '#4CAF50' },
        { value: 'system', label: 'النظام', icon: 'fa-solid fa-cog', color: '#f44336' },
      ],
    };
  },
  computed: {
    unreadCount() {
      return this.alerts.filter((a) => !a.read).length;
    },

    priorityCounts() {
      const counts = { critical: 0, high: 0, medium: 0, low: 0 };
      this.alerts.forEach((alert) => {
        if (counts[alert.severity] !== undefined) {
          counts[alert.severity]++;
        }
      });
      return counts;
    },

    categoryCounts() {
      const counts = {};
      this.alerts.forEach((alert) => {
        counts[alert.category] = (counts[alert.category] || 0) + 1;
      });
      return counts;
    },

    filteredAlerts() {
      let filtered = [...this.alerts];

      // تصفية حسب الحالة
      if (this.currentFilter === 'unread') {
        filtered = filtered.filter((a) => !a.read);
      } else if (this.currentFilter === 'critical') {
        filtered = filtered.filter((a) => a.severity === 'critical' || a.severity === 'high');
      }

      // تصفية حسب التصنيف
      if (this.currentCategory !== 'all') {
        filtered = filtered.filter((a) => a.category === this.currentCategory);
      }

      // ترتيب حسب الأحدث
      filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

      // تقسيم الصفحات
      return filtered.slice(0, this.currentPage * this.pageSize);
    },

    hasMore() {
      let total = this.alerts.length;
      if (this.currentFilter === 'unread') total = this.unreadCount;
      if (this.currentFilter === 'critical')
        total = this.priorityCounts.critical + this.priorityCounts.high;
      if (this.currentCategory !== 'all') total = this.categoryCounts[this.currentCategory] || 0;

      return this.filteredAlerts.length < total;
    },
  },
  mounted() {
    this.loadAlerts();

    // الاستماع للتحديثات
    AlertService.subscribe(this.handleAlertUpdate);
  },
  beforeUnmount() {
    // إلغاء الاشتراك
    AlertService.unsubscribe(this.handleAlertUpdate);
  },
  methods: {
    loadAlerts() {
      this.loading = true;
      try {
        this.alerts = AlertService.getAlerts();
        this.currentPage = 1;
      } catch (error) {
        console.error('خطأ في تحميل التنبيهات:', error);
      } finally {
        this.loading = false;
      }
    },

    handleAlertUpdate(alerts) {
      this.alerts = alerts;
    },

    markAsRead(alertId) {
      AlertService.markAsRead(alertId);
    },

    markAllAsRead() {
      AlertService.markAllAsRead();
    },

    deleteAlert(alertId) {
      AlertService.deleteAlert(alertId);
    },

    handleAction(alert) {
      if (alert.action?.handler) {
        const handler = alert.action.handler;
        const params = alert.action.params || {};

        if (handler === 'viewProduct' && params.productId) {
          this.$router.push(`/dashboard/products?view=${params.productId}`);
        } else if (handler === 'viewForecast') {
          this.$router.push('/dashboard/forecast');
        } else if (handler === 'viewSeasonality') {
          this.$router.push('/dashboard/forecast?tab=seasonality');
        }
      }
    },

    loadMore() {
      this.currentPage++;
    },

    formatTime(timestamp) {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return 'الآن';
      if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
      if (diffHours < 24) return `منذ ${diffHours} ساعة`;
      if (diffDays === 1) return 'أمس';
      if (diffDays < 7) return `منذ ${diffDays} أيام`;

      return date.toLocaleDateString('ar-SA');
    },

    getCategoryLabel(category) {
      const cat = this.categories.find((c) => c.value === category);
      return cat ? cat.label : category;
    },

    getCategoryIcon(category) {
      const cat = this.categories.find((c) => c.value === category);
      return cat ? cat.icon : 'fa-solid fa-bell';
    },

    getCategoryColor(category) {
      const cat = this.categories.find((c) => c.value === category);
      return cat ? cat.color : '#d4af37';
    },

    getDefaultIcon(alert) {
      const icons = {
        inventory: 'fa-solid fa-box',
        forecast: 'fa-solid fa-chart-line',
        seasonal: 'fa-solid fa-calendar-alt',
        abc: 'fa-solid fa-chart-pie',
        system: 'fa-solid fa-cog',
      };
      return icons[alert.category] || 'fa-solid fa-bell';
    },

    getSeverityIcon(severity) {
      const icons = {
        critical: 'fa-solid fa-exclamation-triangle',
        high: 'fa-solid fa-exclamation-circle',
        medium: 'fa-solid fa-exclamation',
        low: 'fa-solid fa-info-circle',
      };
      return icons[severity] || 'fa-solid fa-bell';
    },

    getSeverityLabel(severity) {
      const labels = {
        critical: 'حرج',
        high: 'عالي',
        medium: 'متوسط',
        low: 'منخفض',
      };
      return labels[severity] || severity;
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.alerts-center {
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

.btn-refresh,
.btn-mark-read {
  padding: 12px 24px;
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-refresh {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--gold-1);
}

.btn-mark-read {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.btn-refresh:hover,
.btn-mark-read:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* إحصائيات */
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

.stat-card.critical .stat-icon {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.stat-card.high .stat-icon {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.stat-card.medium .stat-icon {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.stat-card.low .stat-icon {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
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

/* تبويبات */
.filters-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.filter-tab {
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 30px;
  color: var(--text-dim);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.filter-tab:hover {
  border-color: var(--gold-1);
  color: var(--gold-1);
}

.filter-tab.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.filter-tab .badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.75rem;
}

.filter-tab.active .badge {
  background: rgba(0, 0, 0, 0.2);
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 25px;
}

.category-tab {
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  color: var(--text-dim);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.category-tab:hover {
  border-color: var(--gold-1);
}

.category-tab.active {
  background: var(--gold-gradient-soft);
  border-color: var(--gold-1);
  color: var(--gold-1);
}

.category-tab .badge {
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 0.7rem;
  color: white;
}

/* قائمة التنبيهات */
.alerts-list {
  margin-top: 20px;
}

.alert-item {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 15px;
  border: 1px solid var(--border-light);
  display: flex;
  gap: 20px;
  transition: all 0.3s;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.alert-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold);
}

.alert-item.severity-critical {
  border-right: 4px solid #f44336;
}

.alert-item.severity-high {
  border-right: 4px solid #ff9800;
}

.alert-item.severity-medium {
  border-right: 4px solid #2196f3;
}

.alert-item.severity-low {
  border-right: 4px solid #4caf50;
}

.alert-item.alert-read {
  opacity: 0.7;
  background: var(--bg-primary);
}

.alert-icon {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.alert-title {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
}

.alert-time {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.alert-message {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 12px;
  line-height: 1.5;
}

.alert-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.alert-category,
.alert-severity,
.alert-days {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.alert-category {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-1);
}

.alert-severity.critical {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.alert-severity.high {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.alert-severity.medium {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.alert-severity.low {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.alert-days {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.alert-days.urgent {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.alert-data {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  background: var(--bg-primary);
  padding: 10px 15px;
  border-radius: 12px;
  margin-top: 10px;
}

.data-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-dim);
  font-size: 0.85rem;
}

.data-item i {
  color: var(--gold-1);
}

.alert-actions {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  flex-shrink: 0;
}

.action-btn {
  width: 35px;
  height: 35px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  background: var(--bg-primary);
  color: var(--text-dim);
}

.action-btn.mark-read:hover {
  background: #4caf50;
  color: white;
}

.action-btn.view:hover {
  background: var(--gold-1);
  color: var(--bg-deep);
}

.action-btn.delete:hover {
  background: #f44336;
  color: white;
}

/* زر تحميل المزيد */
.load-more {
  text-align: center;
  margin-top: 30px;
}

.load-more button {
  padding: 12px 30px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 30px;
  color: var(--gold-1);
  cursor: pointer;
  transition: all 0.3s;
}

.load-more button:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: translateY(-3px);
}

/* حالة فارغة */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: var(--bg-card);
  border-radius: 24px;
  border: 1px solid var(--border-light);
}

.empty-icon {
  font-size: 4rem;
  color: var(--text-dim);
  margin-bottom: 20px;
  animation: float 3s ease infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-state h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.empty-state p {
  color: var(--text-dim);
  font-size: 1rem;
}

/* تأثيرات الحركة */
.alert-enter-active,
.alert-leave-active {
  transition: all 0.3s;
}

.alert-enter {
  opacity: 0;
  transform: translateX(20px);
}

.alert-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* استجابة للشاشات الصغيرة */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .header-actions {
    width: 100%;
    justify-content: center;
  }

  .alert-item {
    flex-direction: column;
  }

  .alert-actions {
    justify-content: flex-end;
  }

  .category-tabs {
    justify-content: center;
  }
}
</style>
