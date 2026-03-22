<template>
  <div class="auth-page">
    <div class="bg-effects">
      <div class="gradient-overlay"></div>
      <div class="floating-orb orb-1"></div>
      <div class="floating-orb orb-2"></div>
      <div class="floating-orb orb-3"></div>
      <div class="floating-orb orb-4"></div>
      <div class="grid-pattern"></div>
    </div>

    <div class="auth-container">
      <div class="glass-card">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-circle">
            <i class="fa-solid fa-gem"></i>
          </div>
          <h1 class="logo-text">Paclos</h1>
          <p class="logo-subtitle">نظام التسجيل المتقدم</p>
        </div>

        <!-- Auth Forms -->
        <div class="auth-forms">
          <!-- Login Form -->
          <div v-if="currentView === 'login'" class="auth-form">
            <h2 class="form-title">تسجيل الدخول</h2>
            <p class="form-subtitle">مرحباً بعودتك! سجل الدخول لحسابك</p>

            <form @submit.prevent="handleLogin" class="form">
              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-user"></i>
                  البريد الإلكتروني أو اسم المستخدم
                </label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    v-model="loginForm.emailOrUsername" 
                    class="form-input"
                    placeholder="أدخل بريدك الإلكتروني أو اسم المستخدم"
                    required
                    autocomplete="username"
                  />
                  <div class="input-border"></div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-lock"></i>
                  كلمة المرور
                </label>
                <div class="input-wrapper">
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    v-model="loginForm.password" 
                    class="form-input"
                    placeholder="أدخل كلمة المرور"
                    required
                    autocomplete="current-password"
                  />
                  <button 
                    type="button" 
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                  >
                    <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                  </button>
                  <div class="input-border"></div>
                </div>
              </div>

              <div class="form-options">
                <label class="checkbox-wrapper">
                  <input type="checkbox" v-model="loginForm.rememberMe" />
                  <span class="checkbox-text">تذكرني</span>
                </label>
                <a href="/forgot-password" class="forgot-link">نسيت كلمة المرور؟</a>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading">
                <span class="btn-content">
                  <i class="fa-solid fa-sign-in-alt"></i>
                  <span v-if="!loading">تسجيل الدخول</span>
                  <span v-else class="loading-text">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    جاري تسجيل الدخول...
                  </span>
                </span>
                <div class="btn-glow"></div>
              </button>
            </form>

            <!-- Social Login -->
            <div class="social-login">
              <div class="divider">
                <span class="divider-text">أو سجل الدخول باستخدام</span>
              </div>
              <div class="social-buttons">
                <button class="social-btn google" @click="socialLogin('google')">
                  <i class="fab fa-google"></i>
                  <span>Google</span>
                </button>
                <button class="social-btn facebook" @click="socialLogin('facebook')">
                  <i class="fab fa-facebook-f"></i>
                  <span>Facebook</span>
                </button>
                <button class="social-btn microsoft" @click="socialLogin('microsoft')">
                  <i class="fab fa-microsoft"></i>
                  <span>Microsoft</span>
                </button>
              </div>
            </div>

            <!-- Switch to Register -->
            <div class="switch-form">
              <p class="switch-text">
                ليس لديك حساب؟
                <button class="switch-btn" @click="currentView = 'register'">
                  إنشاء حساب جديد
                </button>
              </p>
            </div>
          </div>

          <!-- Register Form -->
          <div v-if="currentView === 'register'" class="auth-form">
            <h2 class="form-title">إنشاء حساب جديد</h2>
            <p class="form-subtitle">انضم إلينا وأنشئ حسابك الجديد</p>

            <form @submit.prevent="handleRegister" class="form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">
                    <i class="fa-solid fa-user"></i>
                    الاسم الأول
                  </label>
                  <div class="input-wrapper">
                    <input 
                      type="text" 
                      v-model="registerForm.firstName" 
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
                    <i class="fa-solid fa-user"></i>
                    الاسم الأخير
                  </label>
                  <div class="input-wrapper">
                    <input 
                      type="text" 
                      v-model="registerForm.lastName" 
                      class="form-input"
                      placeholder="أدخل اسمك الأخير"
                      autocomplete="family-name"
                    />
                    <div class="input-border"></div>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-user"></i>
                  اسم المستخدم
                </label>
                <div class="input-wrapper">
                  <input 
                    type="text" 
                    v-model="registerForm.username" 
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
                  <i class="fa-solid fa-envelope"></i>
                  البريد الإلكتروني
                </label>
                <div class="input-wrapper">
                  <input 
                    type="email" 
                    v-model="registerForm.email" 
                    class="form-input"
                    placeholder="أدخل بريدك الإلكتروني"
                    required
                    autocomplete="email"
                  />
                  <div class="input-border"></div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-phone"></i>
                  رقم الهاتف
                </label>
                <div class="input-wrapper">
                  <input 
                    type="tel" 
                    v-model="registerForm.phone" 
                    class="form-input"
                    placeholder="أدخل رقم هاتفك"
                    autocomplete="tel"
                  />
                  <div class="input-border"></div>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <i class="fa-solid fa-lock"></i>
                  كلمة المرور
                </label>
                <div class="input-wrapper">
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    v-model="registerForm.password" 
                    class="form-input"
                    placeholder="أدخل كلمة المرور"
                    required
                    autocomplete="new-password"
                    @input="checkPasswordStrength"
                  />
                  <button 
                    type="button" 
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                  >
                    <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                  </button>
                  <div class="input-border"></div>
                </div>
                <!-- Password Strength Indicator -->
                <div v-if="registerForm.password" class="password-strength">
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
                  <i class="fa-solid fa-lock"></i>
                  تأكيد كلمة المرور
                </label>
                <div class="input-wrapper">
                  <input 
                    :type="showConfirmPassword ? 'text' : 'password'"
                    v-model="registerForm.confirmPassword" 
                    class="form-input"
                    placeholder="أعد إدخال كلمة المرور"
                    required
                    autocomplete="new-password"
                  />
                  <button 
                    type="button" 
                    class="password-toggle"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <i :class="showConfirmPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                  </button>
                  <div class="input-border"></div>
                </div>
                <div
                  v-if="registerForm.password && registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword"
                  class="error-text"
                >
                  كلمات المرور غير متطابقة
                </div>
              </div>

              <div class="form-options">
                <label class="checkbox-wrapper">
                  <input type="checkbox" v-model="registerForm.acceptTerms" required />
                  <span class="checkbox-text">أوافق على الشروط والأحكام وسياسة الخصوصية</span>
                </label>
              </div>

              <button type="submit" class="submit-btn" :disabled="loading || !isFormValid">
                <span class="btn-content">
                  <i class="fa-solid fa-user-plus"></i>
                  <span v-if="!loading">إنشاء حساب</span>
                  <span v-else class="loading-text">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    جاري إنشاء الحساب...
                  </span>
                </span>
                <div class="btn-glow"></div>
              </button>
            </form>

            <!-- Social Register -->
            <div class="social-login">
              <div class="divider">
                <span class="divider-text">أو سجل باستخدام</span>
              </div>
              <div class="social-buttons">
                <button class="social-btn google" @click="socialLogin('google')">
                  <i class="fab fa-google"></i>
                  <span>Google</span>
                </button>
                <button class="social-btn facebook" @click="socialLogin('facebook')">
                  <i class="fab fa-facebook-f"></i>
                  <span>Facebook</span>
                </button>
                <button class="social-btn microsoft" @click="socialLogin('microsoft')">
                  <i class="fab fa-microsoft"></i>
                  <span>Microsoft</span>
                </button>
              </div>
            </div>

            <!-- Switch to Login -->
            <div class="switch-form">
              <p class="switch-text">
                لديك حساب بالفعل؟
                <button class="switch-btn" @click="currentView = 'login'">
                  تسجيل الدخول
                </button>
              </p>
            </div>
          </div>
        </div>

        <!-- Error/Success Messages -->
        <div v-if="error" class="message error-message">
          <div class="message-icon">
            <i class="fa-solid fa-exclamation-triangle"></i>
          </div>
          <div class="message-content">
            <span class="message-title">خطأ</span>
            <span class="message-text">{{ error }}</span>
          </div>
          <button class="message-close" @click="error = null">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>

        <div v-if="success" class="message success-message">
          <div class="message-icon">
            <i class="fa-solid fa-check-circle"></i>
          </div>
          <div class="message-content">
            <span class="message-title">نجاح</span>
            <span class="message-text">{{ success }}</span>
          </div>
          <button class="message-close" @click="success = null">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import zxcvbn from 'zxcvbn';

const router = useRouter();
const authStore = useAuthStore();

const currentView = ref('login');
const loading = ref(false);
const error = ref(null);
const success = ref(null);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const passwordStrength = reactive({
  score: 0,
  text: '',
});

const loginForm = reactive({
  emailOrUsername: '',
  password: '',
  rememberMe: false,
});

const registerForm = reactive({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false,
});

const isFormValid = computed(() => {
  return registerForm.firstName &&
         registerForm.username &&
         registerForm.email &&
         registerForm.password &&
         registerForm.confirmPassword &&
         registerForm.password === registerForm.confirmPassword &&
         registerForm.acceptTerms &&
         passwordStrength.score >= 2;
});

const checkPasswordStrength = () => {
  if (registerForm.password) {
    const result = zxcvbn(registerForm.password);
    passwordStrength.score = result.score;

    const strengthTexts = {
      0: 'ضعيف جداً',
      1: 'ضعيف',
      2: 'متوسط',
      3: 'قوي',
      4: 'قوي جداً'
    };
    passwordStrength.text = strengthTexts[result.score];
  } else {
    passwordStrength.score = 0;
    passwordStrength.text = '';
  }
};

const handleLogin = async () => {
  try {
    loading.value = true;
    error.value = null;
    success.value = null;

    await authStore.login(loginForm.emailOrUsername, loginForm.password);
    
    success.value = 'تم تسجيل الدخول بنجاح!';
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  } catch (err) {
    error.value = err.message || 'فشل تسجيل الدخول';
  } finally {
    loading.value = false;
  }
};

const handleRegister = async () => {
  try {
    loading.value = true;
    error.value = null;
    success.value = null;

    if (!isFormValid.value) {
      error.value = 'يرجى ملء جميع الحقول المطلوبة بشكل صحيح';
      return;
    }

    const userData = {
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      password_confirm: registerForm.confirmPassword,
      first_name: registerForm.firstName,
      last_name: registerForm.lastName,
      phone: registerForm.phone,
    };
    
    await authStore.register(userData);
    
    success.value = 'تم إنشاء الحساب بنجاح!';
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  } catch (err) {
    error.value = err.message || 'فشل إنشاء الحساب';
  } finally {
    loading.value = false;
  }
};

const socialLogin = (provider) => {
  // TODO: Implement social login
  console.log(`Social login with ${provider}`);
  error.value = `تسجيل الدخول باستخدام ${provider} قيد التطوير`;
};

onMounted(() => {
  // Initialize auth store
  authStore.initializeAuth();
});
</script>

<style scoped>
/* ===== Advanced Auth Page ===== */
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
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
  background: radial-gradient(circle at 25% 25%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 75% 75%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 50% 10%, rgba(212, 175, 55, 0.05) 0%, transparent 50%);
}

.floating-orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, rgba(212, 175, 55, 0.05) 50%, transparent 100%);
  filter: blur(2px);
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.orb-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.orb-4 {
  width: 100px;
  height: 100px;
  top: 30%;
  right: 30%;
  animation-delay: 6s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
  25% { transform: translateY(-30px) rotate(90deg) scale(1.05); }
  50% { transform: translateY(-20px) rotate(180deg) scale(1); }
  75% { transform: translateY(-40px) rotate(270deg) scale(1.02); }
}

.grid-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* Auth Container */
.auth-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 500px;
  padding: 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 0 40px rgba(255, 255, 255, 0.02);
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
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
}

.glass-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Logo Section */
.logo-section {
  text-align: center;
  margin-bottom: 40px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #0f0f23;
  font-size: 32px;
  box-shadow: 
    0 10px 30px rgba(212, 175, 55, 0.3),
    inset 0 2px 10px rgba(255, 255, 255, 0.3);
  animation: logoGlow 3s ease-in-out infinite alternate;
}

@keyframes logoGlow {
  0% { box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3), inset 0 2px 10px rgba(255, 255, 255, 0.3); }
  100% { box-shadow: 0 15px 40px rgba(212, 175, 55, 0.4), inset 0 2px 15px rgba(255, 255, 255, 0.4); }
}

.logo-text {
  font-size: 32px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

/* Auth Forms */
.auth-form {
  margin-bottom: 30px;
}

.form-title {
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  text-align: center;
}

.form-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0 0 30px 0;
  text-align: center;
}

/* Form Styles */
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 500;
}

.form-label i {
  color: #d4af37;
  font-size: 16px;
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
  border-color: rgba(212, 175, 55, 0.4);
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
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.6), transparent);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.form-input:focus ~ .input-border {
  transform: scaleX(1);
}

.password-toggle {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #d4af37;
}

/* Password Strength */
.password-strength {
  margin-top: 8px;
}

.strength-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.strength-label {
  color: rgba(255, 255, 255, 0.6);
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
  background: #dc3545;
}

.strength-bar.active.medium {
  background: #ffc107;
}

.strength-bar.active.strong {
  background: #28a745;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-input {
  accent-color: #d4af37;
  width: 16px;
  height: 16px;
}

.checkbox-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.forgot-link,
.switch-btn {
  color: #d4af37;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s ease;
  background: transparent;
  border: none;
  cursor: pointer;
}

.forgot-link:hover,
.switch-btn:hover {
  color: #f4e4c1;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 18px;
  background: linear-gradient(135deg, #d4af37 0%, #f4e4c1 50%, #d4af37 100%);
  border: none;
  border-radius: 12px;
  color: #0f0f23;
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
  box-shadow: 0 15px 35px rgba(212, 175, 55, 0.4);
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

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.submit-btn:hover:not(:disabled) .btn-glow {
  left: 100%;
}

/* Social Login */
.social-login {
  margin: 30px 0;
}

.divider {
  position: relative;
  text-align: center;
  margin: 20px 0;
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
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(10px);
  padding: 0 16px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

.social-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.social-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.social-btn.google:hover {
  border-color: #4285f4;
  color: #4285f4;
}

.social-btn.facebook:hover {
  border-color: #1877f2;
  color: #1877f2;
}

.social-btn.microsoft:hover {
  border-color: #00a4ef;
  color: #00a4ef;
}

.social-btn i {
  font-size: 20px;
}

/* Switch Form */
.switch-form {
  text-align: center;
  margin-top: 20px;
}

.switch-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

/* Messages */
.message {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 12px;
  margin-top: 20px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.error-message {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.success-message {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.message-icon {
  font-size: 20px;
  margin-top: 2px;
}

.error-message .message-icon {
  color: #dc3545;
}

.success-message .message-icon {
  color: #28a745;
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

/* Error Text */
.error-text {
  color: #dc3545;
  font-size: 12px;
  margin-top: 8px;
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
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .social-buttons {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .social-btn {
    flex-direction: row;
    justify-content: center;
    padding: 12px 16px;
  }
  
  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
