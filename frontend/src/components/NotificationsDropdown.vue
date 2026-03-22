<template>
  <div class="notifications-container">
    <button class="notifications-btn" @click="toggleDropdown" ref="btn">
      <i class="fa-solid fa-bell"></i>
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>

    <div class="notifications-dropdown" v-show="isOpen" ref="dropdown">
      <div class="dropdown-header">
        <h3>{{ $t('notifications') }}</h3>
        <div class="header-actions">
          <button
            v-if="unreadCount > 0"
            class="mark-read-btn"
            @click="markAllAsRead"
            :title="$t('markAllAsRead')"
          >
            <i class="fa-solid fa-check-double"></i>
          </button>
          <button class="close-btn" @click="isOpen = false">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </div>

      <div class="notifications-list">
        <div v-if="notifications.length === 0" class="empty-notifications">
          <i class="fa-solid fa-bell-slash"></i>
          <p>{{ $t('noNotifications') }}</p>
        </div>

        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification-item"
          :class="{ unread: !notification.read }"
          @click="markAsRead(notification.id)"
        >
          <div class="notification-icon" :class="notification.type">
            <i :class="notification.icon || 'fa-solid fa-bell'"></i>
          </div>

          <div class="notification-content">
            <div class="notification-header">
              <h4>{{ notification.title }}</h4>
              <span class="notification-time">{{ formatTime(notification.time) }}</span>
            </div>
            <p>{{ notification.message }}</p>
          </div>

          <button
            class="delete-notification"
            @click.stop="deleteNotification(notification.id)"
            :title="$t('delete')"
          >
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>

      <div class="dropdown-footer" v-if="notifications.length > 0">
        <button class="view-all-btn" @click="viewAll">
          {{ $t('viewAllNotifications') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'NotificationsDropdown',
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapGetters('user', ['notifications', 'unreadCount']),
  },
  methods: {
    ...mapActions('user', ['markNotificationRead', 'markAllRead', 'deleteNotification']),

    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },

    markAsRead(id) {
      this.markNotificationRead(id);
    },

    markAllAsRead() {
      this.markAllRead();
    },

    deleteNotification(id) {
      if (confirm(this.$t('confirmDeleteNotification'))) {
        this.deleteNotification(id);
      }
    },

    viewAll() {
      this.$router.push('/notifications');
      this.isOpen = false;
    },

    formatTime(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diff = Math.floor((now - date) / 1000); // الفرق بالثواني

      if (diff < 60) return this.$t('justNow');
      if (diff < 3600) {
        const minutes = Math.floor(diff / 60);
        return this.$t('minutesAgo', { count: minutes });
      }
      if (diff < 86400) {
        const hours = Math.floor(diff / 3600);
        return this.$t('hoursAgo', { count: hours });
      }
      return date.toLocaleDateString(this.$i18n.locale);
    },

    handleClickOutside(event) {
      if (
        this.isOpen &&
        !this.$refs.dropdown?.contains(event.target) &&
        !this.$refs.btn?.contains(event.target)
      ) {
        this.isOpen = false;
      }
    },
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  },
};
</script>

<style scoped>
.notifications-container {
  position: relative;
}

.notifications-btn {
  position: relative;
  width: 42px;
  height: 42px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: 50%;
  color: var(--gold-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.notifications-btn:hover {
  border-color: var(--gold-primary);
  transform: scale(1.1);
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  background: #f44336;
  color: white;
  border-radius: 10px;
  font-size: 0.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notifications-dropdown {
  position: absolute;
  top: 50px;
  right: 0;
  width: 350px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  box-shadow: var(--shadow-soft);
  z-index: 1000;
  overflow: hidden;
}

[dir='ltr'] .notifications-dropdown {
  right: auto;
  left: 0;
}

.dropdown-header {
  padding: 15px 20px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dropdown-header h3 {
  color: var(--gold-primary);
  font-size: 1.1rem;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.mark-read-btn,
.close-btn {
  width: 30px;
  height: 30px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.3s;
}

.mark-read-btn:hover,
.close-btn:hover {
  border-color: var(--gold-primary);
  color: var(--gold-primary);
}

.notifications-list {
  max-height: 400px;
  overflow-y: auto;
}

.empty-notifications {
  padding: 40px 20px;
  text-align: center;
}

.empty-notifications i {
  font-size: 3rem;
  color: var(--gold-primary);
  opacity: 0.3;
  margin-bottom: 10px;
}

.empty-notifications p {
  color: var(--text-muted);
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: background 0.3s;
  position: relative;
}

.notification-item:hover {
  background: rgba(212, 175, 55, 0.05);
}

.notification-item.unread {
  background: rgba(212, 175, 55, 0.02);
}

.notification-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.success {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.notification-icon.info {
  background: rgba(33, 150, 243, 0.1);
  color: #2196f3;
}

.notification-icon.warning {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.notification-icon.error {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
}

.notification-header h4 {
  color: var(--text-primary);
  font-size: 0.95rem;
  margin: 0;
}

.notification-time {
  color: var(--text-muted);
  font-size: 0.75rem;
}

.notification-content p {
  color: var(--text-secondary);
  font-size: 0.85rem;
  line-height: 1.4;
  margin: 0;
}

.delete-notification {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  width: 25px;
  height: 25px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s;
}

[dir='ltr'] .delete-notification {
  left: auto;
  right: 10px;
}

.notification-item:hover .delete-notification {
  opacity: 1;
}

.delete-notification:hover {
  color: #f44336;
}

.dropdown-footer {
  padding: 15px 20px;
  border-top: 1px solid var(--border-subtle);
}

.view-all-btn {
  width: 100%;
  padding: 8px;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  color: var(--gold-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.view-all-btn:hover {
  border-color: var(--gold-primary);
  background: rgba(212, 175, 55, 0.1);
}

@media (max-width: 480px) {
  .notifications-dropdown {
    width: 300px;
    left: -100px;
  }

  [dir='ltr'] .notifications-dropdown {
    left: auto;
    right: -100px;
  }
}
</style>
