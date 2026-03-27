<template>
  <v-card class="contact-form-card" elevation="4">
    <v-card-title class="text-h5 font-weight-bold mb-4">
      <v-icon color="primary" class="mr-2">mdi-email-send</v-icon>
      تواصل معنا
    </v-card-title>
    
    <v-card-text>
      <v-form @submit.prevent="submitContactForm">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="contactForm.name"
              :label="$t('fullName') || 'الاسم الكامل'"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              :error-messages="v$.name.$error ? v$.name.$errors[0].$message : ''"
              @blur="v$.name.$touch()"
              required
            />
          </v-col>
          
          <v-col cols="12" md="6">
            <v-text-field
              v-model="contactForm.email"
              :label="$t('email') || 'البريد الإلكتروني'"
              prepend-inner-icon="mdi-email"
              type="email"
              variant="outlined"
              :error-messages="v$.email.$error ? v$.email.$errors[0].$message : ''"
              @blur="v$.email.$touch()"
              required
            />
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="contactForm.phone"
              :label="$t('phone') || 'رقم الهاتف'"
              prepend-inner-icon="mdi-phone"
              type="tel"
              variant="outlined"
              :error-messages="v$.phone.$error ? v$.phone.$errors[0].$message : ''"
              @blur="v$.phone.$touch()"
              required
            />
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12">
            <v-textarea
              v-model="contactForm.message"
              :label="$t('message') || 'الرسالة'"
              prepend-inner-icon="mdi-message-text"
              variant="outlined"
              rows="4"
              :error-messages="v$.message.$error ? v$.message.$errors[0].$message : ''"
              @blur="v$.message.$touch()"
              required
            />
          </v-col>
        </v-row>
        
        <v-row>
          <v-col cols="12">
            <v-btn
              type="submit"
              color="primary"
              variant="elevated"
              size="large"
              prepend-icon="mdi-send"
              :loading="sending"
              block
            >
              {{ sending ? ($t('sending') || 'جاري الإرسال...') : ($t('sendMessage') || 'إرسال الرسالة') }}
            </v-btn>
          </v-col>
        </v-row>
        
        <!-- Form Status Messages -->
        <v-row v-if="formStatus" class="mt-4">
          <v-col cols="12">
            <v-alert
              :type="formStatus.type"
              :icon="formStatus.icon"
              variant="elevated"
              class="mb-0"
            >
              {{ formStatus.message }}
            </v-alert>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
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

