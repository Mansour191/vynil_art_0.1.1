<template>
  <div class="alert-center" ref="el">
    <!-- زر التنبيهات مع العداد -->
    <div class="alert-trigger" @click="toggleDropdown">
      <i class="fa-solid fa-bell"></i>
      <span v-if="unreadCount > 0" class="alert-badge">{{ unreadCount }}</span>
    </div>

    <!-- قائمة التنبيهات -->
    <transition name="slide-down">
      <div class="alert-dropdown" v-if="showDropdown">
        <div class="alert-header">
          <h3>التنبيهات</h3>
          <div class="alert-actions">
            <button @click="markAllAsRead" title="تحديد الكل كمقروء">
              <i class="fa-solid fa-check-double"></i>
            </button>
            <button @click="clearAll" title="مسح الكل">
              <i class="fa-solid fa-trash"></i>
            </button>
            <button @click="showDropdown = false">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
        </div>

        <div class="alert-filters">
          <button
            v-for="filter in filters"
            :key="filter.value"
            class="filter-btn"
            :class="{ active: currentFilter === filter.value }"
            @click="currentFilter = filter.value"
          >
            {{ filter.label }}
          </button>
        </div>

        <div class="alert-list">
          <div v-if="filteredAlerts.length === 0" class="no-alerts">
            <i class="fa-solid fa-check-circle"></i>
            <p>لا توجد تنبيهات</p>
          </div>

          <div
            v-for="alert in filteredAlerts.slice(0, 5)"
            :key="alert.id"
            class="alert-item"
            :class="[alert.severity, { unread: !alert.read }]"
          >
            <div class="alert-icon">
              <i :class="getAlertIcon(alert.type)"></i>
            </div>

            <div class="alert-content">
              <div class="alert-title">{{ alert.title }}</div>
              <div class="alert-message">{{ alert.message }}</div>
              <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
            </div>
          </div>
        </div>

        <div class="alert-footer" v-if="alerts.length > 0">
          <button @click="viewAll">عرض الكل ({{ alerts.length }})</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import AlertService from '@/integration/services/AlertService';
import moment from 'moment';

const router = useRouter();

// State
const showDropdown = ref(false);
const currentFilter = ref('all');
const alerts = ref([]);
const filters = [
  { label: 'الكل', value: 'all' },
  { label: 'غير مقروء', value: 'unread' },
  { label: 'عالي', value: 'high' },
];

const el = ref(null);

const formatTime = (timestamp) => {
  if (!timestamp) return '';
  return moment(timestamp).fromNow();
};

// Computed
const unreadCount = computed(() => alerts.value.filter((a) => !a.read).length);

const filteredAlerts = computed(() => {
  if (currentFilter.value === 'all') return alerts.value;
  if (currentFilter.value === 'unread') {
    return alerts.value.filter((a) => !a.read);
  }
  return alerts.value.filter((a) => a.severity === currentFilter.value);
});

// Methods
const loadAlerts = () => {
  alerts.value = AlertService.getAlerts({ limit: 20 });
};

const handleNewAlert = (alert) => {
  alerts.value = [alert, ...alerts.value].slice(0, 20);
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
  if (showDropdown.value) {
    loadAlerts();
  }
};

const handleClickOutside = (event) => {
  if (el.value && !el.value.contains(event.target)) {
    showDropdown.value = false;
  }
};

const getAlertIcon = (type) => {
  const icons = {
    inventory_difference: 'fa-solid fa-boxes',
    price_difference: 'fa-solid fa-tag',
    customer_balance: 'fa-solid fa-user-clock',
    pending_orders: 'fa-solid fa-clock',
    low_stock: 'fa-solid fa-exclamation-triangle',
    sync_errors: 'fa-solid fa-exclamation-circle',
  };
  return icons[type] || 'fa-solid fa-bell';
};

const markAllAsRead = () => {
  AlertService.markAllAsRead();
  alerts.value.forEach((a) => (a.read = true));
};

const clearAll = () => {
  if (confirm('هل أنت متأكد من مسح جميع التنبيهات؟')) {
    AlertService.clearAllAlerts();
    alerts.value = [];
  }
};

const viewAll = () => {
  showDropdown.value = false;
  router.push('/dashboard/alerts');
};

// Lifecycle
onMounted(() => {
  loadAlerts();
  AlertService.subscribe(handleNewAlert);
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.alert-center {
  position: relative;
}

.alert-trigger {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  color: var(--gold-1);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
}

.alert-trigger:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: translateY(-2px);
}

.alert-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #f44336;
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.alert-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 350px;
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 16px;
  margin-top: 10px;
  box-shadow: var(--shadow-xl), var(--shadow-gold);
  z-index: 1000;
  overflow: hidden;
}

.alert-header {
  padding: 15px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-header h3 {
  color: white;
  font-size: 1rem;
}

.alert-actions {
  display: flex;
  gap: 8px;
}

.alert-actions button {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.3s;
}

.alert-actions button:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.alert-filters {
  padding: 10px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  gap: 5px;
}

.filter-btn {
  padding: 5px 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  color: var(--text-dim);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
}

.filter-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.alert-list {
  max-height: 350px;
  overflow-y: auto;
}

.alert-item {
  padding: 12px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  gap: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.alert-item:hover {
  background: var(--bg-primary);
}

.alert-item.unread {
  background: rgba(212, 175, 55, 0.05);
}

.alert-item.high {
  border-right: 3px solid #f44336;
}

.alert-item.medium {
  border-right: 3px solid #ff9800;
}

.alert-item.low {
  border-right: 3px solid #4caf50;
}

.alert-icon {
  width: 35px;
  height: 35px;
  border-radius: 10px;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-1);
  flex-shrink: 0;
}

.alert-content {
  flex: 1;
  min-width: 0;
}

.alert-title {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-message {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alert-time {
  color: var(--text-dim);
  font-size: 0.7rem;
}

.no-alerts {
  padding: 30px;
  text-align: center;
  color: var(--text-dim);
}

.no-alerts i {
  font-size: 2rem;
  margin-bottom: 10px;
  opacity: 0.5;
}

.alert-footer {
  padding: 12px;
  border-top: 1px solid var(--border-light);
  text-align: center;
}

.alert-footer button {
  background: transparent;
  border: none;
  color: var(--gold-1);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.alert-footer button:hover {
  text-decoration: underline;
}
</style>
