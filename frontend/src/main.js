import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import i18n from './plugins/i18n';
import AITranslation from './plugins/AITranslation';
import store from './store';
import seo from './plugins/seo';
import '@/assets/theme.css';
import AlertService from '@/integration/services/AlertService';
import { useAuthStore } from '@/store/auth';
import AIService from '@/services/AIService';
import AIMonitorService from '@/services/AIMonitorService';
import PricingService from '@/services/PricingService';
import ChatService from '@/integration/services/ChatService';
import AILearningService from '@/services/AILearningService';
// استيراد الأيقونات
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@mdi/font/css/materialdesignicons.min.css';

const app = createApp(App);
const pinia = createPinia();

// Initialize AI Services Immediately
console.log('🚀 Starting AI Services...');

// Start AI Monitoring
console.log('🔍 Starting AI Monitoring...');

// Initialize Pricing Service
PricingService.clearAllCache();
console.log('✅ Pricing Service Initialized');

// معالج الأخطاء العالمي
app.config.errorHandler = (err, instance, info) => {
  console.error('🔥 Global Error:', err);
  console.error('📍 Info:', info);

  // إرسال تنبيه للمستخدم
  AlertService.sendAlert({
    type: 'danger',
    severity: 'high',
    title: '⚠️ حدث خطأ غير متوقع',
    message: 'نعتذر، حدث خطأ في النظام. تم تسجيل الخطأ وسنعمل على إصلاحه.',
  });
};

app.use(pinia);
app.use(store);
app.use(router);
app.use(i18n);
app.use(AITranslation);
app.use(seo);

// Initialize auth store after all plugins are installed
const authStore = useAuthStore();
authStore.initializeAuth();

// Mount the app
const mountedApp = app.mount('#app');

// Initialize AI Services after app is mounted
console.log('🚀 Starting AI Services...');

// Initialize AI Services
AIService.initializeAISystems().then(() => {
  console.log('✅ AI Services Started Successfully');
}).catch(error => {
  console.warn('⚠️ AI Services Warning:', error);
});

// Start AI Monitoring
console.log('🔍 Starting AI Monitoring...');
AIMonitorService.startMonitoring().then(() => {
  console.log('✅ AI Monitoring Started');
}).catch(error => {
  console.warn('⚠️ AI Monitoring Warning:', error);
});

// Initialize Pricing Service
PricingService.clearAllCache();
console.log('✅ Pricing Service Initialized');

// Initialize Chat Service to ensure it's always available
console.log('💬 Chat Service Initialized');

// Initialize AI Learning System
console.log('🎓 Starting AI Learning System...');
AILearningService.initializeLearningSystem().then(() => {
  console.log('✅ AI Learning System Started Successfully');
}).catch(error => {
  console.warn('⚠️ AI Learning System Warning:', error);
});
