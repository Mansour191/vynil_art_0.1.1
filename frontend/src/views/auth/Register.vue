// @\views\auth\Register.vue
<template>
  <div class="register-page">
    <!-- Background Effects -->
    <div class="bg-effects">
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
      <div class="gradient-overlay"></div>
    </div>

    <!-- Main Container -->
    <div class="auth-container">
      <!-- Glass Effect Card -->
      <div class="glass-card">
        <div class="auth-header">
          <div class="logo-section">
            <div class="logo-icon">
              <i class="fa-solid fa-user-plus"></i>
            </div>
            <h3 class="register-header-title">
              {{ $t('signupTitle') }}
            </h3>
            <p class="auth-subtitle">أنشئ حساب جديد وابدأ رحلتك معنا</p>
          </div>
        </div>

        <div class="auth-body">
          <!-- Error/Success Messages -->
          <div v-if="error" class="message error-message">
            <div class="message-icon">
              <i class="fa-solid fa-exclamation-triangle"></i>
            </div>
            <div class="message-content">
              <span class="message-title">خطأ في إنشاء الحساب</span>
              <span class="message-text">{{ error }}</span>
            </div>
          </div>

          <div v-if="success" class="message success-message">
            <div class="message-icon">
              <i class="fa-solid fa-check-circle"></i>
            </div>
            <div class="message-content">
              <span class="message-title">تم إنشاء الحساب!</span>
              <span class="message-text">{{ success }}</span>
            </div>
          </div>

          <!-- Social Signup -->
          <div class="social-section">
            <p class="social-label">سجل بسرعة باستخدام</p>
            <div class="social-buttons">
              <button
                class="social-btn google"
                @click="signupWithSocial('google')"
                :disabled="loading"
                type="button"
              >
                <div class="social-icon">
                  <i class="fab fa-google"></i>
                </div>
                <span class="social-text">Google</span>
                <div class="social-hover"></div>
              </button>

              <button
                class="social-btn facebook"
                @click="signupWithSocial('facebook')"
                :disabled="loading"
                type="button"
              >
                <div class="social-icon">
                  <i class="fab fa-facebook-f"></i>
                </div>
                <span class="social-text">Facebook</span>
                <div class="social-hover"></div>
              </button>

              <button
                class="social-btn microsoft"
                @click="signupWithSocial('microsoft')"
                :disabled="loading"
                type="button"
              >
                <div class="social-icon">
                  <i class="fab fa-microsoft"></i>
                </div>
                <span class="social-text">Microsoft</span>
                <div class="social-hover"></div>
              </button>
            </div>
          </div>

          <div class="divider">
            <span class="divider-text">أو سجل باستخدام البريد الإلكتروني</span>
          </div>

          <!-- Registration Form -->
          <form @submit.prevent="handleSignup" v-if="!loading" class="auth-form">
            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-user label-icon"></i>
                <span>الاسم الكامل</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  v-model="form.name" 
                  class="form-input"
                  placeholder="أدخل اسمك الكامل"
                  required 
                  autocomplete="name"
                />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- Contact Method Toggle -->
            <div class="contact-method-toggle">
              <label class="toggle-label">
                <span class="toggle-text">طريقة التواصل</span>
                <div class="toggle-switch">
                  <input 
                    type="radio" 
                    v-model="form.contactMethod" 
                    value="email" 
                    class="toggle-input"
                    id="contact-email"
                  />
                  <label for="contact-email" class="toggle-option">
                    <i class="fa-solid fa-envelope"></i>
                    <span>البريد الإلكتروني</span>
                  </label>
                  <input 
                    type="radio" 
                    v-model="form.contactMethod" 
                    value="phone" 
                    class="toggle-input"
                    id="contact-phone"
                  />
                  <label for="contact-phone" class="toggle-option">
                    <i class="fa-solid fa-phone"></i>
                    <span>رقم الهاتف</span>
                  </label>
                </div>
              </label>
            </div>

            <div class="form-group" v-if="form.contactMethod === 'email'">
              <label class="form-label">
                <i class="fa-solid fa-envelope label-icon"></i>
                <span>البريد الإلكتروني</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="email" 
                  v-model="form.email" 
                  class="form-input"
                  placeholder="أدخل بريدك الإلكتروني"
                  required 
                  autocomplete="email"
                />
                <div class="input-border"></div>
              </div>
            </div>

            <div class="form-group" v-if="form.contactMethod === 'phone'">
              <label class="form-label">
                <i class="fa-solid fa-phone label-icon"></i>
                <span>رقم الهاتف</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="tel" 
                  v-model="form.phone" 
                  class="form-input"
                  placeholder="أدخل رقم هاتفك"
                  required 
                  autocomplete="tel"
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
                  autocomplete="new-password"
                  @input="checkPasswordStrength"
                />
                <div class="input-border"></div>
              </div>
              <!-- Password Strength Indicator -->
              <div v-if="form.password" class="password-strength">
                <div class="strength-header">
                  <span class="strength-label">قوة كلمة المرور</span>
                  <span class="strength-text">{{ passwordStrength.text }}</span>
                </div>
                <div class="strength-bars">
                  <div
                    v-for="n in 4"
                    :key="n"
                    class="strength-bar"
                    :class="{
                      active: n <= passwordStrength.score,
                      weak: passwordStrength.score <= 1,
                      medium: passwordStrength.score === 2,
                      strong: passwordStrength.score >= 3,
                    }"
                  ></div>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-lock label-icon"></i>
                <span>تأكيد كلمة المرور</span>
              </label>
              <div class="input-wrapper">
                <input
                  type="password"
                  v-model="form.confirmPassword"
                  class="form-input"
                  placeholder="أعد إدخال كلمة المرور"
                  required
                  autocomplete="new-password"
                />
                <div class="input-border"></div>
              </div>
              <div
                v-if="form.password && form.confirmPassword && form.password !== form.confirmPassword"
                class="error-text"
              >
                كلمات المرور غير متطابقة
              </div>
            </div>

            <!-- Terms Agreement -->
            <div class="form-options">
              <label class="checkbox-wrapper">
                <input type="checkbox" v-model="form.acceptTerms" class="checkbox-input" required />
                <span class="checkbox-text">أوافق على الشروط والأحكام</span>
              </label>
              <a href="/terms" target="_blank" class="terms-link">عرض الشروط</a>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading || !isFormValid">
              <span class="btn-content">
                <i class="fa-solid fa-user-plus btn-icon"></i>
                <span v-if="!loading">إنشاء حساب جديد</span>
                <span v-else class="loading-text">
                  <i class="fa-solid fa-spinner fa-spin"></i>
                  جاري إنشاء الحساب...
                </span>
              </span>
              <div class="btn-glow"></div>
            </button>
          </form>

          <!-- Footer -->
          <div class="auth-footer">
            <p class="footer-text">لديك حساب بالفعل؟</p>
            <router-link to="/login" class="footer-link">
              <span>سجل الدخول</span>
              <i class="fa-solid fa-arrow-left"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import zxcvbn from 'zxcvbn';

const authStore = useAuthStore();
const router = useRouter();
const { t } = useI18n();

const form = reactive({
  name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
  contactMethod: 'email', // 'email' or 'phone'
});

const passwordStrength = reactive({
  score: 0,
  text: '',
});

const loading = ref(false);
const error = ref(null);
const success = ref(null);

const isFormValid = computed(() => {
  return (
    form.name &&
    (form.contactMethod === 'email' ? form.email : form.phone) &&
    form.password &&
    form.confirmPassword &&
    form.password === form.confirmPassword &&
    form.acceptTerms &&
    form.password.length >= 8
  );
});

const checkPasswordStrength = () => {
  if (form.password) {
    const result = zxcvbn(form.password);
    passwordStrength.score = result.score;

    const strengthTexts = {
      0: t('weak'),
      1: t('weak'),
      2: t('medium'),
      3: t('strong'),
      4: t('veryStrong'),
    };
    passwordStrength.text = strengthTexts[result.score];
  } else {
    passwordStrength.score = 0;
    passwordStrength.text = '';
  }
};

const signupWithSocial = async (platform) => {
  loading.value = true;
  error.value = null;
  
  try {
    // Mock social login - replace with actual implementation
    switch(platform) {
      case 'google':
        // TODO: Implement Google OAuth
        error.value = 'سيتم تفعيل تسجيل الدخول بـ Google قريباً';
        break;
      case 'facebook':
        // TODO: Implement Facebook OAuth
        error.value = 'سيتم تفعيل تسجيل الدخول بـ Facebook قريباً';
        break;
      case 'microsoft':
        // TODO: Implement Microsoft OAuth
        error.value = 'سيتم تفعيل تسجيل الدخول بـ Microsoft قريباً';
        break;
      default:
        error.value = 'منصة غير مدعومة';
    }
  } catch (err) {
    error.value = err.message || 'فشل تسجيل الدخول';
  } finally {
    loading.value = false;
  }
};

const handleSignup = async () => {
  if (!isFormValid.value) return;

  if (form.password !== form.confirmPassword) {
    error.value = t('passwordsDoNotMatch');
    return;
  }

  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    // Use GraphQL registration instead of Firebase
    const userData = {
      username: form.contactMethod === 'email' ? form.email.split('@')[0] : form.phone,
      email: form.contactMethod === 'email' ? form.email : '',
      phone: form.contactMethod === 'phone' ? form.phone : '',
      password: form.password,
      firstName: form.name,
      lastName: ''
    };
    
    const result = await authStore.register(userData);
    
    if (result.success) {
      success.value = 'تم إنشاء الحساب بنجاح!';
      
      // Auto-login after successful registration
      await authStore.login(userData.username, userData.password);
      
      setTimeout(() => {
        router.push('/dashboard');
      }, 1000);
    } else {
      error.value = result.error || 'فشل إنشاء الحساب';
    }
  } catch (err) {
    error.value = err.message || 'فشل إنشاء الحساب';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Contact Method Toggle */
.contact-method-toggle {
  margin-bottom: 24px;
}

.toggle-label {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toggle-text {
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
}

.toggle-switch {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 4px;
  position: relative;
}

.toggle-input {
  display: none;
}

.toggle-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
}

.toggle-option i {
  font-size: 16px;
}

.toggle-input:checked + .toggle-option {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.toggle-option:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

.toggle-input:checked + .toggle-option:hover {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
}
.register-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
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

/* Main Container */
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

/* Header Section */
.auth-header {
  text-align: center;
  margin-bottom: 35px;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
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
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3),
              0 0 60px rgba(212, 175, 55, 0.2);
  position: relative;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3), 0 0 60px rgba(212, 175, 55, 0.2); }
  50% { transform: scale(1.05); box-shadow: 0 15px 40px rgba(212, 175, 55, 0.4), 0 0 80px rgba(212, 175, 55, 0.3); }
}

.register-header-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff 0%, #d4af37 50%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  letter-spacing: -0.5px;
  text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.95rem;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Messages */
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
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.error-message {
  background: rgba(255, 82, 82, 0.1);
  border-color: rgba(255, 82, 82, 0.3);
  color: #ff5252;
}

.success-message {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
  color: #4caf50;
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

.success-message .message-icon {
  background: rgba(76, 175, 80, 0.2);
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

/* Social Section */
.social-section {
  margin-bottom: 32px;
}

.social-label {
  text-align: center;
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.9rem;
  margin-bottom: 16px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.social-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.social-btn {
  position: relative;
  flex: 1;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.social-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.social-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.social-hover {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.social-btn:hover .social-hover {
  opacity: 1;
}

.social-btn.google:hover {
  color: #db4437;
  border-color: #db4437;
  box-shadow: 0 5px 15px rgba(219, 68, 55, 0.3);
}

.social-btn.facebook:hover {
  color: #1877f2;
  border-color: #1877f2;
  box-shadow: 0 5px 15px rgba(24, 119, 242, 0.3);
}

.social-btn.microsoft:hover {
  color: #00a4ef;
  border-color: #00a4ef;
  box-shadow: 0 5px 15px rgba(0, 164, 239, 0.3);
}

/* Divider */
.divider {
  position: relative;
  text-align: center;
  margin: 24px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.divider-text {
  position: relative;
  background: rgba(26, 26, 46, 0.9);
  padding: 0 16px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Form Styles */
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
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: #d4af37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2), 0 2px 8px rgba(0, 0, 0, 0.3);
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

/* Password Strength */
.password-strength {
  margin-top: 8px;
}

.strength-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.strength-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.strength-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.strength-bars {
  display: flex;
  gap: 4px;
}

.strength-bar {
  height: 4px;
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-bar.active.weak { background: #ff5252; }
.strength-bar.active.medium { background: #ffc107; }
.strength-bar.active.strong { background: #4caf50; }

.error-text {
  color: #ff5252;
  font-size: 0.8rem;
  margin-top: 4px;
}

/* Form Options */
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.75);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.checkbox-input {
  width: 18px;
  height: 18px;
  accent-color: #d4af37;
  cursor: pointer;
}

.terms-link {
  color: #d4af37;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.terms-link:hover {
  color: #f4e4c1;
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

/* Submit Button */
.submit-btn {
  position: relative;
  width: 100%;
  padding: 18px 24px;
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
  transform: none;
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

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Footer */
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
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
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
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

/* Responsive Design */
@media (max-width: 640px) {
  .auth-container {
    padding: 16px;
  }
  
  .glass-card {
    padding: 32px 24px;
  }
  
  .register-header-title {
    font-size: 1.75rem;
  }
  
  .social-buttons {
    flex-direction: column;
  }
  
  .social-btn {
    width: 100%;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}

/* Accessibility */
.submit-btn:focus,
.social-btn:focus,
.form-input:focus {
  outline: 2px solid #d4af37;
  outline-offset: 2px;
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .glass-card {
    background: rgba(0, 0, 0, 0.9);
    border-color: rgba(255, 255, 255, 0.3);
  }
  
  .form-input {
    background: rgba(0, 0, 0, 0.5);
    border-color: rgba(255, 255, 255, 0.5);
  }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .floating-orb,
  .logo-icon,
  .btn-glow,
  .social-hover {
    animation: none;
  }
  
  .submit-btn:hover,
  .social-btn:hover {
    transform: none;
  }
}
</style>
