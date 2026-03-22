import OrderSyncService from './OrderSyncService';
import ProductSyncService from './ProductSyncService';
import AlertService from './AlertService';
import EmailService from './EmailService';

class AutomationService {
  constructor() {
    this.rules = [];
    this.jobs = [];
    this.loadRules();
    this.startScheduler();
  }

  // تحميل قواعد الأتمتة من localStorage
  loadRules() {
    const saved = localStorage.getItem('automationRules');
    if (saved) {
      this.rules = JSON.parse(saved);
    } else {
      // قواعد افتراضية
      this.rules = [
        {
          id: 'auto-sync-orders',
          name: 'ترحيل تلقائي للطلبات المكتملة',
          enabled: true,
          trigger: 'order.delivered',
          action: 'sync.order',
          conditions: { status: 'delivered' },
          createdAt: new Date().toISOString(),
        },
        {
          id: 'auto-update-inventory',
          name: 'تحديث المخزون يومياً',
          enabled: false,
          trigger: 'schedule.daily',
          action: 'sync.inventory',
          conditions: { time: '02:00' },
          createdAt: new Date().toISOString(),
        },
        {
          id: 'auto-create-invoice',
          name: 'إنشاء فواتير للطلبات المكتملة',
          enabled: true,
          trigger: 'order.delivered',
          action: 'create.invoice',
          conditions: { status: 'delivered' },
          createdAt: new Date().toISOString(),
        },
      ];
      this.saveRules();
    }
  }

  saveRules() {
    localStorage.setItem('automationRules', JSON.stringify(this.rules));
  }

  // بدء المجدول (يفحص كل دقيقة)
  startScheduler() {
    setInterval(() => {
      this.checkScheduledRules();
    }, 60000); // كل دقيقة
  }

  // فحص القواعد المجدولة
  async checkScheduledRules() {
    const now = new Date();
    const currentHour = now.getHours();
    const currentMinute = now.getMinutes();

    for (const rule of this.rules) {
      if (!rule.enabled) continue;

      if (rule.trigger === 'schedule.daily') {
        const [hour, minute] = rule.conditions.time.split(':').map(Number);
        if (currentHour === hour && currentMinute === minute) {
          await this.executeRule(rule);
        }
      }
    }
  }

  // تنفيذ قاعدة معينة
  async executeRule(rule) {
    console.log(`🤖 تنفيذ قاعدة: ${rule.name}`);

    try {
      let result;

      switch (rule.action) {
        case 'sync.order':
          result = await this.syncPendingOrders();
          break;
        case 'sync.inventory':
          result = await this.syncAllInventory();
          break;
        case 'create.invoice':
          result = await this.createInvoicesForDeliveredOrders();
          break;
        default:
          console.log('لا يوجد إجراء مطابق');
          return;
      }

      // تسجيل التنفيذ الناجح
      this.logExecution(rule, result);
    } catch (error) {
      console.error('خطأ في تنفيذ القاعدة:', error);

      // إرسال تنبيه بالخطأ
      await AlertService.sendAlert({
        type: 'automation_error',
        severity: 'high',
        title: '🤖 خطأ في الأتمتة',
        message: `فشل تنفيذ قاعدة "${rule.name}": ${error.message}`,
        actionable: true,
        action: {
          label: 'مراجعة',
          handler: () => console.log('مراجعة الخطأ'),
        },
      });

      // إرسال بريد للمدير
      await EmailService.notifyAdmin('sync_error', {
        entity: rule.name,
        error: error.message,
      });
    }
  }

  // مزامنة الطلبات المعلقة
  async syncPendingOrders() {
    const result = await OrderSyncService.syncOrders();

    if (result.success && result.stats.created > 0) {
      await AlertService.sendAlert({
        type: 'automation_success',
        severity: 'low',
        title: '✅ تم ترحيل الطلبات تلقائياً',
        message: `تم ترحيل ${result.stats.created} طلب جديد`,
        actionable: false,
      });
    }

    return result;
  }

  // مزامنة المخزون بالكامل
  async syncAllInventory() {
    const result = await ProductSyncService.syncProducts();

    if (result.success && (result.stats.created > 0 || result.stats.updated > 0)) {
      await AlertService.sendAlert({
        type: 'automation_success',
        severity: 'low',
        title: '🔄 تم تحديث المخزون تلقائياً',
        message: `تم تحديث ${result.stats.updated} منتج وإضافة ${result.stats.created} منتج جديد`,
        actionable: false,
      });
    }

    return result;
  }

  // إنشاء فواتير للطلبات المكتملة
  async createInvoicesForDeliveredOrders() {
    const result = await OrderSyncService.syncOrders();

    if (result.success && result.stats.created > 0) {
      await AlertService.sendAlert({
        type: 'automation_success',
        severity: 'low',
        title: '💰 تم إنشاء فواتير جديدة',
        message: `تم إنشاء ${result.stats.created} فاتورة جديدة`,
        actionable: false,
      });
    }

    return result;
  }

  // تسجيل تنفيذ قاعدة
  logExecution(rule, result) {
    const logs = JSON.parse(localStorage.getItem('automationLogs') || '[]');
    logs.unshift({
      ruleId: rule.id,
      ruleName: rule.name,
      result,
      timestamp: new Date().toISOString(),
    });

    // احتفظ بآخر 100 تنفيذ
    if (logs.length > 100) logs.pop();

    localStorage.setItem('automationLogs', JSON.stringify(logs));
  }

  // إضافة قاعدة جديدة
  addRule(rule) {
    rule.id = `rule-${Date.now()}`;
    rule.createdAt = new Date().toISOString();
    this.rules.push(rule);
    this.saveRules();
  }

  // تحديث قاعدة
  updateRule(ruleId, updates) {
    const index = this.rules.findIndex((r) => r.id === ruleId);
    if (index !== -1) {
      this.rules[index] = { ...this.rules[index], ...updates };
      this.saveRules();
    }
  }

  // حذف قاعدة
  deleteRule(ruleId) {
    this.rules = this.rules.filter((r) => r.id !== ruleId);
    this.saveRules();
  }

  // تفعيل/تعطيل قاعدة
  toggleRule(ruleId, enabled) {
    const rule = this.rules.find((r) => r.id === ruleId);
    if (rule) {
      rule.enabled = enabled;
      this.saveRules();
    }
  }

  // الحصول على جميع القواعد
  getRules() {
    return this.rules;
  }

  // الحصول على سجل التنفيذ
  getExecutionLogs(limit = 20) {
    const logs = JSON.parse(localStorage.getItem('automationLogs') || '[]');
    return logs.slice(0, limit);
  }
}

export default new AutomationService();
