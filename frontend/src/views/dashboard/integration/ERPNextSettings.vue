<template>
  <div class="erpnext-settings">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-cog header-icon"></i>
          إعدادات التكامل مع ERPNext
        </h1>
        <p class="header-subtitle">تكوين وإدارة الاتصال مع نظام ERPNext</p>
      </div>
      <div class="header-actions">
        <button class="btn-test" @click="testConnection" :disabled="testing">
          <i :class="testing ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-plug'"></i>
          <span>{{ testing ? 'جاري الاختبار...' : 'اختبار الاتصال' }}</span>
        </button>
        <button class="btn-save" @click="saveSettings" :disabled="!settingsChanged">
          <i class="fa-solid fa-save"></i>
          <span>حفظ الإعدادات</span>
        </button>
      </div>
    </div>

    <!-- حالة الاتصال -->
    <div class="connection-status" :class="{ connected: connectionStatus }" v-if="connectionTested">
      <div class="status-icon">
        <i :class="connectionStatus ? 'fa-solid fa-check-circle' : 'fa-solid fa-times-circle'"></i>
      </div>
      <div class="status-message">
        <h3>{{ connectionStatus ? 'اتصال ناجح' : 'فشل الاتصال' }}</h3>
        <p>{{ connectionMessage }}</p>
      </div>
    </div>

    <!-- نموذج الإعدادات -->
    <form @submit.prevent="saveSettings" class="settings-form">
      <!-- قسم الاتصال الأساسي -->
      <div class="settings-section">
        <h3><i class="fa-solid fa-plug"></i> إعدادات الاتصال</h3>

        <div class="form-row">
          <div class="form-group">
            <label>عنوان الخادم (URL) <span class="required">*</span></label>
            <input
              type="url"
              v-model="settings.baseURL"
              placeholder="https://your-erpnext.com"
              required
            />
            <small class="hint">مثال: https://erpnext.yourcompany.com</small>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>مفتاح API (API Key) <span class="required">*</span></label>
            <input type="text" v-model="settings.apiKey" placeholder="أدخل مفتاح API" required />
          </div>

          <div class="form-group">
            <label>السر (API Secret) <span class="required">*</span></label>
            <input
              :type="showSecret ? 'text' : 'password'"
              v-model="settings.apiSecret"
              placeholder="أدخل secret key"
              required
            />
            <button type="button" class="toggle-secret" @click="showSecret = !showSecret">
              <i :class="showSecret ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
            </button>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>مهلة الطلب (Timeout)</label>
            <input type="number" v-model="settings.timeout" min="5" max="120" />
            <small class="hint">بالثواني (افتراضي: 30 ثانية)</small>
          </div>
        </div>
      </div>

      <!-- إعدادات المزامنة -->
      <div class="settings-section">
        <h3><i class="fa-solid fa-sync-alt"></i> إعدادات المزامنة</h3>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.sync.autoSync" />
              <span class="checkbox-custom"></span>
              <span>تفعيل المزامنة التلقائية</span>
            </label>
          </div>
        </div>

        <div class="form-row" v-if="settings.sync.autoSync">
          <div class="form-group">
            <label>فترة المزامنة</label>
            <select v-model="settings.sync.interval">
              <option value="5">كل 5 دقائق</option>
              <option value="15">كل 15 دقيقة</option>
              <option value="30">كل 30 دقيقة</option>
              <option value="60">كل ساعة</option>
              <option value="360">كل 6 ساعات</option>
              <option value="720">كل 12 ساعة</option>
              <option value="1440">كل يوم</option>
            </select>
          </div>

          <div class="form-group">
            <label>عدد محاولات إعادة المحاولة</label>
            <input type="number" v-model="settings.sync.retryAttempts" min="1" max="10" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.sync.autoCreateProducts" />
              <span class="checkbox-custom"></span>
              <span>إنشاء منتجات جديدة في ERPNext تلقائياً</span>
            </label>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.sync.autoUpdateProducts" />
              <span class="checkbox-custom"></span>
              <span>تحديث المنتجات في ERPNext تلقائياً</span>
            </label>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.sync.autoCreateCustomers" />
              <span class="checkbox-custom"></span>
              <span>إنشاء عملاء جدد في ERPNext تلقائياً</span>
            </label>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.sync.autoCreateInvoices" />
              <span class="checkbox-custom"></span>
              <span>إنشاء فواتير للطلبات المكتملة تلقائياً</span>
            </label>
          </div>
        </div>
      </div>

      <!-- إعدادات المحاسبة -->
      <div class="settings-section">
        <h3><i class="fa-solid fa-chart-line"></i> إعدادات المحاسبة</h3>

        <div class="form-row">
          <div class="form-group">
            <label>المستودع الافتراضي</label>
            <input
              type="text"
              v-model="settings.accounting.defaultWarehouse"
              placeholder="Stores - SA"
            />
          </div>

          <div class="form-group">
            <label>حساب الضرائب الافتراضي</label>
            <input
              type="text"
              v-model="settings.accounting.defaultTaxAccount"
              placeholder="VAT - 15% - SA"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>طريقة الدفع الافتراضية</label>
            <select v-model="settings.accounting.defaultPaymentMethod">
              <option value="cash">الدفع عند الاستلام</option>
              <option value="card">بطاقة ائتمان</option>
              <option value="bank">تحويل بنكي</option>
            </select>
          </div>

          <div class="form-group">
            <label>نسبة الضريبة الافتراضية (%)</label>
            <input
              type="number"
              v-model="settings.accounting.defaultTaxRate"
              min="0"
              max="100"
              step="0.1"
            />
          </div>
        </div>
      </div>

      <!-- إعدادات تصنيف المنتجات -->
      <div class="settings-section">
        <h3><i class="fa-solid fa-tags"></i> تصنيف المنتجات</h3>

        <div class="info-box">
          <i class="fa-solid fa-info-circle"></i>
          <span>ربط تصنيفات الموقع مع مجموعات المنتجات في ERPNext</span>
        </div>

        <div class="category-mapping">
          <div v-for="(category, index) in categoryMappings" :key="index" class="mapping-row">
            <div class="mapping-site">
              <span>{{ category.siteLabel }}</span>
            </div>
            <div class="mapping-arrow">
              <i class="fa-solid fa-arrow-left"></i>
            </div>
            <div class="mapping-erpnext">
              <input
                type="text"
                v-model="category.erpnextGroup"
                :placeholder="`مجموعة ${category.siteLabel} في ERPNext`"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- أزرار الحفظ -->
      <div class="form-actions">
        <button type="button" class="btn-reset" @click="resetSettings">
          <i class="fa-solid fa-undo-alt"></i>
          <span>إعادة تعيين</span>
        </button>
        <button type="submit" class="btn-save" :disabled="!settingsChanged">
          <i class="fa-solid fa-save"></i>
          <span>حفظ الإعدادات</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
// DEPRECATED: ERPNextService has been migrated to GraphQL
// Use GraphQLERPNextService instead
import { erpNextSyncService } from '@/services/ERPNextSyncService';

const emit = defineEmits(['settings-saved']);

// State
const testing = ref(false);
const connectionTested = ref(false);
const connectionStatus = ref(false);
const connectionMessage = ref('');
const showSecret = ref(false);
const originalSettings = ref(null);

const settings = reactive({
  baseURL: '',
  apiKey: '',
  apiSecret: '',
  timeout: 30,
  sync: {
    autoSync: false,
    interval: 60,
    retryAttempts: 3,
    autoCreateProducts: true,
    autoUpdateProducts: true,
    autoCreateCustomers: true,
    autoCreateInvoices: true,
  },
  accounting: {
    defaultWarehouse: 'Stores - SA',
    defaultTaxAccount: 'VAT - 15% - SA',
    defaultPaymentMethod: 'cash',
    defaultTaxRate: 15,
  },
});

const categoryMappings = ref([
  { siteKey: 'walls', siteLabel: 'جدران', erpnextGroup: 'ملصقات جدران' },
  { siteKey: 'doors', siteLabel: 'أبواب', erpnextGroup: 'ملصقات أبواب' },
  { siteKey: 'furniture', siteLabel: 'أثاث', erpnextGroup: 'ملصقات أثاث' },
  { siteKey: 'cars', siteLabel: 'سيارات', erpnextGroup: 'ملصقات سيارات' },
  { siteKey: 'kitchens', siteLabel: 'مطابخ', erpnextGroup: 'ملصقات مطابخ' },
  { siteKey: 'ceilings', siteLabel: 'أسقف', erpnextGroup: 'ملصقات أسقف' },
  { siteKey: 'tiles', siteLabel: 'بلاط', erpnextGroup: 'ملصقات بلاط' },
]);

// Computed
const settingsChanged = computed(() => {
  return JSON.stringify(originalSettings.value) !== JSON.stringify(settings);
});

// Methods
const loadSettings = () => {
  const saved = localStorage.getItem('erpnextSettings');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      Object.assign(settings, parsed);
      if (parsed.categoryMappings) {
        categoryMappings.value = parsed.categoryMappings;
      }
    } catch (e) {
      console.error('Failed to load settings:', e);
    }
  } else {
    // Default settings
    settings.baseURL = ''; // Could use process.env if available
    settings.apiKey = '';
    settings.apiSecret = '';
  }
  originalSettings.value = JSON.parse(JSON.stringify(settings));
};

const testConnection = async () => {
  testing.value = true;
  connectionTested.value = true;
  try {
    const result = await erpNextSyncService.testConnection();
    connectionStatus.value = result.success;
    connectionMessage.value = result.success
      ? 'تم الاتصال بنجاح مع ERPNext'
      : result.message || 'فشل الاتصال';
  } catch (error) {
    connectionStatus.value = false;
    connectionMessage.value = error.message || 'حدث خطأ أثناء الاتصال';
  } finally {
    testing.value = false;
  }
};

const saveSettings = () => {
  try {
    const settingsToSave = {
      ...settings,
      categoryMappings: categoryMappings.value,
    };
    localStorage.setItem('erpnextSettings', JSON.stringify(settingsToSave));
    originalSettings.value = JSON.parse(JSON.stringify(settings));
    emit('settings-saved', settingsToSave);
    alert('✅ تم حفظ الإعدادات بنجاح');
  } catch (error) {
    console.error('Save error:', error);
    alert('❌ فشل حفظ الإعدادات');
  }
};

const resetSettings = () => {
  if (confirm('هل أنت متأكد من إعادة تعيين جميع الإعدادات؟')) {
    loadSettings();
  }
};

// Lifecycle
onMounted(() => {
  loadSettings();
});
</script>

<style scoped>
@import '@/assets/theme.css';

.erpnext-settings {
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

.btn-test,
.btn-save {
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

.btn-test {
  background: var(--bg-card);
  color: var(--gold-1);
  border: 1px solid var(--border-light);
}

.btn-save {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-test:hover,
.btn-save:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* حالة الاتصال */
.connection-status {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 20px 25px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid var(--border-light);
}

.connection-status.connected {
  border-color: #4caf50;
  background: rgba(76, 175, 80, 0.1);
}

.connection-status .status-icon i {
  font-size: 2.5rem;
}

.connection-status.connected .status-icon i {
  color: #4caf50;
}

.connection-status:not(.connected) .status-icon i {
  color: #f44336;
}

.status-message h3 {
  color: white;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.status-message p {
  color: var(--text-dim);
}

/* نموذج الإعدادات */
.settings-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.settings-section {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
}

.settings-section h3 {
  color: var(--gold-1);
  font-size: 1.1rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-light);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  position: relative;
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: var(--text-dim);
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.required {
  color: var(--danger);
  margin-right: 3px;
}

.form-group input,
.form-group select {
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.hint {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-top: 5px;
}

/* زر إظهار/إخفاء السر */
.toggle-secret {
  position: absolute;
  left: 12px;
  top: 38px;
  background: transparent;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  padding: 5px;
  transition: color 0.3s;
}

.toggle-secret:hover {
  color: var(--gold-1);
}

/* خانات الاختيار */
.checkbox-group {
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
}

.checkbox-label input[type='checkbox'] {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-light);
  border-radius: 5px;
  position: relative;
  transition: all 0.3s;
}

.checkbox-label input:checked + .checkbox-custom {
  background: var(--gold-gradient);
  border-color: transparent;
}

.checkbox-label input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--bg-deep);
  font-size: 0.8rem;
  font-weight: 700;
}

/* تصنيف المنتجات */
.info-box {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid #2196f3;
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2196f3;
}

.category-mapping {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mapping-row {
  display: grid;
  grid-template-columns: 100px 30px 1fr;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: var(--bg-primary);
  border-radius: 12px;
}

.mapping-site {
  color: white;
  font-weight: 500;
}

.mapping-arrow {
  text-align: center;
  color: var(--gold-1);
}

.mapping-erpnext input {
  width: 100%;
  padding: 8px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  color: white;
}

.mapping-erpnext input:focus {
  outline: none;
  border-color: var(--gold-1);
}

/* أزرار الحفظ */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.btn-reset {
  padding: 12px 24px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-reset:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  border-color: var(--gold-1);
}

/* استجابة للشاشات الصغيرة */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .mapping-row {
    grid-template-columns: 1fr;
    gap: 5px;
  }

  .mapping-arrow {
    transform: rotate(90deg);
  }
}
</style>
