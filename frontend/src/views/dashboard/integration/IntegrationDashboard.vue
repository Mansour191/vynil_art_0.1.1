<template>
  <div class="integration-dashboard">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-plug header-icon"></i>
          لوحة التكامل
        </h1>
        <p class="header-subtitle">مراقبة وإدارة التكامل مع ERPNext</p>
      </div>
      <div class="header-actions">
        <button class="btn-sync-all" @click="syncAll" :disabled="globalSyncing">
          <i :class="globalSyncing ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
          <span>{{ globalSyncing ? 'جاري المزامنة الشاملة...' : 'مزامنة شاملة' }}</span>
        </button>
        <button class="btn-refresh" @click="refreshAll">
          <i class="fa-solid fa-redo-alt"></i>
          <span>تحديث</span>
        </button>
      </div>
    </div>

    <!-- حالة الاتصال مع ERPNext -->
    <div class="connection-card" :class="{ connected: connectionStatus }">
      <div class="connection-icon">
        <i :class="connectionStatus ? 'fa-solid fa-check-circle' : 'fa-solid fa-exclamation-circle'"></i>
      </div>
      <div class="connection-info">
        <h3>ERPNext</h3>
        <p>{{ connectionStatus ? 'متصل' : 'غير متصل' }}</p>
        <small v-if="connectionStatus">آخر تحديث: {{ lastSync || 'لم تتم المزامنة بعد' }}</small>
      </div>
      <button class="btn-test" @click="testConnection" :disabled="testing">
        {{ testing ? 'جاري الاختبار...' : 'اختبار الاتصال' }}
      </button>
    </div>

    <!-- إحصائيات المزامنة -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon products">
          <i class="fa-solid fa-box"></i>
        </div>
        <div class="stat-content">
          <h3>المنتجات</h3>
          <div class="stat-numbers">
            <div class="stat-item">
              <span class="stat-label">الإجمالي:</span>
              <span class="stat-value">{{ stats.products.total }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">متزامن:</span>
              <span class="stat-value success">{{ stats.products.synced }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">معلق:</span>
              <span class="stat-value warning">{{ stats.products.pending }}</span>
            </div>
          </div>
          <div class="stat-actions">
            <button class="btn-sync" @click="syncProducts" :disabled="syncing.products">
              <i :class="syncing.products ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
              {{ syncing.products ? 'جاري...' : 'مزامنة' }}
            </button>
            <router-link to="/dashboard/products" class="btn-view">عرض</router-link>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon customers">
          <i class="fa-solid fa-users"></i>
        </div>
        <div class="stat-content">
          <h3>العملاء</h3>
          <div class="stat-numbers">
            <div class="stat-item">
              <span class="stat-label">الإجمالي:</span>
              <span class="stat-value">{{ stats.customers.total }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">متزامن:</span>
              <span class="stat-value success">{{ stats.customers.synced }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">معلق:</span>
              <span class="stat-value warning">{{ stats.customers.pending }}</span>
            </div>
          </div>
          <div class="stat-actions">
            <button class="btn-sync" @click="syncCustomers" :disabled="syncing.customers">
              <i :class="syncing.customers ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
              {{ syncing.customers ? 'جاري...' : 'مزامنة' }}
            </button>
            <router-link to="/dashboard/users" class="btn-view">عرض</router-link>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon orders">
          <i class="fa-solid fa-shopping-cart"></i>
        </div>
        <div class="stat-content">
          <h3>الطلبات</h3>
          <div class="stat-numbers">
            <div class="stat-item">
              <span class="stat-label">الإجمالي:</span>
              <span class="stat-value">{{ stats.orders.total }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">مرحل:</span>
              <span class="stat-value success">{{ stats.orders.synced }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">معلق:</span>
              <span class="stat-value warning">{{ stats.orders.pending }}</span>
            </div>
          </div>
          <div class="stat-actions">
            <button class="btn-sync" @click="syncOrders" :disabled="syncing.orders">
              <i :class="syncing.orders ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-sync-alt'"></i>
              {{ syncing.orders ? 'جاري...' : 'ترحيل' }}
            </button>
            <router-link to="/dashboard/orders" class="btn-view">عرض</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- شريط التقدم للمزامنة الشاملة -->
    <transition name="fade">
      <div v-if="globalSyncing" class="global-progress">
        <div class="progress-info">
          <i class="fa-solid fa-cog fa-spin"></i>
          <span>جاري المزامنة الشاملة...</span>
        </div>
        <div class="progress-steps">
          <div
            class="step"
            :class="{
              active: syncStep === 'products',
              done: syncStep === 'customers' || syncStep === 'orders' || syncStep === 'done',
            }"
          >
            <i class="fa-solid fa-box"></i>
            <span>المنتجات</span>
          </div>
          <div
            class="step"
            :class="{
              active: syncStep === 'customers',
              done: syncStep === 'orders' || syncStep === 'done',
            }"
          >
            <i class="fa-solid fa-users"></i>
            <span>العملاء</span>
          </div>
          <div class="step" :class="{ active: syncStep === 'orders', done: syncStep === 'done' }">
            <i class="fa-solid fa-shopping-cart"></i>
            <span>الطلبات</span>
          </div>
        </div>
      </div>
    </transition>

    <!-- سجل المزامنة -->
    <div class="sync-history">
      <div class="history-header">
        <h3><i class="fa-solid fa-history"></i> سجل المزامنة</h3>
        <button class="btn-clear" @click="clearHistory" v-if="syncHistory.length > 0">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>

      <div class="history-list" v-if="syncHistory.length > 0">
        <div
          v-for="record in syncHistory"
          :key="record.id"
          class="history-item"
          :class="record.status"
        >
          <div class="history-icon">
            <i :class="record.icon"></i>
          </div>
          <div class="history-details">
            <div class="history-title">{{ record.title }}</div>
            <div class="history-meta">
              <span class="history-time">{{ record.time }}</span>
              <span class="history-stats" v-if="record.stats">
                +{{ record.stats.created }} / ↻{{ record.stats.updated }} / ✗{{
                  record.stats.failed
                }}
              </span>
            </div>
          </div>
          <div class="history-status">
            <span class="status-badge" :class="record.status">
              {{
                record.status === 'success'
                  ? 'نجاح'
                  : record.status === 'error'
                  ? 'فشل'
                  : 'قيد التنفيذ'
              }}
            </span>
          </div>
        </div>
      </div>

      <div v-else class="no-history">
        <i class="fa-solid fa-history"></i>
        <p>لا يوجد سجل مزامنة بعد</p>
      </div>
    </div>

    <!-- أخطاء التكامل -->
    <div class="integration-errors" v-if="integrationErrors.length > 0">
      <div class="errors-header">
        <h3><i class="fa-solid fa-exclamation-triangle"></i> أخطاء التكامل</h3>
        <button class="btn-clear" @click="clearErrors">
          <i class="fa-solid fa-check"></i>
        </button>
      </div>

      <div class="errors-list">
        <div v-for="error in integrationErrors" :key="error.id" class="error-item">
          <i class="fa-solid fa-times-circle"></i>
          <div class="error-details">
            <div class="error-message">{{ error.message }}</div>
            <div class="error-time">{{ error.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProductSyncService from '@/integration/services/ProductSyncService';
import CustomerSyncService from '@/integration/services/CustomerSyncService';
import OrderSyncService from '@/integration/services/OrderSyncService';
import ERPNextService from '@/integration/services/ERPNextService';

export default {
  name: 'IntegrationDashboard',
  data() {
    return {
      connectionStatus: false,
      lastSync: null,
      testing: false,
      globalSyncing: false,
      syncStep: null,
      syncing: {
        products: false,
        customers: false,
        orders: false,
      },
      stats: {
        products: { total: 0, synced: 0, pending: 0 },
        customers: { total: 0, synced: 0, pending: 0 },
        orders: { total: 0, synced: 0, pending: 0 },
      },
      syncHistory: [],
      integrationErrors: [],
    };
  },
  mounted() {
    this.loadStats();
    this.loadSyncHistory();
  },
  methods: {
    async testConnection() {
      this.testing = true;
      const result = await ERPNextService.testConnection();
      this.connectionStatus = result.success;
      this.testing = false;

      if (result.success) {
        this.addToHistory({
          title: 'اتصال ERPNext',
          status: 'success',
          icon: 'fa-solid fa-plug',
        });
      } else {
        this.addToHistory({
          title: 'فشل الاتصال بـ ERPNext',
          status: 'error',
          icon: 'fa-solid fa-exclamation-triangle',
        });
        this.integrationErrors.push({
          id: Date.now(),
          message: 'فشل الاتصال بـ ERPNext',
          time: new Date().toLocaleString('ar-SA'),
        });
      }
    },

    async syncProducts() {
      this.syncing.products = true;
      this.addToHistory({
        title: 'مزامنة المنتجات',
        status: 'pending',
        icon: 'fa-solid fa-box',
      });

      try {
        const result = await ProductSyncService.syncProducts();

        if (result.success) {
          this.addToHistory({
            title: 'مزامنة المنتجات',
            status: 'success',
            icon: 'fa-solid fa-box',
            stats: result.stats,
          });
        } else {
          throw new Error(result.message);
        }
      } catch (error) {
        this.addToHistory({
          title: 'فشل مزامنة المنتجات',
          status: 'error',
          icon: 'fa-solid fa-box',
        });
        this.integrationErrors.push({
          id: Date.now(),
          message: error.message,
          time: new Date().toLocaleString('ar-SA'),
        });
      } finally {
        this.syncing.products = false;
        this.loadStats();
      }
    },

    async syncCustomers() {
      this.syncing.customers = true;
      this.addToHistory({
        title: 'مزامنة العملاء',
        status: 'pending',
        icon: 'fa-solid fa-users',
      });

      try {
        const result = await CustomerSyncService.syncCustomers();

        if (result.success) {
          this.addToHistory({
            title: 'مزامنة العملاء',
            status: 'success',
            icon: 'fa-solid fa-users',
            stats: result.stats,
          });
        } else {
          throw new Error(result.message);
        }
      } catch (error) {
        this.addToHistory({
          title: 'فشل مزامنة العملاء',
          status: 'error',
          icon: 'fa-solid fa-users',
        });
        this.integrationErrors.push({
          id: Date.now(),
          message: error.message,
          time: new Date().toLocaleString('ar-SA'),
        });
      } finally {
        this.syncing.customers = false;
        this.loadStats();
      }
    },

    async syncOrders() {
      this.syncing.orders = true;
      this.addToHistory({
        title: 'ترحيل الطلبات',
        status: 'pending',
        icon: 'fa-solid fa-shopping-cart',
      });

      try {
        const result = await OrderSyncService.syncOrders();

        if (result.success) {
          this.addToHistory({
            title: 'ترحيل الطلبات',
            status: 'success',
            icon: 'fa-solid fa-shopping-cart',
            stats: result.stats,
          });
        } else {
          throw new Error(result.message);
        }
      } catch (error) {
        this.addToHistory({
          title: 'فشل ترحيل الطلبات',
          status: 'error',
          icon: 'fa-solid fa-shopping-cart',
        });
        this.integrationErrors.push({
          id: Date.now(),
          message: error.message,
          time: new Date().toLocaleString('ar-SA'),
        });
      } finally {
        this.syncing.orders = false;
        this.loadStats();
      }
    },

    async syncAll() {
      this.globalSyncing = true;
      this.integrationErrors = [];

      // مزامنة المنتجات
      this.syncStep = 'products';
      await this.syncProducts();

      // مزامنة العملاء
      this.syncStep = 'customers';
      await this.syncCustomers();

      // ترحيل الطلبات
      this.syncStep = 'orders';
      await this.syncOrders();

      this.syncStep = 'done';
      this.globalSyncing = false;

      this.addToHistory({
        title: 'مزامنة شاملة',
        status: 'success',
        icon: 'fa-solid fa-check-circle',
      });
    },

    loadStats() {
      // هنا هنجلب الإحصائيات من الـ store
      // هذا مؤقتاً
      this.stats = {
        products: { total: 156, synced: 134, pending: 22 },
        customers: { total: 89, synced: 45, pending: 44 },
        orders: { total: 234, synced: 156, pending: 78 },
      };
    },

    loadSyncHistory() {
      // جلب سجل المزامنة من localStorage
      const saved = localStorage.getItem('syncHistory');
      if (saved) {
        this.syncHistory = JSON.parse(saved);
      }
    },

    addToHistory(record) {
      const newRecord = {
        id: Date.now(),
        time: new Date().toLocaleString('ar-SA'),
        ...record,
      };

      this.syncHistory.unshift(newRecord);

      // حفظ آخر 20 سجل
      if (this.syncHistory.length > 20) {
        this.syncHistory = this.syncHistory.slice(0, 20);
      }

      localStorage.setItem('syncHistory', JSON.stringify(this.syncHistory));
    },

    clearHistory() {
      this.syncHistory = [];
      localStorage.removeItem('syncHistory');
    },

    clearErrors() {
      this.integrationErrors = [];
    },

    refreshAll() {
      this.loadStats();
      this.testConnection();
    },
  },
};
</script>

<style scoped>
@import '@/assets/theme.css';

.integration-dashboard {
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

.btn-sync-all,
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

.btn-sync-all {
  background: linear-gradient(135deg, #4caf50, #45a049);
  color: white;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-refresh {
  background: var(--bg-card);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-sync-all:hover,
.btn-refresh:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.5);
}

/* بطاقة الاتصال */
.connection-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 25px;
}

.connection-card.connected {
  border-color: #4caf50;
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.2);
}

.connection-icon i {
  font-size: 3rem;
  color: #f44336;
}

.connection-card.connected .connection-icon i {
  color: #4caf50;
}

.connection-info {
  flex: 1;
}

.connection-info h3 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.connection-info p {
  color: var(--text-dim);
  margin-bottom: 5px;
}

.connection-info small {
  color: var(--gold-1);
}

.btn-test {
  padding: 10px 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--gold-1);
  cursor: pointer;
  transition: all 0.3s;
}

.btn-test:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

/* شبكة الإحصائيات */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 25px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
  display: flex;
  align-items: flex-start;
  gap: 20px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.stat-icon.products {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.stat-icon.customers {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.stat-icon.orders {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.stat-content {
  flex: 1;
}

.stat-content h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.stat-numbers {
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  color: var(--text-dim);
  font-size: 0.9rem;
}

.stat-value {
  font-weight: 600;
}

.stat-value.success {
  color: #4caf50;
}

.stat-value.warning {
  color: #ff9800;
}

.stat-actions {
  display: flex;
  gap: 10px;
}

.btn-sync,
.btn-view {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.3s;
  text-decoration: none;
}

.btn-sync {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-view {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-sync:hover,
.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.btn-sync:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* شريط التقدم الشامل */
.global-progress {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-glow);
  box-shadow: var(--shadow-gold);
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--gold-1);
  margin-bottom: 20px;
}

.progress-info i {
  font-size: 1.2rem;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 25px;
  left: 50px;
  right: 50px;
  height: 2px;
  background: var(--border-light);
  z-index: 1;
}

.step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step i {
  width: 50px;
  height: 50px;
  background: var(--bg-primary);
  border: 2px solid var(--border-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: var(--text-dim);
  transition: all 0.3s;
}

.step span {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.step.active i {
  border-color: var(--gold-1);
  background: var(--gold-gradient);
  color: var(--bg-deep);
  box-shadow: var(--shadow-gold);
}

.step.active span {
  color: var(--gold-1);
}

.step.done i {
  border-color: #4caf50;
  background: #4caf50;
  color: white;
}

.step.done span {
  color: #4caf50;
}

/* سجل المزامنة */
.sync-history {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  margin-bottom: 25px;
  border: 1px solid var(--border-light);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  color: white;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.history-header h3 i {
  color: var(--gold-1);
}

.btn-clear {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.3s;
}

.btn-clear:hover {
  background: var(--danger);
  color: white;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: var(--bg-primary);
  border-radius: 12px;
  border-right: 3px solid transparent;
}

.history-item.success {
  border-right-color: #4caf50;
}

.history-item.error {
  border-right-color: #f44336;
}

.history-item.pending {
  border-right-color: #ff9800;
}

.history-icon i {
  font-size: 1.2rem;
}

.history-item.success .history-icon i {
  color: #4caf50;
}

.history-item.error .history-icon i {
  color: #f44336;
}

.history-item.pending .history-icon i {
  color: #ff9800;
}

.history-details {
  flex: 1;
}

.history-title {
  color: white;
  font-weight: 600;
  margin-bottom: 3px;
}

.history-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: var(--text-dim);
}

.history-stats {
  color: var(--gold-1);
}

.history-status .status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
}

.status-badge.success {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.status-badge.error {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.status-badge.pending {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.no-history {
  text-align: center;
  padding: 40px;
  color: var(--text-dim);
}

.no-history i {
  font-size: 3rem;
  margin-bottom: 10px;
  opacity: 0.5;
}

/* أخطاء التكامل */
.integration-errors {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid #f44336;
  border-radius: 20px;
  padding: 25px;
}

.errors-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.errors-header h3 {
  color: #f44336;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.errors-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.error-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.error-item i {
  color: #f44336;
}

.error-details {
  flex: 1;
}

.error-message {
  color: white;
  font-size: 0.9rem;
  margin-bottom: 3px;
}

.error-time {
  color: var(--text-dim);
  font-size: 0.8rem;
}

/* تأثيرات */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
