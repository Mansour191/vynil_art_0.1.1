<template>
  <div class="notifications-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="notifications-container">
      <div class="glass-card">
        <!-- Header -->
        <div class="notifications-header">
          <div class="header-content">
            <h1 class="page-title">
              <i class="fa-solid fa-bell"></i>
              الإشعارات
            </h1>
            <p class="page-subtitle">آخر الإشعارات والتحديثات</p>
          </div>
          <div class="header-actions">
            <div class="notification-stats">
              <span class="unread-count">{{ unreadCount }}</span>
              <span class="stats-label">غير مقروء</span>
            </div>
            <button class="mark-all-btn" @click="markAllAsRead" :disabled="unreadCount === 0">
              <i class="fa-solid fa-check-double"></i>
              قراءة الكل
            </button>
          </div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-tabs">
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            :class="['filter-tab', { active: activeFilter === filter.value }]"
            @click="activeFilter = filter.value"
          >
            <i :class="filter.icon"></i>
            <span>{{ filter.label }}</span>
            <span v-if="filter.count > 0" class="filter-count">{{ filter.count }}</span>
          </button>
        </div>

        <!-- Notifications List -->
        <div class="notifications-list">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner">
              <i class="fa-solid fa-spinner fa-spin"></i>
            </div>
            <p class="loading-text">جاري تحميل الإشعارات...</p>
          </div>

          <div v-else-if="filteredNotifications.length === 0" class="empty-state">
            <div class="empty-icon">
              <i class="fa-solid fa-bell-slash"></i>
            </div>
            <h3 class="empty-title">لا توجد إشعارات</h3>
            <p class="empty-text">لا توجد إشعارات في هذه الفئة</p>
          </div>

          <div v-else class="notifications-grid">
            <div 
              v-for="notification in filteredNotifications" 
              :key="notification.id" 
              :class="['notification-item', { unread: !notification.read }]"
              @click="markAsRead(notification.id)"
            >
              <div class="notification-icon">
                <i :class="getNotificationIcon(notification.type)"></i>
              </div>
              
              <div class="notification-content">
                <div class="notification-header">
                  <h3 class="notification-title">{{ notification.title }}</h3>
                  <span class="notification-time">{{ formatTime(notification.createdAt) }}</span>
                </div>
                
                <p class="notification-message">{{ notification.message }}</p>
                
                <div v-if="notification.action" class="notification-action">
                  <button 
                    class="action-btn"
                    @click.stop="handleAction(notification.action)"
                  >
                    {{ notification.action.label }}
                  </button>
                </div>
              </div>

              <div class="notification-status">
                <div v-if="!notification.read" class="unread-dot"></div>
                <button class="delete-btn" @click.stop="deleteNotification(notification.id)">
                  <i class="fa-solid fa-times"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More -->
        <div v-if="hasMore" class="load-more">
          <button class="load-more-btn" @click="loadMore" :disabled="loading">
            <i class="fa-solid fa-chevron-down"></i>
            <span v-if="!loading">تحميل المزيد</span>
            <span v-else class="loading-text">
              <i class="fa-solid fa-spinner fa-spin"></i>
              جاري التحميل...
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const loading = ref(false);
const activeFilter = ref('all');
const hasMore = ref(true);
const page = ref(1);

const notifications = ref([]);

const filters = [
  { value: 'all', label: 'الكل', icon: 'fa-solid fa-inbox', count: 0 },
  { value: 'unread', label: 'غير مقروء', icon: 'fa-solid fa-envelope', count: 0 },
  { value: 'orders', label: 'الطلبات', icon: 'fa-solid fa-shopping-bag', count: 0 },
  { value: 'payments', label: 'المدفوعات', icon: 'fa-solid fa-credit-card', count: 0 },
  { value: 'promotions', label: 'العروض', icon: 'fa-solid fa-tag', count: 0 },
  { value: 'system', label: 'النظام', icon: 'fa-solid fa-cog', count: 0 }
];

// Mock data - في الواقع سيتم جلبها من GraphQL
const mockNotifications = [
  {
    id: 1,
    type: 'order',
    title: 'تم شحن طلبك',
    message: 'طلبك #ORD001 تم شحنه وهو في طريقه إليك. يمكنك تتبع حالة الطلب عبر حسابك.',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    read: false,
    action: {
      type: 'track_order',
      label: 'تتبع الطلب',
      orderId: 'ORD001'
    }
  },
  {
    id: 2,
    type: 'payment',
    title: 'تم استلام الدفعة',
    message: 'تم استلام دفعتك بنجاح بقيمة 1,250 دج. سيتم تأكيد طلبك قريباً.',
    createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000), // 5 hours ago
    read: false,
    action: {
      type: 'view_order',
      label: 'عرض الطلب',
      orderId: 'ORD002'
    }
  },
  {
    id: 3,
    type: 'promotion',
    title: 'عرض خاص لك!',
    message: 'احصل على خصم 20% على جميع منتجات الديكور. العرض صالح لمدة 48 ساعة فقط.',
    createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
    read: true,
    action: {
      type: 'view_promotion',
      label: 'عرض العروض'
    }
  },
  {
    id: 4,
    type: 'system',
    title: 'تحديث النظام',
    message: 'تم تحديث النظام مع ميزات جديدة ومحسّنة. تحقق من الميزات الجديدة.',
    createdAt: new Date(Date.now() - 48 * 60 * 60 * 1000), // 2 days ago
    read: true,
    action: null
  },
  {
    id: 5,
    type: 'order',
    title: 'تم تأكيد طلبك',
    message: 'طلبك #ORD003 تم تأكيده بنجاح. سنقوم بتحضير طلبك للشحن قريباً.',
    createdAt: new Date(Date.now() - 72 * 60 * 60 * 1000), // 3 days ago
    read: true,
    action: {
      type: 'view_order',
      label: 'عرض الطلب',
      orderId: 'ORD003'
    }
  }
];

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length;
});

const filteredNotifications = computed(() => {
  let filtered = notifications.value;
  
  if (activeFilter.value === 'unread') {
    filtered = filtered.filter(n => !n.read);
  } else if (activeFilter.value !== 'all') {
    filtered = filtered.filter(n => n.type === activeFilter.value);
  }
  
  return filtered;
});

const getNotificationIcon = (type) => {
  const icons = {
    order: 'fa-solid fa-shopping-bag',
    payment: 'fa-solid fa-credit-card',
    promotion: 'fa-solid fa-tag',
    system: 'fa-solid fa-cog',
    review: 'fa-solid fa-star',
    message: 'fa-solid fa-envelope',
    security: 'fa-solid fa-shield-alt'
  };
  return icons[type] || 'fa-solid fa-bell';
};

const formatTime = (date) => {
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 1) return 'الآن';
  if (minutes < 60) return `منذ ${minutes} دقيقة`;
  if (hours < 24) return `منذ ${hours} ساعة`;
  if (days < 7) return `منذ ${days} يوم`;
  
  return date.toLocaleDateString('ar-SA');
};

const markAsRead = async (notificationId) => {
  try {
    const notification = notifications.value.find(n => n.id === notificationId);
    if (notification && !notification.read) {
      notification.read = true;
      // TODO: Implement GraphQL mutation to mark as read
      console.log('Mark as read:', notificationId);
    }
  } catch (error) {
    console.error('Error marking notification as read:', error);
  }
};

const markAllAsRead = async () => {
  try {
    // TODO: Implement GraphQL mutation to mark all as read
    console.log('Mark all as read');
    
    notifications.value.forEach(notification => {
      notification.read = true;
    });
  } catch (error) {
    console.error('Error marking all notifications as read:', error);
  }
};

const deleteNotification = async (notificationId) => {
  try {
    // TODO: Implement GraphQL mutation to delete notification
    console.log('Delete notification:', notificationId);
    
    notifications.value = notifications.value.filter(n => n.id !== notificationId);
  } catch (error) {
    console.error('Error deleting notification:', error);
  }
};

const handleAction = (action) => {
  switch (action.type) {
    case 'track_order':
      router.push(`/profile/orders/${action.orderId}`);
      break;
    case 'view_order':
      router.push(`/profile/orders/${action.orderId}`);
      break;
    case 'view_promotion':
      router.push('/products?promotion=true');
      break;
    case 'view_product':
      router.push(`/products/${action.productId}`);
      break;
    default:
      console.log('Unknown action:', action);
  }
};

const loadMore = async () => {
  try {
    loading.value = true;
    page.value++;
    
    // TODO: Implement GraphQL query to load more notifications
    console.log('Load more notifications, page:', page.value);
    
    // Mock loading
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In real implementation, append new notifications
    hasMore.value = false; // No more for demo
  } catch (error) {
    console.error('Error loading more notifications:', error);
  } finally {
    loading.value = false;
  }
};

const loadNotifications = async () => {
  try {
    loading.value = true;
    
    // TODO: Implement GraphQL query to fetch notifications
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    notifications.value = mockNotifications;
    
    // Update filter counts
    filters.forEach(filter => {
      if (filter.value === 'all') {
        filter.count = notifications.value.length;
      } else if (filter.value === 'unread') {
        filter.count = notifications.value.filter(n => !n.read).length;
      } else {
        filter.count = notifications.value.filter(n => n.type === filter.value).length;
      }
    });
  } catch (error) {
    console.error('Error loading notifications:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadNotifications();
});
</script>

<style scoped>
/* ===== Notifications Page ===== */
.notifications-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

/* Background Effects */
.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 20%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(212, 175, 55, 0.12) 0%, transparent 50%);
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, rgba(212, 175, 55, 0.1) 50%, transparent 100%);
  filter: blur(2px);
  animation: float 6s ease-in-out infinite;
}

.orb-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) scale(1); }
  50% { transform: translateY(-20px) scale(1.05); }
}

/* Notifications Container */
.notifications-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 800px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.08),
              inset 0 0 30px rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
}

/* Header */
.notifications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.page-title i {
  color: #d4af37;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 8px;
}

.unread-count {
  color: #d4af37;
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
}

.stats-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  margin-top: 2px;
}

.mark-all-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mark-all-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: #d4af37;
  border-color: rgba(212, 175, 55, 0.3);
}

.mark-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  position: relative;
}

.filter-tab:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.filter-tab.active {
  background: rgba(212, 175, 55, 0.2);
  border-color: rgba(212, 175, 55, 0.3);
  color: #d4af37;
}

.filter-tab i {
  font-size: 14px;
}

.filter-count {
  min-width: 20px;
  height: 20px;
  background: rgba(212, 175, 55, 0.3);
  border-radius: 50%;
  color: #1a1a2e;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.loading-spinner {
  font-size: 48px;
  color: #d4af37;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 18px;
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.7);
}

.empty-icon {
  font-size: 64px;
  color: rgba(255, 255, 255, 0.3);
  margin-bottom: 24px;
}

.empty-title {
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.empty-text {
  font-size: 16px;
  margin: 0;
}

/* Notifications List */
.notifications-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.notification-item:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.notification-item.unread {
  background: rgba(212, 175, 55, 0.05);
  border-color: rgba(212, 175, 55, 0.2);
}

.notification-icon {
  width: 48px;
  height: 48px;
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d4af37;
  font-size: 20px;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notification-title {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  line-height: 1.4;
}

.notification-time {
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  white-space: nowrap;
}

.notification-message {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.notification-action {
  margin-top: 8px;
}

.action-btn {
  padding: 6px 12px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 6px;
  color: #d4af37;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(212, 175, 55, 0.3);
  color: #ffffff;
}

.notification-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.unread-dot {
  width: 8px;
  height: 8px;
  background: #d4af37;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(212, 175, 55, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(212, 175, 55, 0);
  }
}

.delete-btn {
  width: 32px;
  height: 32px;
  background: rgba(220, 53, 69, 0.2);
  border: none;
  border-radius: 6px;
  color: #dc3545;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  background: rgba(220, 53, 69, 0.3);
  color: #ffffff;
}

/* Load More */
.load-more {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.load-more-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.load-more-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  color: #d4af37;
  border-color: rgba(212, 175, 55, 0.3);
}

.load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .notifications-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .notifications-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .filter-tabs {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .filter-tab {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .notification-item {
    padding: 16px;
    gap: 12px;
  }
  
  .notification-icon {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
  
  .notification-header {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }
  
  .notification-time {
    align-self: flex-start;
  }
}
</style>
