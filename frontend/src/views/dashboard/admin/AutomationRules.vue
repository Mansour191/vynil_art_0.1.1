<template>
  <div class="automation-rules">
    <div class="page-header">
      <h1><i class="fa-solid fa-robot"></i> قواعد الأتمتة الذكية</h1>
      <button class="btn-primary" @click="showRuleModal = true">
        <i class="fa-solid fa-plus"></i> قاعدة جديدة
      </button>
    </div>

    <div class="rules-list">
      <div v-for="rule in rules" :key="rule.id" class="rule-card">
        <div class="rule-header">
          <div class="rule-title">
            <i class="fa-solid fa-cog"></i>
            <h3>{{ rule.name }}</h3>
          </div>
          <label class="switch">
            <input type="checkbox" v-model="rule.enabled" @change="toggleRule(rule)" />
            <span class="slider"></span>
          </label>
        </div>

        <div class="rule-details">
          <p><strong>الحدث:</strong> {{ getTriggerLabel(rule.trigger) }}</p>
          <p><strong>الإجراء:</strong> {{ getActionLabel(rule.action) }}</p>
        </div>

        <div class="rule-actions">
          <button @click="editRule(rule)" class="btn-icon">
            <i class="fa-solid fa-edit"></i>
          </button>
          <button @click="deleteRule(rule.id)" class="btn-icon delete">
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- نافذة إضافة/تعديل قاعدة -->
    <div class="modal" v-if="showRuleModal" @click.self="showRuleModal = false">
      <div class="modal-content">
        <h2>{{ editingRule ? 'تعديل قاعدة' : 'قاعدة جديدة' }}</h2>

        <form @submit.prevent="saveRule">
          <div class="form-group">
            <label>اسم القاعدة</label>
            <input type="text" v-model="form.name" required />
          </div>

          <div class="form-group">
            <label>الحدث</label>
            <select v-model="form.trigger" required>
              <option value="order.delivered">اكتمال طلب</option>
              <option value="order.shipped">شحن طلب</option>
              <option value="inventory.low">انخفاض المخزون</option>
              <option value="schedule.daily">موعد يومي</option>
              <option value="schedule.weekly">موعد أسبوعي</option>
            </select>
          </div>

          <div class="form-group">
            <label>الإجراء</label>
            <select v-model="form.action" required>
              <option value="sync.order">ترحيل الطلبات</option>
              <option value="sync.inventory">تحديث المخزون</option>
              <option value="create.invoice">إنشاء فاتورة</option>
              <option value="send.email">إرسال بريد</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="button" @click="showRuleModal = false">إلغاء</button>
            <button type="submit">حفظ</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AutomationService from '@/integration/services/AutomationService';

export default {
  name: 'AutomationRules',
  data() {
    return {
      rules: [],
      showRuleModal: false,
      editingRule: null,
      form: {
        name: '',
        trigger: '',
        action: '',
        enabled: true,
      },
    };
  },
  mounted() {
    this.loadRules();
  },
  methods: {
    loadRules() {
      this.rules = AutomationService.getRules();
    },

    getTriggerLabel(trigger) {
      const labels = {
        'order.delivered': 'اكتمال طلب',
        'order.shipped': 'شحن طلب',
        'inventory.low': 'انخفاض المخزون',
        'schedule.daily': 'موعد يومي',
        'schedule.weekly': 'موعد أسبوعي',
      };
      return labels[trigger] || trigger;
    },

    getActionLabel(action) {
      const labels = {
        'sync.order': 'ترحيل الطلبات',
        'sync.inventory': 'تحديث المخزون',
        'create.invoice': 'إنشاء فاتورة',
        'send.email': 'إرسال بريد',
      };
      return labels[action] || action;
    },

    toggleRule(rule) {
      AutomationService.toggleRule(rule.id, rule.enabled);
    },

    editRule(rule) {
      this.editingRule = rule;
      this.form = { ...rule };
      this.showRuleModal = true;
    },

    deleteRule(ruleId) {
      if (confirm('هل أنت متأكد من حذف هذه القاعدة؟')) {
        AutomationService.deleteRule(ruleId);
        this.loadRules();
      }
    },

    saveRule() {
      if (this.editingRule) {
        AutomationService.updateRule(this.editingRule.id, this.form);
      } else {
        AutomationService.addRule(this.form);
      }

      this.showRuleModal = false;
      this.editingRule = null;
      this.form = { name: '', trigger: '', action: '', enabled: true };
      this.loadRules();
    },
  },
};
</script>

<style scoped>
.automation-rules {
  padding: 25px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.rules-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.rule-card {
  background: var(--bg-card);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--border-light);
  position: relative;
}

.rule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.rule-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rule-title i {
  color: var(--gold-1);
}

.rule-title h3 {
  color: white;
  font-size: 1rem;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: '';
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4caf50;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.rule-details {
  margin-bottom: 15px;
}

.rule-details p {
  color: var(--text-dim);
  margin: 5px 0;
}

.rule-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-icon {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-icon:hover {
  background: var(--gold-1);
  color: var(--bg-deep);
}

.btn-icon.delete:hover {
  background: #f44336;
  color: white;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
}

.modal-content h2 {
  color: white;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  color: var(--text-dim);
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.form-actions button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.form-actions button[type='submit'] {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}
</style>
