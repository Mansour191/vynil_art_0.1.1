// @\App.vue
<template>
  <div id="app" :dir="isRTL ? 'rtl' : 'ltr'" :class="{ 'light-mode': isLightMode }">
    <ErrorBoundary>
      <!-- Header - يظهر فقط في الصفحات العامة (ليس في Dashboard) -->
      <Header
        v-if="!isDashboardRoute"
        :isDarkMode="isLightMode"
        @toggle-theme="toggleTheme"
        @toggle-mobile-menu="toggleMobileMenu"
        @change-language="changeLanguage"
      />

      <!-- Mobile Menu - يظهر فقط في الصفحات العامة -->
      <template v-if="!isDashboardRoute">
        <div class="mobile-menu" :class="{ open: mobileMenuOpen }">
          <div class="menu-header">
            <span class="menu-logo">{{ $t('siteTitle') }}</span>
            <button class="close-menu" @click="toggleMobileMenu">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>

          <ul class="mobile-nav">
            <li>
              <router-link to="/" @click="toggleMobileMenu">
                <i class="fa-solid fa-home"></i> {{ $t('home') }}
              </router-link>
            </li>
            <li class="has-dropdown">
              <a href="#" @click.prevent="toggleMobileDropdown($event)">
                <i class="fa-solid fa-th-large"></i> {{ $t('products') }}
                <i class="fa-solid fa-chevron-down chevron"></i>
              </a>
              <ul class="mobile-dropdown">
                <li>
                  <router-link to="/furniture" @click="toggleMobileMenu">
                    <i class="fa-solid fa-couch"></i> {{ $t('furniture') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/doors" @click="toggleMobileMenu">
                    <i class="fa-solid fa-door-open"></i> {{ $t('doors') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/walls" @click="toggleMobileMenu">
                    <i class="fa-solid fa-paint-roller"></i> {{ $t('walls') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/ceilings" @click="toggleMobileMenu">
                    <i class="fa-solid fa-arrow-up"></i> {{ $t('ceilings') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/tiles" @click="toggleMobileMenu">
                    <i class="fa-solid fa-border-all"></i> {{ $t('tiles') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/kitchens" @click="toggleMobileMenu">
                    <i class="fa-solid fa-utensils"></i> {{ $t('kitchens') }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/cars" @click="toggleMobileMenu">
                    <i class="fa-solid fa-car"></i> {{ $t('cars') }}
                  </router-link>
                </li>
              </ul>
            </li>
            <li>
              <router-link to="/gallery" @click="toggleMobileMenu">
                <i class="fa-solid fa-images"></i> {{ $t('gallery') }}
              </router-link>
            </li>
            <li>
              <router-link to="/about" @click="toggleMobileMenu">
                <i class="fa-solid fa-users"></i> {{ $t('about') }}
              </router-link>
            </li>
            <li>
              <router-link to="/contact" @click="toggleMobileMenu">
                <i class="fa-solid fa-phone-alt"></i> {{ $t('contact') }}
              </router-link>
            </li>
            <!-- Mobile Theme Switcher -->
            <li>
              <a href="#" @click.prevent="toggleTheme">
                <i :class="isLightMode ? 'fa-solid fa-moon' : 'fa-solid fa-sun'"></i>
                {{ $t('toggleTheme') }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Overlay -->
        <div class="overlay" :class="{ show: mobileMenuOpen }" @click="toggleMobileMenu"></div>
      </template>

      <!-- Main Content -->
      <main>
        <router-view></router-view>
      </main>

      <!-- Footer - يظهر فقط في الصفحات العامة -->
      <Footer v-if="!isDashboardRoute" />

      <!-- إشعارات التواست -->
      <Toast />
      <FloatingChatbot />
    </ErrorBoundary>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import Toast from '@/components/common/Toast.vue';
import FloatingChatbot from '@/components/common/FloatingChatbot.vue';
import { ERPNextService } from '@/integration';
import ErrorBoundary from '@/components/ErrorBoundary.vue';
import { useAuthStore } from '@/store/auth';

export default {
  name: 'App',
  components: {
    ErrorBoundary,
    Header,
    Footer,
    Toast,
    FloatingChatbot,
  },
  data() {
    return {
      mobileMenuOpen: false,
      isLightMode: false,
      result: null,
    };
  },

  computed: {
    currentLocale() {
      return this.$i18n.locale;
    },
    isRTL() {
      return this.currentLocale === 'ar';
    },
    currentLang() {
      return this.currentLocale;
    },
    // يخفي الـ Header والـ Footer في لوحات التحكم (Dashboard و Investor)
    isDashboardRoute() {
      const path = this.$route.path;
      return path.startsWith('/dashboard') || path.startsWith('/investor');
    },
  },

  methods: {
    ...mapActions(['logout']),

    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
      document.body.style.overflow = this.mobileMenuOpen ? 'hidden' : '';
    },

    toggleMobileDropdown(event) {
      const parent = event.currentTarget.parentElement;
      parent.classList.toggle('active');
      const dropdown = parent.querySelector('.mobile-dropdown');
      if (dropdown) dropdown.classList.toggle('show');
    },

    changeLanguage(lang) {
      this.$i18n.locale = lang;
      localStorage.setItem('language', lang);
      document.documentElement.lang = lang;
      document.body.dir = lang === 'ar' ? 'rtl' : 'ltr';
    },

    toggleTheme() {
      this.isLightMode = !this.isLightMode;
      document.body.classList.toggle('light-mode', this.isLightMode);
      localStorage.setItem('theme', this.isLightMode ? 'light' : 'dark');
    },

    async testERPNext() {
      this.result = await ERPNextService.testConnection();
    },
    async getProducts() {
      this.result = await ERPNextService.getProducts();
    },
    async createTestProduct() {
      this.result = await ERPNextService.createProduct({
        name: 'منتج تجريبي',
        sku: 'TEST-001',
        price: 99,
        category: 'walls',
        description: 'هذا منتج للتجربة',
      });
    },
  },
  mounted() {
    // استرجاع تفضيل المستخدم للغة
    const savedLang = localStorage.getItem('language') || 'ar';
    this.$i18n.locale = savedLang;
    document.documentElement.lang = savedLang;
    document.body.dir = savedLang === 'ar' ? 'rtl' : 'ltr';

    // استرجاع تفضيل المستخدم للوضع
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      this.isLightMode = true;
      document.body.classList.add('light-mode');
    } else {
      this.isLightMode = false;
      document.body.classList.remove('light-mode');
    }
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap');
@import '@/assets/theme.css';

:root {
  /* الوضع الداكن (الافتراضي) */
  --bg-deep: #0f0f0f;
  --bg-dark: #1a1a1a;
  --bg-card: #222222;
  --bg-surface: #2a2a2a;
  --text-primary: #ffffff;
  --text-secondary: #e0e0e0;
  --text-muted: #a0a0a0;
  --text-dim: #707070;
  --gold-primary: #d4af37;
  --gold-light: #ffd700;
  --gold-dim: #b8860b;
  --gold-gradient: linear-gradient(135deg, #d4af37 0%, #ffd700 50%, #d4af37 100%);
  --border-subtle: #333333;
  --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.4);
  --shadow-gold: 0 4px 20px rgba(212, 175, 55, 0.2);
  --header-height: 80px;
  --mobile-header-height: 60px;

  /* ألوان جديدة للقائمة المنسدلة */
  --dropdown-bg: rgba(26, 26, 26, 0.95);
  --dropdown-border: rgba(212, 175, 55, 0.3);
  --dropdown-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
  --dropdown-hover-bg: rgba(212, 175, 55, 0.1);
  --dropdown-item-hover: rgba(212, 175, 55, 0.05);
}

/* تحسينات إضافية للخط */
#app {
  font-family: var(--font-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* تحسين العناوين في Dashboard */
.dashboard-main h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  background: linear-gradient(135deg, #fff, var(--gold-1));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.dashboard-main h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

.dashboard-main h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  color: var(--gold-1);
}

/* تحسين النصوص في البطاقات */
.stat-value {
  font-family: var(--font-numbers);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
}

.stat-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* تحسين الجداول */
.orders-table th {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.orders-table td {
  font-size: var(--text-sm);
}

.customer-name {
  font-weight: var(--font-semibold);
}

.customer-email {
  font-size: var(--text-xs);
}

/* تحسين الأرقام */
.order-id-badge,
.amount,
.total-amount {
  font-family: var(--font-numbers);
  font-weight: var(--font-medium);
}

/* تحسين حالة الطلب */
.status-badge {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  letter-spacing: 0.3px;
}

/* تحسين أزرار الإجراءات */
.action-btn {
  font-size: var(--text-base);
}

.action-menu button {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

/* تحسين الفلاتر */
.filter-select {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

/* تحسين النوافذ المنبثقة */
.modal-header h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
}

.detail-card h3 {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* تحسين Pagination */
.page-btn {
  font-weight: var(--font-medium);
}

.pagination-info {
  font-size: var(--text-sm);
}

/* تحسين حالة عدم وجود بيانات */
.no-data-content h4 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
}

.no-data-content p {
  font-size: var(--text-base);
}

/* تأثيرات حركية للخط */
@keyframes textGlow {
  0%,
  100% {
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
  }
  50% {
    text-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
  }
}

.glow-text {
  animation: textGlow 3s ease infinite;
}

/* الوضع الفاتح */
body.light-mode {
  --bg-deep: #f5f5f5;
  --bg-dark: #ffffff;
  --bg-card: #ffffff;
  --bg-surface: #f0f0f0;
  --text-primary: #333333;
  --text-secondary: #555555;
  --text-muted: #777777;
  --text-dim: #999999;
  --gold-primary: #b8860b;
  --gold-light: #d4af37;
  --gold-dim: #8b6910;
  --gold-gradient: linear-gradient(135deg, #b8860b 0%, #d4af37 50%, #b8860b 100%);
  --border-subtle: #dddddd;
  --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.1);
  --shadow-gold: 0 4px 20px rgba(184, 134, 11, 0.2);
  --dropdown-bg: rgba(255, 255, 255, 0.95);
  --dropdown-border: rgba(184, 134, 11, 0.3);
  --dropdown-shadow: 0 10px 30px rgba(184, 134, 11, 0.1);
  --dropdown-hover-bg: rgba(184, 134, 11, 0.1);
  --dropdown-item-hover: rgba(184, 134, 11, 0.05);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Cairo', sans-serif;
  background: var(--bg-deep);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  width: 100%;
  transition: background-color 0.3s ease, color 0.3s ease;
}

body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 20% 20%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(212, 175, 55, 0.03) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

a {
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.container {
  width: 100%;
  padding: 0 15px;
  margin: 0 auto;
}

/* Mobile Menu Styles */
.mobile-menu {
  position: fixed;
  top: 0;
  right: -100%;
  width: 85%;
  max-width: 340px;
  height: 100vh;
  background: var(--bg-dark);
  z-index: 1000;
  padding: 20px;
  transition: right 0.3s ease;
  overflow-y: auto;
  border-left: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-soft);
  -webkit-overflow-scrolling: touch;
}

[dir='ltr'] .mobile-menu {
  right: auto;
  left: -100%;
  border-left: none;
  border-right: 1px solid var(--border-subtle);
}

[dir='ltr'] .mobile-menu.open {
  left: 0;
  right: auto;
}

.mobile-menu.open {
  right: 0;
}

.menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-subtle);
}

.menu-logo {
  font-size: 1.2rem;
  font-weight: 700;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.close-menu {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface);
  border: none;
  color: var(--gold-primary);
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s;
  flex-shrink: 0;
}

.close-menu:hover {
  background: var(--gold-primary);
  color: var(--bg-deep);
  transform: rotate(90deg);
}

.mobile-nav {
  list-style: none;
  margin-bottom: 20px;
}

.mobile-nav li {
  margin-bottom: 5px;
}

.mobile-nav li a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  border-radius: 10px;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.3s;
  font-size: 0.95rem;
  cursor: pointer;
}

.mobile-nav li a i {
  width: 20px;
  font-size: 1.1rem;
  color: var(--gold-primary);
  transition: all 0.3s;
  text-align: center;
}

.mobile-nav li a:hover {
  background: var(--bg-surface);
  color: var(--text-primary);
}

.mobile-dropdown {
  list-style: none;
  padding-right: 30px;
  margin: 2px 0 4px;
  display: none;
}

[dir='ltr'] .mobile-dropdown {
  padding-right: 0;
  padding-left: 30px;
}

.mobile-dropdown.show {
  display: block;
}

.mobile-dropdown li a {
  padding: 10px 15px;
  font-size: 0.9rem;
  background: var(--bg-deep);
  border-radius: 8px;
  margin-bottom: 2px;
}

.has-dropdown > a {
  justify-content: space-between;
}

.has-dropdown > a .chevron {
  transition: transform 0.3s;
  font-size: 0.9rem;
}

.has-dropdown.active > a .chevron {
  transform: rotate(180deg);
}

/* Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
}

.overlay.show {
  opacity: 1;
  visibility: visible;
}

/* Media Queries */
@media (min-width: 768px) {
  .container {
    max-width: 1200px;
    padding: 0 30px;
  }
}

@media (max-width: 480px) {
  .login-text {
    display: none;
  }
}

/* أيقونات احتياطية */
i.fa, i.fas, i.far, i.fal, i.fab {
  font-family: 'Font Awesome 6 Free', 'Font Awesome 6 Brands', sans-serif !important;
  font-weight: 900;
}

i.mdi {
  font-family: 'Material Design Icons', sans-serif !important;
}

/* تأكد من تحميل الخطوط */
@font-face {
  font-family: 'Font Awesome 6 Free';
  src: url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-solid-900.woff2') format('woff2');
  font-weight: 900;
  font-style: normal;
}

@font-face {
  font-family: 'Font Awesome 6 Brands';
  src: url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/webfonts/fa-brands-400.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
</style>
