<template>
  <div class="register-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
    </div>

    <div class="auth-container">
      <div class="glass-card">
        <!-- Header Section -->
        <div class="auth-header">
          <div class="logo-section">
            <div class="logo-icon">
              <i class="fa-solid fa-gem"></i>
            </div>
            <h1 class="logo-text">Paclos</h1>
            <p class="logo-subtitle">نظام التسجيل المتقدم</p>
          </div>
        </div>

        <div class="auth-body">
          <!-- Progress Steps -->
          <div class="progress-steps">
            <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
              <div class="step-number">1</div>
              <div class="step-label">المعلومات الأساسية</div>
            </div>
            <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
              <div class="step-number">2</div>
              <div class="step-label">معلومات التواصل</div>
            </div>
            <div class="step" :class="{ active: currentStep >= 3, completed: currentStep > 3 }">
              <div class="step-number">3</div>
              <div class="step-label">الأمان</div>
            </div>
            <div class="step" :class="{ active: currentStep >= 4, completed: currentStep > 4 }">
              <div class="step-number">4</div>
              <div class="step-label">التأكيد</div>
            </div>
          </div>

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

          <!-- Step 1: Basic Information -->
          <div v-if="currentStep === 1" class="step-content">
            <h3 class="step-title">المعلومات الأساسية</h3>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-user label-icon"></i>
                  <span>الاسم الأول</span>
                </label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    v-model="form.firstName" 
                    class="form-input"
                    placeholder="أدخل اسمك الأول"
                    required 
                    autocomplete="given-name"
                  />
                  <div class="input-border"></div>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-user label-icon"></i>
                  <span>الاسم الأخير</span>
                </label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    v-model="form.lastName" 
                    class="form-input"
                    placeholder="أدخل اسمك الأخير"
                    required 
                    autocomplete="family-name"
                  />
                  <div class="input-border"></div>
                </div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-calendar label-icon"></i>
                <span>تاريخ الميلاد</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="date" 
                  v-model="form.birthDate" 
                  class="form-input"
                  required 
                />
                <div class="input-border"></div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-venus-mars label-icon"></i>
                <span>الجنس</span>
              </label>
              <div class="gender-options">
                <label class="gender-option">
                  <input type="radio" v-model="form.gender" value="male" />
                  <span class="gender-text">ذكر</span>
                </label>
                <label class="gender-option">
                  <input type="radio" v-model="form.gender" value="female" />
                  <span class="gender-text">أنثى</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Step 2: Contact Information -->
          <div v-if="currentStep === 2" class="step-content">
            <h3 class="step-title">معلومات التواصل</h3>
            
            <!-- Contact Method Toggle -->
            <div class="contact-method-toggle">
              <label class="toggle-label">
                <span class="toggle-text">طريقة التواصل المفضلة</span>
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
                <i class="fa-solid fa-location-dot label-icon"></i>
                <span>العنوان</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  v-model="form.address" 
                  class="form-input"
                  placeholder="أدخل عنوانك الكامل"
                  required 
                  autocomplete="street-address"
                />
                <div class="input-border"></div>
              </div>
            </div>
          </div>

          <!-- Step 3: Security -->
          <div v-if="currentStep === 3" class="step-content">
            <h3 class="step-title">الأمان</h3>
            <div class="form-group">
              <label class="form-label">
                <i class="fa-solid fa-user label-icon"></i>
                <span>اسم المستخدم</span>
              </label>
              <div class="input-wrapper">
                <input 
                  type="text" 
                  v-model="form.username" 
                  class="form-input"
                  placeholder="اختر اسم مستخدم فريد"
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
          </div>

          <!-- Step 4: Confirmation -->
          <div v-if="currentStep === 4" class="step-content">
            <h3 class="step-title">تأكيد المعلومات</h3>
            <div class="confirmation-summary">
              <div class="summary-item">
                <span class="summary-label">الاسم الكامل:</span>
                <span class="summary-value">{{ form.firstName }} {{ form.lastName }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">اسم المستخدم:</span>
                <span class="summary-value">{{ form.username }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">البريد الإلكتروني:</span>
                <span class="summary-value">{{ form.email || form.phone }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">العنوان:</span>
                <span class="summary-value">{{ form.address }}</span>
              </div>
            </div>
            
            <!-- Terms Agreement -->
            <div class="form-options">
              <label class="checkbox-wrapper">
                <input type="checkbox" v-model="form.acceptTerms" class="checkbox-input" required />
                <span class="checkbox-text">أوافق على الشروط والأحكام وسياسة الخصوصية</span>
              </label>
              <a href="/terms" target="_blank" class="terms-link">عرض الشروط</a>
            </div>

            <!-- Email Verification -->
            <div v-if="form.contactMethod === 'email'" class="verification-section">
              <div class="verification-input">
                <input 
                  type="text" 
                  v-model="form.verificationCode" 
                  class="form-input"
                  placeholder="أدخل رمز التحقق"
                  maxlength="6"
                />
                <button @click="sendVerificationCode" class="verify-btn" :disabled="verificationSent">
                  {{ verificationSent ? 'تم الإرسال' : 'إرسال الرمز' }}
                </button>
              </div>
            </div>

            <!-- Phone Verification -->
            <div v-if="form.contactMethod === 'phone'" class="verification-section">
              <div class="verification-input">
                <input 
                  type="text" 
                  v-model="form.verificationCode" 
                  class="form-input"
                  placeholder="أدخل رمز التحقق"
                  maxlength="6"
                />
                <button @click="sendVerificationCode" class="verify-btn" :disabled="verificationSent">
                  {{ verificationSent ? 'تم الإرسال' : 'إرسال الرمز' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="step-navigation">
            <button 
              v-if="currentStep > 1" 
              @click="previousStep" 
              class="nav-btn prev-btn"
              :disabled="loading"
            >
              <i class="fa-solid fa-arrow-right"></i>
              <span>السابق</span>
            </button>
            
            <button 
              v-if="currentStep < 4" 
              @click="nextStep" 
              class="nav-btn next-btn"
              :disabled="!isCurrentStepValid || loading"
            >
              <span>التالي</span>
              <i class="fa-solid fa-arrow-left"></i>
            </button>
            
            <button 
              v-if="currentStep === 4" 
              @click="handleSignup" 
              class="submit-btn"
              :disabled="!isFormValid || loading"
            >
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import zxcvbn from 'zxcvbn';

const authStore = useAuthStore();
const router = useRouter();
const { t } = useI18n();

const currentStep = ref(1);
const loading = ref(false);
const error = ref(null);
const success = ref(null);
const verificationSent = ref(false);

const form = reactive({
  firstName: '',
  lastName: '',
  birthDate: '',
  gender: '',
  username: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
  contactMethod: 'email',
  verificationCode: ''
});

const passwordStrength = reactive({
  score: 0,
  text: '',
});

const isCurrentStepValid = computed(() => {
  switch(currentStep.value) {
    case 1:
      return form.firstName && form.lastName && form.birthDate && form.gender;
    case 2:
      return (form.contactMethod === 'email' ? form.email : form.phone) && form.address;
    case 3:
      return form.username && form.password && form.confirmPassword && 
             form.password === form.confirmPassword && form.password.length >= 8;
    case 4:
      return form.acceptTerms && (form.contactMethod === 'email' ? form.verificationCode : true);
    default:
      return false;
  }
});

const isFormValid = computed(() => {
  return isCurrentStepValid.value;
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

const nextStep = () => {
  if (isCurrentStepValid.value) {
    currentStep.value++;
  }
};

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const sendVerificationCode = async () => {
  try {
    loading.value = true;
    // Mock verification code sending
    setTimeout(() => {
      verificationSent.value = true;
      loading.value = false;
      // In real implementation, send SMS/email with verification code
    }, 2000);
  } catch (err) {
    error.value = 'فشل إرسال رمز التحقق';
    loading.value = false;
  }
};

const handleSignup = async () => {
  if (!isFormValid.value) return;

  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    const userData = {
      username: form.username,
      email: form.contactMethod === 'email' ? form.email : '',
      phone: form.contactMethod === 'phone' ? form.phone : '',
      password: form.password,
      firstName: form.firstName,
      lastName: form.lastName,
      address: form.address,
      birthDate: form.birthDate,
      gender: form.gender
    };
    
    const result = await authStore.register(userData);
    
    if (result.success) {
      success.value = 'تم إنشاء الحساب بنجاح!';
      
      // Auto-login after successful registration
      await authStore.login(userData.username, userData.password);
      
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);
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
/* ===== Advanced Registration System ===== */
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
  max-width: 600px;
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
  color: #1a1a2e;
  font-size: 32px;
  box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
}

.logo-text {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin: 0;
}

/* Progress Steps */
.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 40px;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border-color: #d4af37;
  color: #1a1a2e;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.step.completed .step-number {
  background: rgba(212, 175, 55, 0.2);
  border-color: rgba(212, 175, 55, 0.4);
  color: #d4af37;
}

.step-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  transition: color 0.3s ease;
}

.step.active .step-label,
.step.completed .step-label {
  color: #ffffff;
}

/* Step Content */
.step-content {
  margin-bottom: 30px;
}

.step-title {
  color: #ffffff;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 25px;
  text-align: center;
}

/* Form Styles */
.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  margin-bottom: 24px;
  flex: 1;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
}

.label-icon {
  font-size: 16px;
  color: #d4af37;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
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

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.form-input:focus ~ .input-border {
  transform: scaleX(1);
}

/* Gender Options */
.gender-options {
  display: flex;
  gap: 20px;
}

.gender-option {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: color 0.3s ease;
}

.gender-option input[type="radio"] {
  accent-color: #d4af37;
}

.gender-text {
  font-size: 14px;
}

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

/* Password Strength */
.password-strength {
  margin-top: 12px;
}

.strength-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.strength-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
}

.strength-text {
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
}

.strength-bars {
  display: flex;
  gap: 4px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-bar.active.weak {
  background: #ff4444;
}

.strength-bar.active.medium {
  background: #ffaa00;
}

.strength-bar.active.strong {
  background: #00c851;
}

/* Error Text */
.error-text {
  color: #ff4444;
  font-size: 12px;
  margin-top: 8px;
}

/* Confirmation Summary */
.confirmation-summary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.summary-value {
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
}

/* Verification Section */
.verification-section {
  margin-bottom: 24px;
}

.verification-input {
  display: flex;
  gap: 12px;
}

.verify-btn {
  padding: 16px 20px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 8px;
  color: #1a1a2e;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.verify-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.verify-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Form Options */
.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.checkbox-input {
  accent-color: #d4af37;
}

.checkbox-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.terms-link {
  color: #d4af37;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.terms-link:hover {
  color: #f4e4c1;
}

/* Step Navigation */
.step-navigation {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.nav-btn {
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  outline: none;
}

.nav-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.next-btn {
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  color: #1a1a2e;
  border: none;
}

.next-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 12px;
  color: #1a1a2e;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  outline: none;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(212, 175, 55, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  position: relative;
  z-index: 2;
}

.btn-icon {
  font-size: 18px;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Messages */
.message {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.error-message {
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid rgba(255, 68, 68, 0.2);
}

.success-message {
  background: rgba(0, 200, 81, 0.1);
  border: 1px solid rgba(0, 200, 81, 0.2);
}

.message-icon {
  font-size: 20px;
  margin-top: 2px;
}

.error-message .message-icon {
  color: #ff4444;
}

.success-message .message-icon {
  color: #00c851;
}

.message-content {
  flex: 1;
}

.message-title {
  display: block;
  color: #ffffff;
  font-weight: 600;
  margin-bottom: 4px;
}

.message-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .auth-container {
    max-width: 100%;
    padding: 10px;
  }
  
  .glass-card {
    padding: 30px 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .progress-steps {
    flex-direction: column;
    gap: 20px;
  }
  
  .step-navigation {
    flex-direction: column;
  }
  
  .verification-input {
    flex-direction: column;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
