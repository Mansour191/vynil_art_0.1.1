// // C:\Users\Mansour\Desktop\vynilart\frontend\src\main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
// Import Vuetify plugin
import vuetify from './plugins/vuetify'
import App from './App.vue'
import router from './router'
import i18n from './plugins/i18n'
import AITranslation from './plugins/AITranslation'
import store from './store'
import seo from './plugins/seo'
import '@/assets/main.css'
import '@/assets/theme.css'
import AlertService from '@/integration/services/AlertService'
import { useAuthStore } from '@/store/auth'
import AIService from '@/services/AIService'  // Import class directly
import AIMonitorService from '@/services/AIMonitorService'
import PricingService from '@/services/PricingService'  // Import class directly
import ChatService from '@/integration/services/ChatService'
import AILearningService from '@/services/AILearningService'
import apiErrorLogger from '@/services/ApiErrorLogger.js'
import { httpClient } from '@/services/HttpClient.js'
import ApiDebugger from '@/utils/ApiDebugger.js'
import ApiTest from '@/utils/ApiTest.js'

// Import new plugins
import PrimeVuePlugin from '@/plugins/primevue'
import VueUsePlugin from '@/plugins/vueuse'
import MotionPlugin from '@/plugins/motion'
import AutoAnimatePlugin from '@/plugins/autoAnimate'
import { ApolloPlugin } from '@/plugins/apolloPlugin'

// Import icons
import '@fortawesome/fontawesome-free/css/all.min.css'
import '@mdi/font/css/materialdesignicons.min.css'
import 'primeicons/primeicons.css'

const app = createApp(App)
const pinia = createPinia()

// Initialize theme system first
import { useTheme } from '@/composables/useTheme';

console.log('🎬 Starting Vynil Art Application...')

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('🔥 Global Error:', err)
  console.error('📍 Info:', info)

  AlertService.sendAlert({
    type: 'danger',
    severity: 'high',
    title: '⚠️ حدث خطأ غير متوقع',
    message: 'نعتذر، حدث خطأ في النظام. تم تسجيل الخطأ وسنعمل على إصلاحه.',
  })
}

// Install plugins in correct order
app.use(pinia)
app.use(store)
app.use(router)
app.use(i18n)
app.use(AITranslation)
app.use(seo)
app.use(vuetify)
app.use(ApolloPlugin) // Add Apollo plugin
// Only use PrimeVue if not already used
if (!app._context.components && !app._context.directives) {
  app.use(PrimeVuePlugin)
}
app.use(VueUsePlugin)
app.use(MotionPlugin)
app.use(AutoAnimatePlugin)

// Initialize auth store after all plugins are installed
const authStore = useAuthStore()
authStore.initializeAuth()

// Initialize theme
const { initTheme } = useTheme()

// Mount the app
const mountedApp = app.mount('#app')

// Initialize theme after mounting
initTheme()

// Initialize AI Services after app is mounted - COORDINATED INITIALIZATION
console.log('🔍 Starting API Error Logger...')
apiErrorLogger.clearStoredErrors() // Clear old errors on startup
console.log('✅ API Error Logger Initialized')

console.log('🚀 Starting AI Services...')

// Use singleton pattern to prevent concurrent initializations
const aiService = AIService.getInstance()
const pricingService = PricingService.getInstance()
const aiMonitorService = new AIMonitorService()

// AI Service will auto-initialize via singleton constructor
// AIMonitorService will coordinate with singleton instances
console.log('✅ AI Services Coordination Established')

// Initialize Chat Service
console.log('💬 Chat Service Initialized')

// Initialize AI Learning System
console.log('🎓 Starting AI Learning System...')
AILearningService.initializeLearningSystem().then(() => {
  console.log('✅ AI Learning System Started Successfully')
}).catch(error => {
  console.warn('⚠️ AI Learning System Warning:', error)
})

console.log('🎬 Vynil Art Application Started Successfully!')
