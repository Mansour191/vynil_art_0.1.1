import store from '@/store';

class NotificationService {
  constructor() {
    this.hasPermission = false;
    this.init();
  }

  async init() {
    if ('Notification' in window) {
      if (Notification.permission === 'granted') {
        this.hasPermission = true;
      } else if (Notification.permission !== 'denied') {
        const permission = await Notification.requestPermission();
        this.hasPermission = permission === 'granted';
      }
    }
  }

  /**
   * إرسال إشعار (داخل التطبيق + سطح المكتب + توست)
   */
  notify({ title, message, type = 'info', icon = 'fa-solid fa-info-circle', link = null }) {
    // 1. إضافة الإشعار للمتجر (Vuex)
    store.dispatch('user/addNotification', {
      title,
      message,
      type,
      icon,
      link,
      read: false,
      createdAt: new Date().toISOString()
    });

    // 2. إظهار إشعار سطح المكتب إذا كان مسموحاً
    if (this.hasPermission && document.visibilityState !== 'visible') {
      new Notification(title, {
        body: message,
        icon: '/favicon.ico'
      });
    }

    // 3. إرسال حدث للتوست (Toast)
    window.dispatchEvent(new CustomEvent('app-toast', {
      detail: { title, message, type, icon }
    }));
  }

  // اختصارات لأنواع الإشعارات
  success(title, message, link = null) {
    this.notify({ title, message, type: 'success', icon: 'fa-solid fa-check-circle', link });
  }

  error(title, message, link = null) {
    this.notify({ title, message, type: 'danger', icon: 'fa-solid fa-exclamation-circle', link });
  }

  info(title, message, link = null) {
    this.notify({ title, message, type: 'info', icon: 'fa-solid fa-info-circle', link });
  }

  warning(title, message, link = null) {
    this.notify({ title, message, type: 'warning', icon: 'fa-solid fa-exclamation-triangle', link });
  }

  /**
   * محاكاة تحديث حالة الطلب
   */
  notifyOrderStatusUpdate(orderId, status) {
    const statusMap = {
      'processing': { title: 'طلبك قيد المعالجة', message: `الطلب رقم ${orderId} يتم تجهيزه الآن.` },
      'shipped': { title: 'تم شحن طلبك', message: `الطلب رقم ${orderId} في طريقه إليك.` },
      'delivered': { title: 'تم التوصيل بنجاح', message: `تم توصيل الطلب رقم ${orderId}. شكراً لتعاملك معنا.` }
    };

    const info = statusMap[status] || { title: 'تحديث حالة الطلب', message: `تم تغيير حالة الطلب ${orderId} إلى ${status}.` };
    this.success(info.title, info.message, `/dashboard/orders/${orderId}`);
  }
}

export default new NotificationService();
