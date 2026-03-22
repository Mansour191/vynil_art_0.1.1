<template>
  <div class="settings-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="settings-container">
      <div class="glass-card">
        <!-- Header -->
        <div class="settings-header">
          <div class="header-content">
            <h1 class="page-title">
              <i class="fa-solid fa-cog"></i>
              الإعدادات
            </h1>
            <p class="page-subtitle">إدارة حسابك وتفضيلاتك</p>
          </div>
        </div>

        <!-- Settings Navigation -->
        <div class="settings-nav">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['nav-btn', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Profile Settings -->
          <div v-if="activeTab === 'profile'" class="tab-panel">
            <div class="settings-section">
              <h2 class="section-title">معلومات الحساب</h2>
              <form @submit.prevent="updateProfile" class="settings-form">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">الاسم الأول</label>
                    <input 
                      type="text" 
                      v-model="profileForm.firstName" 
                      class="form-input"
                      placeholder="أدخل اسمك الأول"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label class="form-label">الاسم الأخير</label>
                    <input 
                      type="text" 
                      v-model="profileForm.lastName" 
                      class="form-input"
                      placeholder="أدخل اسمك الأخير"
                    />
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">البريد الإلكتروني</label>
                  <input 
                    type="email" 
                    v-model="profileForm.email" 
                    class="form-input"
                    placeholder="أدخل بريدك الإلكتروني"
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">رقم الهاتف</label>
                  <input 
                    type="tel" 
                    v-model="profileForm.phone" 
                    class="form-input"
                    placeholder="أدخل رقم هاتفك"
                  />
                </div>
                <div class="form-actions">
                  <button type="submit" class="save-btn" :disabled="loading">
                    <i class="fa-solid fa-save"></i>
                    <span v-if="!loading">حفظ التغييرات</span>
                    <span v-else class="loading-text">
                      <i class="fa-solid fa-spinner fa-spin"></i>
                      جاري الحفظ...
                    </span>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Security Settings -->
          <div v-if="activeTab === 'security'" class="tab-panel">
            <div class="settings-section">
              <h2 class="section-title">تغيير كلمة المرور</h2>
              <form @submit.prevent="changePassword" class="settings-form">
                <div class="form-group">
                  <label class="form-label">كلمة المرور الحالية</label>
                  <input 
                    type="password" 
                    v-model="passwordForm.oldPassword" 
                    class="form-input"
                    placeholder="أدخل كلمة المرور الحالية"
                    required
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">كلمة المرور الجديدة</label>
                  <input 
                    type="password" 
                    v-model="passwordForm.newPassword" 
                    class="form-input"
                    placeholder="أدخل كلمة المرور الجديدة"
                    required
                  />
                  <div class="password-strength" v-if="passwordForm.newPassword">
                    <div class="strength-bars">
                      <div 
                        v-for="n in 4" 
                        :key="n" 
                        :class="['strength-bar', { active: n <= passwordStrength.score }]"
                      ></div>
                    </div>
                    <span class="strength-text">{{ passwordStrength.text }}</span>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">تأكيد كلمة المرور الجديدة</label>
                  <input 
                    type="password" 
                    v-model="passwordForm.confirmPassword" 
                    class="form-input"
                    placeholder="أعد إدخال كلمة المرور الجديدة"
                    required
                  />
                </div>
                <div class="form-actions">
                  <button type="submit" class="save-btn" :disabled="loading">
                    <i class="fa-solid fa-lock"></i>
                    <span v-if="!loading">تغيير كلمة المرور</span>
                    <span v-else class="loading-text">
                      <i class="fa-solid fa-spinner fa-spin"></i>
                      جاري التغيير...
                    </span>
                  </button>
                </div>
              </form>
            </div>

            <div class="settings-section">
              <h2 class="section-title">الأمان</h2>
              <div class="security-options">
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">المصادقة الثنائية</h3>
                    <p class="option-description">إضافة طبقة أمان إضافية لحسابك</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="securitySettings.twoFactor" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">تسجيل الخروج التلقائي</h3>
                    <p class="option-description">تسجيل الخروج تلقائياً بعد فترة من عدم النشاط</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="securitySettings.autoLogout" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Notification Settings -->
          <div v-if="activeTab === 'notifications'" class="tab-panel">
            <div class="settings-section">
              <h2 class="section-title">إعدادات الإشعارات</h2>
              <div class="notification-options">
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">الإشعارات عبر البريد الإلكتروني</h3>
                    <p class="option-description">استلام الإشعارات الهامة عبر البريد الإلكتروني</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="notificationSettings.email" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">الإشعارات عبر الرسائل النصية</h3>
                    <p class="option-description">استلام الإشعارات الهامة عبر الرسائل النصية</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="notificationSettings.sms" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">الإشعارات الفورية</h3>
                    <p class="option-description">استلام الإشعارات الفورية في المتصفح</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="notificationSettings.push" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">نشرات المنتجات</h3>
                    <p class="option-description">إشعارات حول المنتجات الجديدة والعروض</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="notificationSettings.marketing" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Privacy Settings -->
          <div v-if="activeTab === 'privacy'" class="tab-panel">
            <div class="settings-section">
              <h2 class="section-title">الخصوصية</h2>
              <div class="privacy-options">
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">الملف الشخصي العام</h3>
                    <p class="option-description">جعل ملفك الشخصي مرئياً للجميع</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="privacySettings.publicProfile" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">إظهار النشاط</h3>
                    <p class="option-description">إظهار نشاطك الأخير للآخرين</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="privacySettings.showActivity" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
                <div class="option-item">
                  <div class="option-info">
                    <h3 class="option-title">البحث عني</h3>
                    <p class="option-description">السماح للآخرين بالعثور عنك عبر البحث</p>
                  </div>
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="privacySettings.allowSearch" />
                    <span class="toggle-slider"></span>
                  </label>
                </div>
              </div>
            </div>

            <div class="settings-section">
              <h2 class="section-title">حذف الحساب</h2>
              <div class="danger-zone">
                <p class="danger-text">
                  حذف حسابك سيزيل جميع بياناتك بشكل دائم. هذا الإجراء لا يمكن التراجع عنه.
                </p>
                <button class="danger-btn" @click="confirmDeleteAccount">
                  <i class="fa-solid fa-trash"></i>
                  حذف الحساب
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" :class="['message-toast', message.type]">
      <div class="message-icon">
        <i :class="message.type === 'success' ? 'fa-solid fa-check-circle' : 'fa-solid fa-exclamation-circle'"></i>
      </div>
      <div class="message-content">
        <span class="message-text">{{ message.text }}</span>
      </div>
      <button class="message-close" @click="clearMessage">
        <i class="fa-solid fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

const activeTab = ref('profile');
const loading = ref(false);
const message = ref(null);

const tabs = [
  { id: 'profile', label: 'الملف الشخصي', icon: 'fa-solid fa-user' },
  { id: 'security', label: 'الأمان', icon: 'fa-solid fa-shield-alt' },
  { id: 'notifications', label: 'الإشعارات', icon: 'fa-solid fa-bell' },
  { id: 'privacy', label: 'الخصوصية', icon: 'fa-solid fa-lock' }
];

const profileForm = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: ''
});

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
});

const passwordStrength = reactive({
  score: 0,
  text: ''
});

const securitySettings = reactive({
  twoFactor: false,
  autoLogout: false
});

const notificationSettings = reactive({
  email: true,
  sms: false,
  push: true,
  marketing: false
});

const privacySettings = reactive({
  publicProfile: false,
  showActivity: true,
  allowSearch: true
});

// Password strength checker
const checkPasswordStrength = () => {
  const password = passwordForm.newPassword;
  if (!password) {
    passwordStrength.score = 0;
    passwordStrength.text = '';
    return;
  }

  let score = 0;
  if (password.length >= 8) score++;
  if (password.match(/[a-z]/) && password.match(/[A-Z]/)) score++;
  if (password.match(/[0-9]/)) score++;
  if (password.match(/[^a-zA-Z0-9]/)) score++;

  passwordStrength.score = score;

  const strengthTexts = {
    0: 'ضعيف جداً',
    1: 'ضعيف',
    2: 'متوسط',
    3: 'قوي',
    4: 'قوي جداً'
  };
  passwordStrength.text = strengthTexts[score];
};

// Watch password changes
import { watch } from 'vue';
watch(() => passwordForm.newPassword, checkPasswordStrength);

const updateProfile = async () => {
  try {
    loading.value = true;
    
    await authStore.updateProfile(profileForm);
    
    showMessage('تم تحديث الملف الشخصي بنجاح', 'success');
  } catch (error) {
    showMessage(error.message || 'فشل تحديث الملف الشخصي', 'error');
  } finally {
    loading.value = false;
  }
};

const changePassword = async () => {
  try {
    loading.value = true;
    
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      showMessage('كلمات المرور الجديدة غير متطابقة', 'error');
      return;
    }
    
    await authStore.changePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword,
      passwordForm.confirmPassword
    );
    
    showMessage('تم تغيير كلمة المرور بنجاح', 'success');
    
    // Clear form
    passwordForm.oldPassword = '';
    passwordForm.newPassword = '';
    passwordForm.confirmPassword = '';
  } catch (error) {
    showMessage(error.message || 'فشل تغيير كلمة المرور', 'error');
  } finally {
    loading.value = false;
  }
};

const confirmDeleteAccount = () => {
  if (confirm('هل أنت متأكد من حذف حسابك؟ هذا الإجراء لا يمكن التراجع عنه.')) {
    // TODO: Implement delete account functionality
    showMessage('سيتم تنفيذ حذف الحساب قريباً', 'info');
  }
};

const showMessage = (text, type) => {
  message.value = { text, type };
  setTimeout(() => {
    message.value = null;
  }, 5000);
};

const clearMessage = () => {
  message.value = null;
};

const loadUserData = () => {
  if (authStore.user) {
    profileForm.firstName = authStore.user.firstName || '';
    profileForm.lastName = authStore.user.lastName || '';
    profileForm.email = authStore.user.email || '';
    profileForm.phone = authStore.user.phone || '';
  }
};

onMounted(() => {
  loadUserData();
});
</script>

<style scoped>
/* ===== Settings Page ===== */
.settings-page {
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

/* Settings Container */
.settings-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 900px;
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
.settings-header {
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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

/* Settings Navigation */
.settings-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 10px;
  overflow-x: auto;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: transparent;
  border: none;
  border-radius: 8px 8px 0 0;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.nav-btn.active {
  color: #d4af37;
  background: rgba(212, 175, 55, 0.1);
}

.nav-btn i {
  font-size: 16px;
}

/* Tab Content */
.tab-content {
  min-height: 400px;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Settings Sections */
.settings-section {
  margin-bottom: 40px;
}

.section-title {
  color: #ffffff;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 24px 0;
}

/* Forms */
.settings-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(212, 175, 55, 0.5);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

/* Password Strength */
.password-strength {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.strength-bars {
  display: flex;
  gap: 4px;
}

.strength-bar {
  width: 40px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-bar.active:nth-child(1) {
  background: #dc3545;
}

.strength-bar.active:nth-child(2) {
  background: #ffc107;
}

.strength-bar.active:nth-child(3) {
  background: #007bff;
}

.strength-bar.active:nth-child(4) {
  background: #28a745;
}

.strength-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Options */
.security-options,
.notification-options,
.privacy-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.option-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.option-info {
  flex: 1;
}

.option-title {
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.option-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 30px;
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
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: 0.4s;
  border-radius: 30px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 4px;
  bottom: 3px;
  background: rgba(255, 255, 255, 0.7);
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background: rgba(212, 175, 55, 0.3);
  border-color: rgba(212, 175, 55, 0.5);
}

input:checked + .toggle-slider:before {
  transform: translateX(30px);
  background: #d4af37;
}

/* Danger Zone */
.danger-zone {
  padding: 24px;
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
  border-radius: 12px;
}

.danger-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.danger-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(220, 53, 69, 0.2);
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 8px;
  color: #dc3545;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.danger-btn:hover {
  background: rgba(220, 53, 69, 0.3);
  color: #ffffff;
}

/* Message Toast */
.message-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.message-toast.success {
  background: rgba(40, 167, 69, 0.9);
  color: #ffffff;
}

.message-toast.error {
  background: rgba(220, 53, 69, 0.9);
  color: #ffffff;
}

.message-toast.info {
  background: rgba(0, 123, 255, 0.9);
  color: #ffffff;
}

.message-icon {
  font-size: 20px;
}

.message-content {
  flex: 1;
}

.message-text {
  font-weight: 500;
}

.message-close {
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.message-close:hover {
  opacity: 1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .settings-page {
    padding: 10px;
  }
  
  .glass-card {
    padding: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .settings-nav {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .nav-btn {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .option-item {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .save-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
