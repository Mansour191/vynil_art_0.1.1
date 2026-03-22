<template>
  <div class="notifications-page container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow-sm border-0 rounded-lg overflow-hidden bg-card">
          <div class="card-header bg-surface border-bottom p-4 d-flex justify-content-between align-items-center">
            <h2 class="mb-0 text-gold h4">
              <i class="fa-solid fa-bell me-2"></i> {{ $t('notificationsCenter') || 'مركز الإشعارات' }}
            </h2>
            <div class="actions">
              <button 
                v-if="unreadCount > 0" 
                @click="markAllAsRead" 
                class="btn btn-sm btn-outline-gold me-2"
              >
                <i class="fa-solid fa-check-double me-1"></i> {{ $t('markAllAsRead') }}
              </button>
              <button @click="clearAll" class="btn btn-sm btn-outline-danger">
                <i class="fa-solid fa-trash-alt me-1"></i> {{ $t('clearAll') || 'مسح الكل' }}
              </button>
            </div>
          </div>

          <div class="card-body p-0">
            <div v-if="notifications.length === 0" class="text-center py-5 opacity-50">
              <i class="fa-solid fa-bell-slash fa-4x mb-3 text-gold"></i>
              <h3>{{ $t('noNotifications') }}</h3>
              <p>{{ $t('noNotificationsMessage') || 'لا توجد إشعارات جديدة حالياً.' }}</p>
            </div>

            <div v-else class="notifications-list">
              <div 
                v-for="notification in notifications" 
                :key="notification.id" 
                class="notification-item p-4 border-bottom transition-all"
                :class="{ 'unread': !notification.read }"
                @click="handleNotificationClick(notification)"
              >
                <div class="d-flex align-items-start gap-3">
                  <div class="notification-icon-wrapper" :class="notification.type">
                    <i :class="notification.icon || 'fa-solid fa-bell'"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <h5 class="mb-0 h6 font-weight-bold">{{ notification.title }}</h5>
                      <span class="small text-muted">{{ formatTime(notification.time) }}</span>
                    </div>
                    <p class="mb-0 text-secondary small">{{ notification.message }}</p>
                  </div>
                  <div class="notification-actions">
                    <button 
                      @click.stop="deleteNotification(notification.id)" 
                      class="btn btn-link text-muted p-0 hover-danger"
                    >
                      <i class="fa-solid fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const store = useStore();
const router = useRouter();
const { t, locale } = useI18n();

const notifications = computed(() => store.getters['user/notifications']);
const unreadCount = computed(() => store.getters['user/unreadCount']);

const markAllAsRead = () => {
  store.dispatch('user/markAllRead');
};

const clearAll = () => {
  if (confirm(t('confirmClearAllNotifications') || 'هل أنت متأكد من مسح جميع الإشعارات؟')) {
    notifications.value.forEach(n => store.dispatch('user/deleteNotification', n.id));
  }
};

const deleteNotification = (id) => {
  store.dispatch('user/deleteNotification', id);
};

const handleNotificationClick = (notification) => {
  if (!notification.read) {
    store.dispatch('user/markNotificationRead', notification.id);
  }
  if (notification.link) {
    router.push(notification.link);
  }
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = Math.floor((now - date) / 1000);

  if (diff < 60) return t('justNow') || 'الآن';
  if (diff < 3600) return t('minutesAgo', { count: Math.floor(diff / 60) }) || `${Math.floor(diff / 60)} دقيقة`;
  if (diff < 86400) return t('hoursAgo', { count: Math.floor(diff / 3600) }) || `${Math.floor(diff / 3600)} ساعة`;
  
  return date.toLocaleDateString(locale.value);
};
</script>

<style scoped>
.notifications-page {
  min-height: 80vh;
}

.bg-card {
  background: var(--bg-card);
}

.bg-surface {
  background: var(--bg-surface);
}

.text-gold {
  color: var(--gold-primary);
}

.btn-outline-gold {
  color: var(--gold-primary);
  border-color: var(--gold-primary);
}

.btn-outline-gold:hover {
  background: var(--gold-gradient);
  color: #000;
  border-color: transparent;
}

.notification-item {
  cursor: pointer;
  position: relative;
}

.notification-item:hover {
  background: rgba(212, 175, 55, 0.05);
}

.notification-item.unread {
  background: rgba(212, 175, 55, 0.02);
  border-right: 4px solid var(--gold-primary);
}

.notification-icon-wrapper {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.notification-icon-wrapper.success { background: rgba(40, 167, 69, 0.1); color: #28a745; }
.notification-icon-wrapper.danger { background: rgba(220, 53, 69, 0.1); color: #dc3545; }
.notification-icon-wrapper.warning { background: rgba(255, 193, 7, 0.1); color: #ffc107; }
.notification-icon-wrapper.info { background: rgba(23, 162, 184, 0.1); color: #17a2b8; }

.hover-danger:hover {
  color: #dc3545 !important;
}

.transition-all {
  transition: all 0.2s ease;
}
</style>
