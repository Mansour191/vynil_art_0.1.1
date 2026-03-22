<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h3>
          <i class="fa-solid fa-envelope-open-text"></i>
          {{ $t('verifyEmailTitle') || 'تفعيل البريد الإلكتروني' }}
        </h3>
      </div>

      <div class="auth-body">
        <div v-if="loading" class="loading-state">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <p>{{ $t('verifying') || 'جاري التحقق...' }}</p>
        </div>

        <div v-if="error" class="error-message">
          <i class="fa-solid fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          <i class="fa-solid fa-check-circle"></i>
          {{ success }}
        </div>

        <div class="auth-footer">
          <router-link to="/login">{{ $t('login') }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { auth } from '@/firebase';
import { applyActionCode } from 'firebase/auth';

const route = useRoute();
const router = useRouter();
const { t } = useI18n();

const loading = ref(true);
const error = ref(null);
const success = ref(null);

onMounted(async () => {
  const token = route.params.token;
  if (!token) {
    error.value = 'رابط غير صالح';
    loading.value = false;
    return;
  }

  try {
    await applyActionCode(auth, token);
    success.value = t('emailVerifiedSuccess') || 'تم تفعيل البريد الإلكتروني بنجاح.';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
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
.loading-state {
  text-align: center;
  padding: 20px;
}
.loading-state i {
  font-size: 2rem;
  margin-bottom: 15px;
}
.auth-footer {
  text-align: center;
  margin-top: 20px;
}
</style>
