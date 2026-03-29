<template>
  <div class="alert-center" ref="el">
    <!-- Alert Trigger with Counter -->
    <v-btn
      @click="toggleDropdown"
      icon="mdi-bell"
      variant="elevated"
      color="primary"
      class="alert-trigger"
    >
      <v-badge
        v-if="unreadCount > 0"
        :content="unreadCount"
        color="error"
        offset-x="-4"
        offset-y="-4"
      />
    </v-btn>

    <!-- Alert Dropdown -->
    <v-menu
      v-model="showDropdown"
      location="bottom end"
      offset="10"
    >
      <v-card min-width="350" max-width="400" elevation="8">
        <!-- Header -->
        <v-card-title class="d-flex align-center justify-space-between pa-4">
          <span class="text-h6">التنبيهات</span>
          <div class="d-flex ga-2">
            <v-btn
              @click="markAllAsRead"
              icon="mdi-check-all"
              variant="text"
              size="small"
              color="primary"
              title="تحديد الكل كمقروء"
            />
            <v-btn
              @click="clearAll"
              icon="mdi-delete"
              variant="text"
              size="small"
              color="error"
              title="مسح الكل"
            />
            <v-btn
              @click="showDropdown = false"
              icon="mdi-close"
              variant="text"
              size="small"
            />
          </div>
        </v-card-title>
        
        <v-divider />
        
        <!-- Filters -->
        <v-card-text class="pa-4">
          <v-btn-toggle
            v-model="currentFilter"
            :items="filters"
            variant="outlined"
            density="compact"
            class="mb-4"
          />
          
          <!-- Alert List -->
          <div v-if="filteredAlerts.length === 0" class="text-center pa-8">
            <v-icon size="48" color="success" class="mb-4">mdi-check-circle</v-icon>
            <p class="text-body-2 text-medium-emphasis">لا توجد تنبيهات</p>
          </div>
          
          <v-list v-else density="compact" class="alert-list">
            <v-list-item
              v-for="alert in filteredAlerts.slice(0, 5)"
              :key="alert.id"
              :class="[
                'alert-item',
                { 'bg-surface-lighten-1': !alert.read },
                `border-${alert.severity}`
              ]"
              @click="markAsRead(alert.id)"
            >
              <template v-slot:prepend>
                <v-avatar size="32" :color="getAlertColor(alert.type)">
                  <v-icon size="16" color="white">
                    {{ getAlertIcon(alert.type) }}
                  </v-icon>
                </v-avatar>
              </template>
              
              <v-list-item-title class="text-body-1 font-weight-medium mb-1">
                {{ alert.title }}
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-2 mb-1">
                {{ alert.message }}
              </v-list-item-subtitle>
              <v-list-item-subtitle class="text-caption text-medium-emphasis">
                {{ formatTime(alert.timestamp) }}
              </v-list-item-subtitle>
              
              <template v-slot:append>
                <v-btn
                  icon="mdi-delete"
                  variant="text"
                  size="small"
                  color="default"
                  @click.stop="deleteAlert(alert.id)"
                  title="حذف"
                />
              </template>
            </v-list-item>
          </v-list>
        </v-card-text>
        
        <!-- Footer -->
        <v-card-actions v-if="alerts.length > 0" class="pa-4">
          <v-btn
            @click="viewAll"
            variant="outlined"
            color="primary"
            block
          >
            عرض الكل ({{ alerts.length }})
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import AlertService from '@/integration/services/AlertService';

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
const formatTime = (timestamp) => {
  if (!timestamp) return '';
  return new Date(timestamp).toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

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
    inventory_difference: 'mdi-package-variant',
    price_difference: 'mdi-tag',
    customer_balance: 'mdi-account-clock',
    pending_orders: 'mdi-clock',
    low_stock: 'mdi-alert',
    sync_errors: 'mdi-alert-circle',
  };
  return icons[type] || 'mdi-bell';
};

const getAlertColor = (severity) => {
  const colors = {
    high: 'error',
    medium: 'warning',
    low: 'success',
  };
  return colors[severity] || 'primary';
};

const markAsRead = (id) => {
  const alertIndex = alerts.value.findIndex(a => a.id === id);
  if (alertIndex !== -1) {
    alerts.value[alertIndex].read = true;
  }
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

const deleteAlert = (id) => {
  if (confirm('هل أنت متأكد من حذف هذا التنبيه؟')) {
    AlertService.deleteAlert(id);
    alerts.value = alerts.value.filter(a => a.id !== id);
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

