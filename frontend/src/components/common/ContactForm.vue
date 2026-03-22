<template>
  <div class="contact-form-column">
    <div class="contact-form-card">
      <form @submit.prevent="submitContactForm" class="contact-form">
        <div class="form-row">
          <div class="form-group">
            <label for="name">
              <i class="fa-solid fa-user"></i>
              {{ $t('fullName') }}
            </label>
            <input
              type="text"
              id="name"
              v-model="contactForm.name"
              :placeholder="$t('fullName')"
              :class="{ 'is-invalid': v$.name.$error }"
              @blur="v$.name.$touch()"
            />
            <div v-if="v$.name.$error" class="error-message">
              {{ v$.name.$errors[0].$message }}
            </div>
          </div>

          <div class="form-group">
            <label for="email">
              <i class="fa-solid fa-envelope"></i>
              {{ $t('email') }}
            </label>
            <input
              type="email"
              id="email"
              v-model="contactForm.email"
              :placeholder="$t('email')"
              :class="{ 'is-invalid': v$.email.$error }"
              @blur="v$.email.$touch()"
            />
            <div v-if="v$.email.$error" class="error-message">
              {{ v$.email.$errors[0].$message }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="phone">
            <i class="fa-solid fa-phone"></i>
            {{ $t('phone') }}
          </label>
          <input
            type="tel"
            id="phone"
            v-model="contactForm.phone"
            :placeholder="$t('phone')"
            :class="{ 'is-invalid': v$.phone.$error }"
            @blur="v$.phone.$touch()"
          />
          <div v-if="v$.phone.$error" class="error-message">
            {{ v$.phone.$errors[0].$message }}
          </div>
        </div>

        <div class="form-group">
          <label for="message">
            <i class="fa-solid fa-comment"></i>
            {{ $t('message') }}
          </label>
          <textarea
            id="message"
            v-model="contactForm.message"
            rows="5"
            :placeholder="$t('messagePlaceholder')"
            :class="{ 'is-invalid': v$.message.$error }"
            @blur="v$.message.$touch()"
          ></textarea>
          <div v-if="v$.message.$error" class="error-message">
            {{ v$.message.$errors[0].$message }}
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="sending">
          <i class="fa-solid fa-paper-plane"></i>
          <span v-if="!sending">{{ $t('sendMessage') }}</span>
          <span v-else>{{ $t('sending') }}</span>
        </button>

        <div v-if="formStatus" :class="['form-status', formStatus.type]">
          <i :class="formStatus.icon"></i>
          <span>{{ formStatus.message }}</span>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useVuelidate } from '@vuelidate/core';
import { required, email, minLength, helpers } from '@vuelidate/validators';

const { t } = useI18n();

const contactForm = reactive({
  name: '',
  email: '',
  phone: '',
  message: '',
});

// قواعد التحقق
const rules = computed(() => ({
  name: { 
    required: helpers.withMessage(t('fieldRequired') || 'هذا الحقل مطلوب', required),
    minLength: helpers.withMessage(t('nameMinLength') || 'الاسم يجب أن يكون 3 أحرف على الأقل', minLength(3))
  },
  email: { 
    required: helpers.withMessage(t('fieldRequired') || 'هذا الحقل مطلوب', required),
    email: helpers.withMessage(t('invalidEmail') || 'بريد إلكتروني غير صالح', email)
  },
  phone: { 
    required: helpers.withMessage(t('fieldRequired') || 'هذا الحقل مطلوب', required),
    minLength: helpers.withMessage(t('phoneMinLength') || 'رقم الهاتف غير صالح', minLength(10))
  },
  message: { 
    required: helpers.withMessage(t('fieldRequired') || 'هذا الحقل مطلوب', required),
    minLength: helpers.withMessage(t('messageMinLength') || 'الرسالة قصيرة جداً', minLength(10))
  }
}));

const v$ = useVuelidate(rules, contactForm);

const sending = ref(false);
const formStatus = ref(null);

const submitContactForm = async () => {
  const isFormCorrect = await v$.value.$validate();
  if (!isFormCorrect) return;

  sending.value = true;
  formStatus.value = null;
  try {
    // محاكاة إرسال الطلب
    await new Promise((resolve) => setTimeout(resolve, 1500));
    formStatus.value = {
      type: 'success',
      icon: 'fa-solid fa-check-circle',
      message: t('messageSent'),
    };
    
    // إعادة تعيين النموذج
    contactForm.name = '';
    contactForm.email = '';
    contactForm.phone = '';
    contactForm.message = '';
    v$.value.$reset();
  } catch (error) {
    formStatus.value = {
      type: 'error',
      icon: 'fa-solid fa-exclamation-circle',
      message: t('messageError'),
    };
  } finally {
    sending.value = false;
    setTimeout(() => {
      formStatus.value = null;
    }, 5000);
  }
};
</script>

<style scoped>
.contact-form-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 25px;
  border: 1px solid var(--border-subtle);
  height: 100%;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

@media (min-width: 768px) {
  .form-row {
    grid-template-columns: 1fr 1fr;
  }
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--gold-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--gold-primary);
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.form-group input.is-invalid,
.form-group textarea.is-invalid {
  border-color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 0.75rem;
  margin-top: 5px;
  font-weight: 500;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border: none;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-status {
  margin-top: 20px;
  padding: 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  font-weight: 600;
}

.form-status.success {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
}

.form-status.error {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}
</style>
