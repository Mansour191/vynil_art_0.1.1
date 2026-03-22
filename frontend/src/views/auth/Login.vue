<template>
  <div class="login-page">
    <div class="bg-effects">
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
      <div class="gradient-overlay"></div>
    </div>

    <div class="auth-container">
      <div class="glass-card">
        <div class="auth-header">
          <div class="logo-section">
            <div class="logo-icon">
              <i class="fa-solid fa-user-circle"></i>
            </div>
            <h3 class="login-header-title">
              {{ $t('loginTitle') }}
            </h3>
            <p class="auth-subtitle">مرحباً بعودتك! سجل الدخول لحسابك</p>
          </div>
        </div>

        <div class="auth-body">
          <!-- رسائل الخطأ -->
          <div v-if="error" class="message error-message">
            <div class="message-icon">
              <i class="fa-solid fa-exclamation-triangle"></i>
            </div>
            <div class="message-content">
              <span class="message-title">خطأ في تسجيل الدخول</span>
              <span class="message-text">{{ error }}</span>
            </div>
          </div>

          <!-- رسالة تحذيرية إذا كان يحاول الوصول لصفحة محمية -->
          <div v-if="isAttemptingProtected" class="message warning-message">
            <div class="message-icon">
              <i class="fa-solid fa-shield-alt"></i>
            </div>
            <div class="message-content">
              <span class="message-title">وصول غير مصرح به</span>
              <span class="message-text">
                هذه الصفحة محمية. يرجى تسجيل الدخول باستخدام حساب مصرح به.
              </span>
            </div>
          </div>

          <!-- نموذج تسجيل الدخول -->
          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-envelope label-icon"></i>
                <span>اسم المستخدم</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  v-model="form.email" 
                  class="form-input"
                  placeholder="أدخل اسم المستخدم"
                  required 
                  autocomplete="username"
                />
                <div class="input-border"></div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-lock label-icon"></i>
                <span>كلمة المرور</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="password" 
                  v-model="form.password" 
                  class="form-input"
                  placeholder="أدخل كلمة المرور"
                  required 
                  autocomplete="current-password"
                />
                <div class="input-border"></div>
              </div>
            </div>

            <div class="form-options">
              <router-link to="/forgot-password" class="forgot-link">
                نسيت كلمة المرور؟
              </router-link>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span class="btn-content">
                <i class="fa-solid fa-sign-in-alt btn-icon"></i>
                <span v-if="!loading">تسجيل الدخول</span>
                <span v-else class="loading-text">
                  <i class="fa-solid fa-spinner fa-spin"></i>
                  جاري تسجيل الدخول...
                </span>
              </span>
              <div class="btn-glow"></div>
            </button>
          </form>

          <!-- ✅ auth-footer - يظهر فقط إذا لم يكن يحاول الوصول لصفحة محمية -->
          <div v-if="!isAttemptingProtected" class="auth-footer">
            <p class="footer-text">ليس لديك حساب؟</p>
            <router-link to="/register" class="footer-link">
              <span>إنشاء حساب جديد</span>
              <i class="fa-solid fa-arrow-left"></i>
            </router-link>
          </div>
          
          <!-- ✅ معلومات تجريبية للاختبار -->
          <div class="demo-info">
            <div class="demo-card">
              <i class="fa-solid fa-flask"></i>
              <div>
                <strong>بيانات تجريبية:</strong><br>
                <span>مدير: admin / admin</span><br>
                <span>ممول: investor / investor</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const { t } = useI18n();

const form = reactive({
  email: '',
  password: '',
});

const loading = ref(false);
const error = ref(null);

// ✅ التحقق مما إذا كان المستخدم يحاول الوصول لصفحة محمية
const isAttemptingProtected = computed(() => {
  const redirect = route.query.redirect;
  return redirect === '/dashboard' || 
         redirect === '/investor' ||
         (redirect && (redirect.startsWith('/dashboard') || redirect.startsWith('/investor')));
});

const handleLogin = async () => {
  loading.value = true;
  error.value = null;
  try {
    const result = await authStore.login(form.email, form.password);
    
    if (result.success) {
      // ✅ التوجيه حسب الدور أو حسب redirect المطلوب
      const redirectPath = route.query.redirect;
      
      if (redirectPath && (redirectPath === '/dashboard' || redirectPath === '/investor')) {
        // إذا كان يحاول الوصول لصفحة محمية، نتحقق من صلاحياته
        if (result.role === 'admin' && redirectPath === '/dashboard') {
          router.push('/dashboard');
        } else if (result.role === 'investor' && redirectPath === '/investor') {
          router.push('/investor');
        } else {
          // إذا لم يكن لديه الصلاحية، نوجه للصفحة الرئيسية
          error.value = 'لا تمتلك الصلاحية للوصول إلى هذه الصفحة';
          router.push('/');
        }
      } else if (result.role === 'admin') {
        router.push('/dashboard');
      } else if (result.role === 'investor') {
        router.push('/investor');
      } else {
        router.push('/');
      }
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

// ✅ إضافة رسالة تحذيرية في console
onMounted(() => {
  if (isAttemptingProtected.value) {
    console.warn('⚠️ محاولة الوصول لصفحة محمية:', route.query.redirect);
  }
});
</script>

<style scoped>
/* إضافة تنسيق للرسالة التحذيرية */
.warning-message {
  background: rgba(255, 152, 0, 0.1);
  border-color: rgba(255, 152, 0, 0.3);
  color: #ff9800;
}

.warning-message .message-icon {
  background: rgba(255, 152, 0, 0.2);
}

/* باقي التنسيقات كما هي */
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

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

.auth-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 480px;
  padding: 20px;
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

.logo-section {
  text-align: center;
  margin-bottom: 35px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #0f0f0f;
  margin: 0 auto 20px;
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.login-header-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #d4af37 50%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.95rem;
  margin-top: 8px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  border: 1px solid;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-message {
  background: rgba(255, 82, 82, 0.1);
  border-color: rgba(255, 82, 82, 0.3);
  color: #ff5252;
}

.message-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.error-message .message-icon {
  background: rgba(255, 82, 82, 0.2);
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.message-text {
  font-size: 0.85rem;
  opacity: 0.8;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
  font-weight: 500;
}

.label-icon {
  color: #d4af37;
  font-size: 0.85rem;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #d4af37, #f4e4c1);
  transition: width 0.3s ease;
  border-radius: 1px;
}

.form-input:focus ~ .input-border {
  width: 100%;
}

.form-options {
  display: flex;
  justify-content: center;
  margin-top: 8px;
}

.forgot-link {
  color: #d4af37;
  text-decoration: none;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.forgot-link:hover {
  color: #f4e4c1;
  text-decoration: underline;
}

.submit-btn {
  position: relative;
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 12px;
  color: #0f0f0f;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  margin-top: 8px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(212, 175, 55, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.submit-btn:hover .btn-glow {
  left: 100%;
}

/* ✅ auth-footer - سيتم إخفاؤه تلقائياً عند محاولة الوصول لصفحة محمية */
.auth-footer {
  margin-top: 32px;
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-text {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.9rem;
  margin: 0 0 12px 0;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #d4af37;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.footer-link:hover {
  color: #f4e4c1;
  transform: translateX(-4px);
}

.demo-info {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

.demo-card {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 12px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.85rem;
  color: #d4af37;
}

.demo-card i {
  font-size: 1.2rem;
}

@media (max-width: 640px) {
  .auth-container {
    padding: 16px;
  }
  
  .glass-card {
    padding: 32px 24px;
  }
  
  .login-header-title {
    font-size: 1.75rem;
  }
}
</style>
