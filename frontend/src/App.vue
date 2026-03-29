<template>
    <v-app 
      id="app" 
      :dir="isRTL ? 'rtl' : 'ltr'" 
      :theme="currentTheme"
      class="paclos-app-wrapper"
    >
    <v-progress-linear
      :active="isRouteLoading"
      indeterminate
      fixed
      top
      color="primary"
      height="3"
      z-index="2000"
    ></v-progress-linear>

    <!-- Header يظهر فقط في الصفحات العادية (غير Dashboard) -->
    <v-app-bar
      v-if="showHeader"
      elevation="2"
      color="background"
      scroll-behavior="elevate"
      class="border-b"
      app
    >
      <Header
        @toggle-mobile-menu="mobileMenuOpen = !mobileMenuOpen"
        @change-language="changeLanguage"
      />
    </v-app-bar>

    <v-navigation-drawer
      v-model="mobileMenuOpen"
      temporary
      location="right"
      width="300"
      class="glass-drawer"
    >
      <v-list nav>
        <v-list-item
          v-for="item in mobileNavItems"
          :key="item.path"
          :to="item.path"
          :prepend-icon="item.icon"
          :title="item.name"
          color="primary"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <!-- Footer يظهر فقط في الصفحات العادية (غير Dashboard) -->
    <Footer v-if="showFooter" />
    
    <ChatBot v-if="showChatbot" />
    <div v-if="showChatbot" style="height: 100px; background-color: #f0f0f0;"></div>
    <div style="height: 50px;"></div>
    <div style="height: 100px;"></div>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import { useTheme } from '@/composables/useTheme';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import ChatBot from '@/components/common/FloatingChatbot.vue';

// Composables
const route = useRoute();
const router = useRouter();
const store = useStore();
const { locale } = useI18n();
const { isDark, toggleTheme, themeClass } = useTheme();

// State
const mobileMenuOpen = ref(false);
const isRouteLoading = ref(false);

// Computed
const currentTheme = computed(() => isDark.value ? 'dark' : 'light');
const isRTL = computed(() => locale.value === 'ar');
const showChatbot = computed(() => store.getters['ui/showChatbot'] ?? true);

// تحديد ما إذا كان المسار الحالي هو Dashboard
const isDashboardRoute = computed(() => {
  const path = route.path;
  // التحقق إذا كان المسار يبدأ بـ /dashboard أو /investor
  return path.startsWith('/dashboard') || path.startsWith('/investor');
});

// عرض Header فقط في الصفحات العادية (غير Dashboard)
const showHeader = computed(() => !isDashboardRoute.value);

// عرض Footer فقط في الصفحات العادية (غير Dashboard)
const showFooter = computed(() => !isDashboardRoute.value);

// Mobile nav items
const mobileNavItems = computed(() => [
  { path: '/', name: 'الرئيسية', icon: 'mdi-home' },
  { path: '/gallery', name: 'المعرض', icon: 'mdi-image-multiple' },
  { path: '/about', name: 'من نحن', icon: 'mdi-information' },
  { path: '/contact', name: 'اتصل بنا', icon: 'mdi-phone' },
  { path: '/shop', name: 'المتجر', icon: 'mdi-store' },
  ...(store.getters['auth/isAuthenticated'] 
    ? [{ path: '/dashboard', name: 'لوحة التحكم', icon: 'mdi-view-dashboard' }]
    : [{ path: '/login', name: 'تسجيل الدخول', icon: 'mdi-login' }])
]);

// Methods
const changeLanguage = (lang) => {
  locale.value = lang;
  localStorage.setItem('language', lang);
  document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
};

// Route loading handling
router.beforeEach((to, from, next) => {
  isRouteLoading.value = true;
  next();
});

router.afterEach(() => {
  setTimeout(() => {
    isRouteLoading.value = false;
  }, 300);
});

// Update document direction when language changes
watch(locale, (newLang) => {
  document.documentElement.dir = newLang === 'ar' ? 'rtl' : 'ltr';
});

onMounted(() => {
  // Set initial direction
  document.documentElement.dir = locale.value === 'ar' ? 'rtl' : 'ltr';
});
</script>

<style>
/* Global styles */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}

.glass-drawer {
  background: rgba(10, 10, 10, 0.95) !important;
  backdrop-filter: blur(12px);
  border-left: 1px solid rgba(212, 175, 55, 0.2);
}

[dir="ltr"] .glass-drawer {
  border-left: none;
  border-right: 1px solid rgba(212, 175, 55, 0.2);
}

.border-b {
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}
</style>