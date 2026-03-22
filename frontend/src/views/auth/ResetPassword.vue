<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h3>
          <i class="fa-solid fa-lock-open"></i>
          {{ $t('resetPasswordTitle') || 'إعادة تعيين كلمة المرور' }}
        </h3>
      </div>

      <div class="auth-body">
        <div v-if="error" class="error-message">
          <i class="fa-solid fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          <i class="fa-solid fa-check-circle"></i>
          {{ success }}
        </div>

        <form @submit.prevent="handleReset" v-if="!success">
          <div class="form-group">
            <label>
              <i class="fa-solid fa-lock"></i>
              {{ $t('newPassword') || 'كلمة المرور الجديدة' }}
            </label>
            <input type="password" v-model="password" required />
          </div>

          <div class="form-group">
            <label>
              <i class="fa-solid fa-lock"></i>
              {{ $t('confirmPassword') }}
            </label>
            <input type="password" v-model="confirmPassword" required />
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <i class="fa-solid fa-save"></i>
            <span v-if="!loading">{{ $t('reset') || 'حفظ كلمة المرور الجديدة' }}</span>
            <span v-else><i class="fa-solid fa-spinner fa-spin"></i> {{ $t('loading') }}</span>
          </button>
        </form>

        <div class="auth-footer">
          <router-link to="/login">{{ $t('login') }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { auth } from '@/firebase';
import { confirmPasswordReset } from 'firebase/auth';

const route = useRoute();
const router = useRouter();
const { t } = useI18n();

const password = ref('');
const confirmPassword = ref('');
const loading = ref(false);
const error = ref(null);
const success = ref(null);

const handleReset = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = t('passwordsDoNotMatch') || 'كلمتا المرور غير متطابقتين';
    return;
  }

  const token = route.params.token;
  if (!token) {
    error.value = 'رابط غير صالح';
    return;
  }

  loading.value = true;
  error.value = null;
  success.value = null;
  try {
    await confirmPasswordReset(auth, token, password.value);
    success.value = t('passwordResetSuccess') || 'تمت إعادة تعيين كلمة المرور بنجاح.';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}
.auth-container {
  width: 100%;
  max-width: 450px;
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.auth-header h3 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}
.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.submit-btn {
  width: 100%;
  padding: 12px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
.auth-footer {
  text-align: center;
  margin-top: 20px;
}
</style>
