<template>
  <div class="settings-manager">
    <!-- رأس الصفحة -->
    <div class="page-header">
      <div class="header-title">
        <h1>
          <i class="fa-solid fa-cog header-icon"></i>
          الإعدادات
        </h1>
        <p class="header-subtitle">إدارة إعدادات الموقع والمتجر</p>
      </div>
      <div class="header-actions">
        <button class="btn-save-header" @click="saveAllSettings">
          <i class="fa-solid fa-save"></i>
          <span>حفظ الكل</span>
        </button>
      </div>
    </div>

    <!-- تبويبات الإعدادات -->
    <div class="settings-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.name }}</span>
      </button>
    </div>

    <!-- محتوى الإعدادات حسب التبويب -->
    <div class="settings-content">
      <!-- ===== الإعدادات العامة ===== -->
      <div v-if="activeTab === 'general'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-globe"></i> الإعدادات العامة</h2>
          <p>إعدادات الموقع الأساسية والمعلومات العامة</p>
        </div>

        <div class="settings-grid">
          <div class="settings-card">
            <h3>معلومات الموقع</h3>
            <div class="form-group">
              <label>اسم الموقع</label>
              <input
                type="text"
                v-model="settings.general.siteName"
                placeholder="أدخل اسم الموقع"
              />
            </div>
            <div class="form-group">
              <label>الوصف المختصر</label>
              <textarea
                v-model="settings.general.siteDescription"
                rows="2"
                placeholder="وصف مختصر للموقع"
              ></textarea>
            </div>
            <div class="form-group">
              <label>الكلمات المفتاحية (SEO)</label>
              <input
                type="text"
                v-model="settings.general.keywords"
                placeholder="فينيل, ملصقات, ديكور"
              />
            </div>
          </div>

          <div class="settings-card">
            <h3>الشعار والأيقونة</h3>
            <div class="logo-upload">
              <div class="logo-preview">
                <img :src="settings.general.logoPreview || '/default-logo.png'" alt="Logo" />
              </div>
              <div class="upload-controls">
                <button class="btn-upload" @click="triggerLogoUpload">
                  <i class="fa-solid fa-upload"></i> تغيير الشعار
                </button>
                <input
                  type="file"
                  ref="logoInput"
                  @change="handleLogoUpload"
                  accept="image/*"
                  style="display: none"
                />
                <p class="upload-hint">PNG, JPG - مقاس 200×200 بكسل</p>
              </div>
            </div>
            <div class="favicon-upload">
              <label>أيقونة الموقع (Favicon)</label>
              <input type="file" @change="handleFaviconUpload" accept="image/*" />
            </div>
          </div>

          <div class="settings-card">
            <h3>اللغة والاتجاه</h3>
            <div class="form-group">
              <label>اللغة الافتراضية</label>
              <select v-model="settings.general.defaultLanguage">
                <option value="ar">العربية</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
              </select>
            </div>
            <div class="form-group">
              <label>اتجاه الموقع</label>
              <select v-model="settings.general.direction">
                <option value="rtl">من اليمين لليسار (RTL)</option>
                <option value="ltr">من اليسار لليمين (LTR)</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== إعدادات المتجر ===== -->
      <div v-if="activeTab === 'store'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-store"></i> إعدادات المتجر</h2>
          <p>إدارة عمليات البيع والمخزون والشحن</p>
        </div>

        <div class="settings-grid">
          <div class="settings-card">
            <h3>العملة</h3>
            <div class="form-group">
              <label>العملة الرئيسية</label>
              <select v-model="settings.store.currency">
                <option value="SAR">ريال سعودي (SAR)</option>
                <option value="USD">دولار أمريكي (USD)</option>
                <option value="EUR">يورو (EUR)</option>
                <option value="AED">درهم إماراتي (AED)</option>
              </select>
            </div>
            <div class="form-group">
              <label>رمز العملة</label>
              <input type="text" v-model="settings.store.currencySymbol" placeholder="ر.س" />
            </div>
          </div>

          <div class="settings-card">
            <h3>الضرائب</h3>
            <div class="form-group">
              <label>نسبة الضريبة (%)</label>
              <input type="number" v-model="settings.store.taxRate" min="0" max="100" step="0.1" />
            </div>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.store.taxIncluded" />
                <span>الضريبة مضمنة في السعر</span>
              </label>
            </div>
          </div>

          <div class="settings-card">
            <h3>الشحن</h3>
            <div class="form-group">
              <label>تكلفة الشحن العادي</label>
              <input type="number" v-model="settings.store.shippingStandard" min="0" step="0.5" />
            </div>
            <div class="form-group">
              <label>تكلفة الشحن السريع</label>
              <input type="number" v-model="settings.store.shippingExpress" min="0" step="0.5" />
            </div>
            <div class="form-group">
              <label>التوصيل المجاني عند</label>
              <input
                type="number"
                v-model="settings.store.freeShippingThreshold"
                min="0"
                step="10"
              />
              <span class="input-hint">ر.س</span>
            </div>
          </div>

          <div class="settings-card">
            <h3>المخزون</h3>
            <div class="form-group">
              <label>تنبيه المخزون المنخفض عند</label>
              <input type="number" v-model="settings.store.lowStockThreshold" min="0" />
            </div>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.store.trackInventory" />
                <span>تتبع المخزون تلقائياً</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== إعدادات الدفع ===== -->
      <div v-if="activeTab === 'payment'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-credit-card"></i> إعدادات الدفع</h2>
          <p>تكوين بوابات الدفع وطرق الدفع المتاحة</p>
        </div>

        <div class="payment-methods">
          <div class="payment-card" v-for="method in paymentMethods" :key="method.id">
            <div class="payment-header">
              <div class="payment-icon">
                <i :class="method.icon"></i>
              </div>
              <div class="payment-info">
                <h3>{{ method.name }}</h3>
                <p>{{ method.description }}</p>
              </div>
              <div class="payment-status">
                <label class="toggle-switch">
                  <input type="checkbox" v-model="method.enabled" />
                  <span class="toggle-slider"></span>
                </label>
              </div>
            </div>
            <div v-if="method.enabled" class="payment-settings">
              <div class="form-group">
                <label>اسم الحساب</label>
                <input type="text" v-model="method.accountName" />
              </div>
              <div class="form-group">
                <label>رقم الحساب</label>
                <input type="text" v-model="method.accountNumber" />
              </div>
              <div class="form-group">
                <label>معلومات إضافية</label>
                <textarea v-model="method.instructions" rows="2"></textarea>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== إعدادات البريد الإلكتروني ===== -->
      <div v-if="activeTab === 'email'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-envelope"></i> إعدادات البريد الإلكتروني</h2>
          <p>إعدادات SMTP وقوالب البريد الإلكتروني</p>
        </div>

        <div class="settings-grid">
          <div class="settings-card">
            <h3>خادم البريد (SMTP)</h3>
            <div class="form-group">
              <label>الخادم</label>
              <input type="text" v-model="settings.email.host" placeholder="smtp.gmail.com" />
            </div>
            <div class="form-group">
              <label>المنفذ</label>
              <input type="number" v-model="settings.email.port" placeholder="587" />
            </div>
            <div class="form-group">
              <label>اسم المستخدم</label>
              <input type="text" v-model="settings.email.username" />
            </div>
            <div class="form-group">
              <label>كلمة المرور</label>
              <input type="password" v-model="settings.email.password" />
            </div>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.email.secure" />
                <span>استخدام SSL/TLS</span>
              </label>
            </div>
          </div>

          <div class="settings-card">
            <h3>البريد المرسل</h3>
            <div class="form-group">
              <label>البريد الإلكتروني</label>
              <input type="email" v-model="settings.email.fromEmail" />
            </div>
            <div class="form-group">
              <label>اسم المرسل</label>
              <input type="text" v-model="settings.email.fromName" placeholder="فينيل آرت" />
            </div>
            <button class="btn-test" @click="testEmail">
              <i class="fa-solid fa-paper-plane"></i> إرسال بريد تجريبي
            </button>
          </div>
        </div>
      </div>

      <!-- ===== إعدادات المستخدمين ===== -->
      <div v-if="activeTab === 'users'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-users-cog"></i> إعدادات المستخدمين</h2>
          <p>صلاحيات المستخدمين وإعدادات التسجيل</p>
        </div>

        <div class="settings-grid">
          <div class="settings-card">
            <h3>التسجيل</h3>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.users.allowRegistration" />
                <span>السماح بتسجيل حسابات جديدة</span>
              </label>
            </div>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.users.emailVerification" />
                <span>تفعيل البريد الإلكتروني</span>
              </label>
            </div>
          </div>

          <div class="settings-card">
            <h3>الصلاحيات الافتراضية</h3>
            <div class="form-group">
              <label>الدور الافتراضي للمستخدمين الجدد</label>
              <select v-model="settings.users.defaultRole">
                <option value="user">مستخدم عادي</option>
                <option value="editor">محرر</option>
                <option value="manager">مسؤول</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== إعدادات واجهة المستخدم ===== -->
      <div v-if="activeTab === 'appearance'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-palette"></i> المظهر</h2>
          <p>تخصيص ألوان وشكل الموقع</p>
        </div>

        <div class="settings-grid">
          <div class="settings-card">
            <h3>الألوان الرئيسية</h3>
            <div class="color-picker-group">
              <div class="color-item">
                <label>اللون الأساسي</label>
                <div class="color-input">
                  <input type="color" v-model="settings.appearance.primaryColor" />
                  <span>{{ settings.appearance.primaryColor }}</span>
                </div>
              </div>
              <div class="color-item">
                <label>اللون الثانوي</label>
                <div class="color-input">
                  <input type="color" v-model="settings.appearance.secondaryColor" />
                  <span>{{ settings.appearance.secondaryColor }}</span>
                </div>
              </div>
              <div class="color-item">
                <label>لون الخلفية</label>
                <div class="color-input">
                  <input type="color" v-model="settings.appearance.backgroundColor" />
                  <span>{{ settings.appearance.backgroundColor }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="settings-card">
            <h3>الوضع الليلي</h3>
            <div class="form-group">
              <label>الوضع الافتراضي</label>
              <select v-model="settings.appearance.defaultTheme">
                <option value="dark">داكن</option>
                <option value="light">فاتح</option>
                <option value="auto">حسب النظام</option>
              </select>
            </div>
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.appearance.allowThemeSwitch" />
                <span>السماح للمستخدمين بتغيير الوضع</span>
              </label>
            </div>
          </div>

          <div class="settings-card">
            <h3>الخطوط</h3>
            <div class="form-group">
              <label>الخط الرئيسي</label>
              <select v-model="settings.appearance.fontFamily">
                <option value="Cairo">Cairo</option>
                <option value="Tajawal">Tajawal</option>
                <option value="Almarai">Almarai</option>
                <option value="Rubik">Rubik</option>
              </select>
            </div>
            <div class="form-group">
              <label>حجم الخط الأساسي</label>
              <input type="number" v-model="settings.appearance.fontSize" min="12" max="24" /> px
            </div>
          </div>
        </div>
      </div>

      <!-- ===== النسخ الاحتياطي ===== -->
      <div v-if="activeTab === 'backup'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-database"></i> النسخ الاحتياطي</h2>
          <p>إدارة نسخ احتياطية للبيانات</p>
        </div>

        <div class="backup-controls">
          <button class="btn-backup" @click="createBackup">
            <i class="fa-solid fa-plus-circle"></i>
            إنشاء نسخة احتياطية جديدة
          </button>
        </div>

        <div class="backup-list">
          <h3>النسخ الاحتياطية المتاحة</h3>
          <table class="backup-table">
            <thead>
              <tr>
                <th>التاريخ</th>
                <th>الحجم</th>
                <th>النوع</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="backup in backups" :key="backup.id">
                <td>{{ backup.date }}</td>
                <td>{{ backup.size }}</td>
                <td>
                  <span class="backup-type" :class="backup.type">
                    {{ backup.type === 'auto' ? 'تلقائي' : 'يدوي' }}
                  </span>
                </td>
                <td class="backup-actions">
                  <button class="backup-btn restore" title="استعادة">
                    <i class="fa-solid fa-undo-alt"></i>
                  </button>
                  <button class="backup-btn download" title="تحميل">
                    <i class="fa-solid fa-download"></i>
                  </button>
                  <button class="backup-btn delete" title="حذف">
                    <i class="fa-solid fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ===== السجل والنشاط ===== -->
      <div v-if="activeTab === 'logs'" class="settings-section">
        <div class="section-header">
          <h2><i class="fa-solid fa-history"></i> سجل النشاط</h2>
          <p>جميع الأنشطة والإجراءات في النظام</p>
        </div>

        <div class="logs-filter">
          <select v-model="logFilter.type">
            <option value="">جميع الأنواع</option>
            <option value="user">مستخدمين</option>
            <option value="product">منتجات</option>
            <option value="order">طلبات</option>
            <option value="setting">إعدادات</option>
          </select>
          <select v-model="logFilter.user">
            <option value="">جميع المستخدمين</option>
            <option value="1">أحمد محمد</option>
            <option value="2">سارة أحمد</option>
          </select>
          <input type="date" v-model="logFilter.date" />
          <button class="btn-filter-logs" @click="filterLogs">
            <i class="fa-solid fa-search"></i> بحث
          </button>
        </div>

        <div class="logs-table-wrapper">
          <table class="logs-table">
            <thead>
              <tr>
                <th>الوقت</th>
                <th>المستخدم</th>
                <th>الإجراء</th>
                <th>التفاصيل</th>
                <th>IP</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in logs" :key="log.id">
                <td>{{ log.time }}</td>
                <td>{{ log.user }}</td>
                <td>
                  <span class="log-action" :class="log.actionType">
                    {{ log.action }}
                  </span>
                </td>
                <td>{{ log.details }}</td>
                <td>{{ log.ip }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- أزرار الحفل في الأسفل -->
    <div class="settings-footer">
      <button class="btn-reset" @click="resetSettings">
        <i class="fa-solid fa-undo-alt"></i>
        إعادة تعيين
      </button>
      <button class="btn-save" @click="saveAllSettings">
        <i class="fa-solid fa-save"></i>
        حفظ التغييرات
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// التبويب النشط
const activeTab = ref('general');

// قائمة التبويبات
const tabs = [
  { id: 'general', name: 'عام', icon: 'fa-solid fa-globe' },
  { id: 'store', name: 'المتجر', icon: 'fa-solid fa-store' },
  { id: 'payment', name: 'الدفع', icon: 'fa-solid fa-credit-card' },
  { id: 'email', name: 'البريد', icon: 'fa-solid fa-envelope' },
  { id: 'users', name: 'المستخدمين', icon: 'fa-solid fa-users-cog' },
  { id: 'appearance', name: 'المظهر', icon: 'fa-solid fa-palette' },
  { id: 'backup', name: 'النسخ الاحتياطي', icon: 'fa-solid fa-database' },
  { id: 'logs', name: 'السجل', icon: 'fa-solid fa-history' },
];

// إعدادات الموقع
const settings = reactive({
  general: {
    siteName: 'فينيل آرت',
    siteDescription: 'متجر متخصص في ملصقات الفينيل للديكور',
    keywords: 'فينيل, ملصقات, ديكور, أثاث, جدران',
    defaultLanguage: 'ar',
    direction: 'rtl',
    logoPreview: '/logo.png',
  },
  store: {
    currency: 'SAR',
    currencySymbol: 'ر.س',
    taxRate: 15,
    taxIncluded: false,
    shippingStandard: 20,
    shippingExpress: 45,
    freeShippingThreshold: 200,
    lowStockThreshold: 10,
    trackInventory: true,
  },
  email: {
    host: 'smtp.gmail.com',
    port: 587,
    username: 'noreply@vinylart.com',
    password: '********',
    secure: true,
    fromEmail: 'noreply@vinylart.com',
    fromName: 'فينيل آرت',
  },
  users: {
    allowRegistration: true,
    emailVerification: true,
    defaultRole: 'user',
  },
  appearance: {
    primaryColor: '#d4af37',
    secondaryColor: '#b8860b',
    backgroundColor: '#0a0a0a',
    defaultTheme: 'dark',
    allowThemeSwitch: true,
    fontFamily: 'Cairo',
    fontSize: 16,
  },
});

// طرق الدفع
const paymentMethods = reactive([
  {
    id: 'cash',
    name: 'الدفع عند الاستلام',
    icon: 'fa-solid fa-money-bill-wave',
    description: 'يدفع العميل عند استلام الطلب',
    enabled: true,
    accountName: '',
    accountNumber: '',
    instructions: 'الدفع نقداً عند استلام الطلب',
  },
  {
    id: 'card',
    name: 'بطاقة ائتمان',
    icon: 'fa-solid fa-credit-card',
    description: 'دفع إلكتروني عبر بطاقة الائتمان',
    enabled: true,
    accountName: 'شركة فينيل آرت',
    accountNumber: '4111 1111 1111 1111',
    instructions: 'بيانات البطاقة محمية بشكل كامل',
  },
  {
    id: 'bank',
    name: 'تحويل بنكي',
    icon: 'fa-solid fa-university',
    description: 'تحويل مباشر إلى الحساب البنكي',
    enabled: false,
    accountName: 'فينيل آرت',
    accountNumber: 'SA123456789012345678',
    instructions: 'يرجى إرسال صورة الإيصال عبر الواتساب',
  },
]);

// فلاتر السجل
const logFilter = reactive({
  type: '',
  user: '',
  date: '',
});

// بيانات النسخ الاحتياطي
const backups = ref([
  { id: 1, date: '2024-03-15 14:30', size: '245 MB', type: 'auto' },
  { id: 2, date: '2024-03-14 10:15', size: '242 MB', type: 'auto' },
  { id: 3, date: '2024-03-13 18:45', size: '240 MB', type: 'manual' },
]);

// سجل النشاط
const logs = ref([
  {
    id: 1,
    time: '2024-03-18 09:15',
    user: 'أحمد محمد',
    action: 'تحديث إعدادات الموقع',
    actionType: 'setting',
    details: 'تم تغيير اسم الموقع',
    ip: '192.168.1.100',
  },
  {
    id: 2,
    time: '2024-03-18 08:30',
    user: 'سارة أحمد',
    action: 'إضافة منتج جديد',
    actionType: 'product',
    details: 'تم إضافة منتج "ملصق وردة حمراء"',
    ip: '192.168.1.101',
  },
  {
    id: 3,
    time: '2024-03-17 16:20',
    user: 'محمد علي',
    action: 'تحديث حالة طلب',
    actionType: 'order',
    details: 'تم تغيير حالة الطلب #ORD-001 إلى مكتمل',
    ip: '192.168.1.102',
  },
]);

// Refs for inputs
const logoInput = ref(null);

// Methods
const triggerLogoUpload = () => {
  logoInput.value.click();
};

const handleLogoUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      settings.general.logoPreview = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const handleFaviconUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    console.log('Favicon uploaded:', file);
  }
};

const saveAllSettings = () => {
  console.log('Saving all settings:', settings);
  alert('✅ تم حفظ جميع الإعدادات بنجاح');
};

const resetSettings = () => {
  if (confirm('هل أنت متأكد من إعادة تعيين جميع الإعدادات؟')) {
    console.log('Settings reset');
    alert('تم إعادة تعيين الإعدادات');
  }
};

const testEmail = () => {
  console.log('Testing email with settings:', settings.email);
  alert('تم إرسال بريد تجريبي بنجاح');
};

const createBackup = () => {
  console.log('Creating backup...');
  alert('جاري إنشاء نسخة احتياطية...');
};

const filterLogs = () => {
  console.log('Filtering logs with:', logFilter);
};
</script>

<style scoped>
@import '@/assets/theme.css';

.settings-manager {
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

/* ===== رأس الصفحة ===== */
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

.btn-save-header {
  padding: 14px 28px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  border-radius: 16px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition-smooth);
}

.btn-save-header:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== تبويبات الإعدادات ===== */
.settings-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 25px;
  background: var(--bg-card);
  padding: 15px;
  border-radius: 20px;
  border: 1px solid var(--border-light);
}

.tab-btn {
  padding: 12px 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.tab-btn i {
  color: var(--gold-1);
  transition: var(--transition-smooth);
}

.tab-btn:hover {
  background: var(--bg-card);
  color: var(--gold-1);
  transform: translateY(-2px);
}

.tab-btn.active {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.tab-btn.active i {
  color: var(--bg-deep);
}

/* ===== محتوى الإعدادات ===== */
.settings-content {
  background: var(--bg-card);
  border-radius: 24px;
  border: 1px solid var(--border-light);
  padding: 30px;
  margin-bottom: 25px;
}

.section-header {
  margin-bottom: 25px;
}

.section-header h2 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header h2 i {
  color: var(--gold-1);
}

.section-header p {
  color: var(--text-dim);
  font-size: 0.95rem;
}

/* ===== شبكة الإعدادات ===== */
.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
}

.settings-card {
  background: var(--bg-primary);
  border-radius: 20px;
  padding: 25px;
  border: 1px solid var(--border-light);
  transition: var(--transition-smooth);
}

.settings-card:hover {
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.settings-card h3 {
  color: var(--gold-1);
  font-size: 1.1rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-light);
}

/* ===== عناصر النموذج ===== */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  color: var(--text-dim);
  margin-bottom: 5px;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: var(--transition-smooth);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
}

.input-hint {
  display: block;
  margin-top: 5px;
  color: var(--text-dim);
  font-size: 0.8rem;
}

/* ===== حقول الاختيار ===== */
.checkbox-group {
  margin: 10px 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-secondary);
}

.checkbox-label input[type='checkbox'] {
  width: 18px;
  height: 18px;
  accent-color: var(--gold-1);
}

/* ===== رفع الشعار ===== */
.logo-upload {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.logo-preview {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid var(--gold-1);
}

.logo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-controls {
  flex: 1;
}

.btn-upload {
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--gold-1);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-upload:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

.upload-hint {
  color: var(--text-dim);
  font-size: 0.8rem;
  margin-top: 5px;
}

.favicon-upload {
  margin-top: 15px;
}

.favicon-upload label {
  display: block;
  color: var(--text-dim);
  margin-bottom: 8px;
}

.favicon-upload input {
  width: 100%;
  padding: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: white;
}

/* ===== طرق الدفع ===== */
.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.payment-card {
  background: var(--bg-primary);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--border-light);
}

.payment-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.payment-icon {
  width: 50px;
  height: 50px;
  background: var(--bg-card);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--gold-1);
}

.payment-info {
  flex: 1;
}

.payment-info h3 {
  color: white;
  font-size: 1rem;
  margin-bottom: 3px;
}

.payment-info p {
  color: var(--text-dim);
  font-size: 0.85rem;
}

.payment-settings {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

/* ===== Toggle Switch ===== */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-light);
  transition: 0.3s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: '';
  height: 20px;
  width: 20px;
  right: 3px;
  bottom: 2px;
  background-color: var(--text-dim);
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--gold-gradient);
}

input:checked + .toggle-slider:before {
  transform: translateX(-24px);
  background-color: var(--bg-deep);
}

/* ===== ألوان ===== */
.color-picker-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-item label {
  width: 100px;
  color: var(--text-dim);
}

.color-input {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-input input[type='color'] {
  width: 50px;
  height: 40px;
  border: 1px solid var(--border-light);
  border-radius: 10px;
  background: var(--bg-card);
  cursor: pointer;
}

.color-input span {
  color: var(--text-secondary);
  font-family: monospace;
}

/* ===== النسخ الاحتياطي ===== */
.btn-backup {
  padding: 15px 30px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 25px;
  transition: var(--transition-smooth);
}

.btn-backup:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

.backup-list h3 {
  color: white;
  margin-bottom: 15px;
}

.backup-table {
  width: 100%;
  border-collapse: collapse;
}

.backup-table th {
  text-align: right;
  padding: 12px;
  color: var(--text-dim);
  font-weight: 600;
  border-bottom: 1px solid var(--border-light);
}

.backup-table td {
  padding: 12px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.backup-type {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.backup-type.auto {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
}

.backup-type.manual {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.backup-actions {
  display: flex;
  gap: 8px;
}

.backup-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition-smooth);
  background: var(--bg-primary);
  color: var(--text-dim);
}

.backup-btn.restore:hover {
  background: #2196f3;
  color: white;
}

.backup-btn.download:hover {
  background: #4caf50;
  color: white;
}

.backup-btn.delete:hover {
  background: var(--danger);
  color: white;
}

/* ===== سجل النشاط ===== */
.logs-filter {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.logs-filter select,
.logs-filter input {
  flex: 1;
  min-width: 150px;
  padding: 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: white;
}

.btn-filter-logs {
  padding: 12px 24px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
}

.btn-filter-logs:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.logs-table-wrapper {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th {
  text-align: right;
  padding: 15px;
  color: var(--text-dim);
  font-weight: 600;
  border-bottom: 2px solid var(--border-light);
}

.logs-table td {
  padding: 12px 15px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}

.log-action {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.log-action.user {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
}
.log-action.product {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}
.log-action.order {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}
.log-action.setting {
  background: rgba(156, 39, 176, 0.2);
  color: #9c27b0;
}

/* ===== الفوتر ===== */
.settings-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.btn-reset,
.btn-save {
  padding: 14px 32px;
  border: none;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition-smooth);
}

.btn-reset {
  background: var(--bg-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-save {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

.btn-reset:hover,
.btn-save:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== اختبار البريد ===== */
.btn-test {
  padding: 12px 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--gold-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition-smooth);
  margin-top: 15px;
}

.btn-test:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
}

/* ===== استجابة ===== */
@media (max-width: 992px) {
  .settings-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
  }

  .tab-btn {
    white-space: nowrap;
  }

  .logs-filter {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .settings-grid {
    grid-template-columns: 1fr;
  }

  .logo-upload {
    flex-direction: column;
    text-align: center;
  }

  .settings-footer {
    flex-direction: column;
  }

  .btn-reset,
  .btn-save {
    width: 100%;
    justify-content: center;
  }
}
</style>
