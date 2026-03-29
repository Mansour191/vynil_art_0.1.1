// src/integration/services/AlertService.js

class AlertService {
  constructor() {
    this.alerts = [];
    this.listeners = [];
    this.alertTypes = {
      INFO: 'info',
      WARNING: 'warning',
      DANGER: 'danger',
      SUCCESS: 'success',
      RECOMMENDATION: 'recommendation',
    };

    this.alertCategories = {
      INVENTORY: 'inventory',
      FORECAST: 'forecast',
      SEASONAL: 'seasonal',
      SYSTEM: 'system',
      ABC: 'abc',
    };

    this.loadPersistedAlerts();
    this.startCleanupTask();
  }

  startCleanupTask() {
    // تنظيف التنبيهات المنتهية كل ساعة
    setInterval(() => {
      this.clearExpiredAlerts();
    }, 3600000);
  }

  // ========== إدارة المستمعين ==========

  subscribe(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter((cb) => cb !== callback);
    };
  }

  notifyListeners() {
    this.listeners.forEach((callback) => callback(this.alerts));
  }

  // ========== إنشاء تنبيه جديد ==========

  async sendAlert(alertData) {
    const alert = {
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      read: false,
      acknowledged: false,
      ...alertData,
      // التأكد من وجود القيم الافتراضية
      type: alertData.type || this.alertTypes.INFO,
      category: alertData.category || this.alertCategories.SYSTEM,
      severity: alertData.severity || 'low',
      title: alertData.title || 'تنبيه جديد',
      message: alertData.message || '',
      actionable: alertData.actionable || false,
      action: alertData.action || null,
      icon: this.getIconForType(alertData.type, alertData.category),
      expiresAt: alertData.expiresAt || this.getDefaultExpiry(),
    };

    this.alerts.unshift(alert);

    // الحفاظ على عدد معقول من التنبيهات في الذاكرة (مثلاً 100)
    if (this.alerts.length > 100) {
      this.alerts = this.alerts.slice(0, 100);
    }

    // حفظ في localStorage (اختياري)
    this.persistAlerts();

    // إشعار المستمعين
    this.notifyListeners();

    // إذا كان التنبيه عالي الأهمية، أرسل إشعار سطح مكتب
    if (alert.severity === 'high' || alert.severity === 'critical') {
      this.sendDesktopNotification(alert);
    }

    return alert;
  }

  // ========== إنشاء تنبيهات ذكية ==========

  // تنبيه المخزون المنخفض
  async createLowStockAlert(product, forecast) {
    const dailyAverage = forecast?.average || 0;
    const daysRemaining = dailyAverage > 0 ? Math.floor(product.stock / dailyAverage) : 999;

    let severity = 'low';
    let type = this.alertTypes.INFO;

    if (daysRemaining < 3) {
      severity = 'critical';
      type = this.alertTypes.DANGER;
    } else if (daysRemaining < 7) {
      severity = 'high';
      type = this.alertTypes.WARNING;
    } else if (daysRemaining < 15) {
      severity = 'medium';
      type = this.alertTypes.WARNING;
    }

    // تحقق من وجود تنبيه مشابه لم يقرأ بعد
    const existingAlert = this.alerts.find(
      (a) =>
        a.category === this.alertCategories.INVENTORY &&
        a.data?.productId === product.id &&
        !a.read &&
        a.severity === severity
    );

    if (existingAlert) {
      // تحديث التنبيه الموجود بدلاً من إنشاء جديد
      existingAlert.timestamp = new Date().toISOString();
      existingAlert.message = `مخزون ${product.name} منخفض (${product.stock} قطعة)، سينفد خلال ${daysRemaining} أيام`;
      existingAlert.data.daysRemaining = daysRemaining;
      this.notifyListeners();
      return existingAlert;
    }

    return this.sendAlert({
      type,
      category: this.alertCategories.INVENTORY,
      severity,
      title: `⚠️ مخزون منخفض: ${product.name}`,
      message: `المخزون الحالي: ${product.stock} قطعة، سينفد خلال ${daysRemaining} أيام`,
      actionable: true,
      icon: daysRemaining < 7 ? 'fa-solid fa-exclamation-triangle' : 'fa-solid fa-exclamation-circle',
      action: {
        label: 'عرض المنتج',
        handler: 'viewProduct',
        params: { productId: product.id },
      },
      data: {
        productId: product.id,
        productName: product.name,
        currentStock: product.stock,
        daysRemaining,
        dailyAverage,
      },
    });
  }

  // تنبيه توقعات المبيعات
  async createForecastAlert(forecastData) {
    const alerts = [];

    // تنبيه نمو غير طبيعي
    if (forecastData.trends?.change > 30) {
      alerts.push(
        await this.sendAlert({
          type: this.alertTypes.RECOMMENDATION,
          category: this.alertCategories.FORECAST,
          severity: 'high',
          title: '📈 نمو قوي متوقع',
          message: `المبيعات في ارتفاع بنسبة ${forecastData.trends.change}% مقارنة بالفترة السابقة`,
          actionable: true,
          icon: 'fa-solid fa-rocket',
          action: {
            label: 'عرض التفاصيل',
            handler: 'viewForecast',
            params: { type: 'growth' },
          },
          data: {
            change: forecastData.trends.change,
            recentAvg: forecastData.trends.recentAvg,
            olderAvg: forecastData.trends.olderAvg,
          },
        })
      );
    }

    // تنبيه انخفاض حاد
    if (forecastData.trends?.change < -20) {
      alerts.push(
        await this.sendAlert({
          type: this.alertTypes.WARNING,
          category: this.alertCategories.FORECAST,
          severity: 'high',
          title: '📉 انخفاض حاد متوقع',
          message: `المبيعات في انخفاض بنسبة ${Math.abs(
            forecastData.trends.change
          )}%، قد تحتاج لعروض ترويجية`,
          actionable: true,
          icon: 'fa-solid fa-chart-line',
          action: {
            label: 'تحليل',
            handler: 'viewForecast',
            params: { type: 'decline' },
          },
          data: {
            change: forecastData.trends.change,
            recentAvg: forecastData.trends.recentAvg,
            olderAvg: forecastData.trends.olderAvg,
          },
        })
      );
    }

    return alerts;
  }

  // تنبيه تحليل ABC
  async createABCAlert(abcData, product) {
    if (product.classification === 'A' && product.stock < product.dailyAverage * 15) {
      return this.sendAlert({
        type: this.alertTypes.WARNING,
        category: this.alertCategories.ABC,
        severity: 'high',
        title: `🔴 منتج استراتيجي (A) يحتاج متابعة`,
        message: `${product.name} - مخزون منخفض لمنتج استراتيجي`,
        actionable: true,
        icon: 'fa-solid fa-crown',
        action: {
          label: 'عرض المنتج',
          handler: 'viewProduct',
          params: { productId: product.id },
        },
        data: {
          productId: product.id,
          productName: product.name,
          classification: 'A',
          stock: product.stock,
          dailyAverage: product.dailyAverage,
        },
      });
    }
    return null;
  }

  // تنبيه موسمي
  async createSeasonalAlert(seasonalData) {
    const currentMonth = new Date().getMonth();
    const nextMonth = (currentMonth + 1) % 12;

    if (seasonalData.monthly?.[nextMonth]?.peak === 'high') {
      return this.sendAlert({
        type: this.alertTypes.RECOMMENDATION,
        category: this.alertCategories.SEASONAL,
        severity: 'medium',
        title: '📅 موسم نشط قادم',
        message: `الشهر القادم متوقع أن يكون نشطاً، جهز المخزون مبكراً`,
        actionable: true,
        icon: 'fa-solid fa-calendar-alt',
        action: {
          label: 'عرض التحليل',
          handler: 'viewSeasonality',
        },
        data: {
          month: nextMonth,
          forecast: seasonalData.monthly[nextMonth],
        },
      });
    }
    return null;
  }

  // ========== إدارة التنبيهات ==========

  // جلب جميع التنبيهات
  getAlerts(filters = {}) {
    let filtered = [...this.alerts];

    if (filters.category) {
      filtered = filtered.filter((a) => a.category === filters.category);
    }
    if (filters.type) {
      filtered = filtered.filter((a) => a.type === filters.type);
    }
    if (filters.severity) {
      filtered = filtered.filter((a) => a.severity === filters.severity);
    }
    if (filters.unreadOnly) {
      filtered = filtered.filter((a) => !a.read);
    }

    return filtered;
  }

  // الحصول على التنبيهات غير المقروءة
  getUnreadCount() {
    return this.alerts.filter((a) => !a.read).length;
  }

  // الحصول على التنبيهات حسب الأولوية
  getAlertsByPriority() {
    const priority = {
      critical: [],
      high: [],
      medium: [],
      low: [],
    };

    this.alerts.forEach((alert) => {
      if (priority[alert.severity]) {
        priority[alert.severity].push(alert);
      }
    });

    return priority;
  }

  // تحديد تنبيه كمقروء
  markAsRead(alertId) {
    const alert = this.alerts.find((a) => a.id === alertId);
    if (alert) {
      alert.read = true;
      this.persistAlerts();
      this.notifyListeners();
    }
  }

  // تحديد الكل كمقروء
  markAllAsRead() {
    this.alerts.forEach((alert) => {
      alert.read = true;
    });
    this.persistAlerts();
    this.notifyListeners();
  }

  // تأكيد تنبيه (للتنبيهات التي تحتاج تفاعل)
  acknowledgeAlert(alertId) {
    const alert = this.alerts.find((a) => a.id === alertId);
    if (alert) {
      alert.acknowledged = true;
      alert.read = true;
      this.persistAlerts();
      this.notifyListeners();
    }
  }

  // حذف تنبيه
  deleteAlert(alertId) {
    this.alerts = this.alerts.filter((a) => a.id !== alertId);
    this.persistAlerts();
    this.notifyListeners();
  }

  // مسح التنبيهات المنتهية
  clearExpiredAlerts() {
    const now = new Date();
    this.alerts = this.alerts.filter((a) => {
      if (!a.expiresAt) return true;
      return new Date(a.expiresAt) > now;
    });
    this.persistAlerts();
    this.notifyListeners();
  }

  // ========== أدوات مساعدة ==========

  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  getIconForType(type, category) {
    const icons = {
      info: 'fa-solid fa-info-circle',
      warning: 'fa-solid fa-exclamation-triangle',
      danger: 'fa-solid fa-times-circle',
      success: 'fa-solid fa-check-circle',
      recommendation: 'fa-solid fa-lightbulb',
      inventory: 'fa-solid fa-box',
      forecast: 'fa-solid fa-chart-line',
      seasonal: 'fa-solid fa-calendar-alt',
      system: 'fa-solid fa-cog',
      abc: 'fa-solid fa-chart-pie',
    };

    return icons[type] || icons[category] || 'fa-solid fa-bell';
  }

  getDefaultExpiry() {
    const date = new Date();
    date.setDate(date.getDate() + 7); // أسبوع
    return date.toISOString();
  }

  // حفظ التنبيهات في localStorage
  persistAlerts() {
    try {
      localStorage.setItem('alerts', JSON.stringify(this.alerts));
    } catch (e) {
      console.error('فشل في حفظ التنبيهات:', e);
    }
  }

  // تحميل التنبيهات من localStorage
  loadPersistedAlerts() {
    try {
      const saved = localStorage.getItem('alerts');
      if (saved) {
        this.alerts = JSON.parse(saved);
      }
    } catch (e) {
      console.error('فشل في تحميل التنبيهات:', e);
    }
  }

  // إرسال إشعار سطح المكتب
  sendDesktopNotification(alert) {
    if (!('Notification' in window)) return;

    if (Notification.permission === 'granted') {
      new Notification(alert.title, {
        body: alert.message,
        icon: '/icon.png',
      });
    } else if (Notification.permission !== 'denied') {
      Notification.requestPermission();
    }
  }
}

export default new AlertService();
