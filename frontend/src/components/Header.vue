// @\components\Header.vue
<template>
  <header class="header-wrap">
    <div class="container header-inner">
      <!-- Logo -->
      <div class="site-title">
        <router-link to="/">{{ $t('siteTitle') }}</router-link>
      </div>

      <!-- Desktop Navigation -->
      <ul class="desktop-nav">
        <li>
          <router-link to="/"><i class="fa-solid fa-home"></i> {{ $t('home') }}</router-link>
        </li>
        <li class="has-dropdown">
          <a href="#"
            ><i class="fa-solid fa-th-large"></i> {{ $t('products') }} <i class="fa-solid fa-chevron-down"></i
          ></a>
          <ul class="dropdown-menu">
            <li>
              <router-link to="/furniture"
                ><i class="fa-solid fa-couch"></i> {{ $t('furniture') }}</router-link
              >
            </li>
            <li>
              <router-link to="/doors"
                ><i class="fa-solid fa-door-open"></i> {{ $t('doors') }}</router-link
              >
            </li>
            <li>
              <router-link to="/walls"
                ><i class="fa-solid fa-paint-roller"></i> {{ $t('walls') }}</router-link
              >
            </li>
            <li>
              <router-link to="/ceilings"
                ><i class="fa-solid fa-arrow-up"></i> {{ $t('ceilings') }}</router-link
              >
            </li>
            <li>
              <router-link to="/tiles"
                ><i class="fa-solid fa-border-all"></i> {{ $t('tiles') }}</router-link
              >
            </li>
            <li>
              <router-link to="/kitchens"
                ><i class="fa-solid fa-utensils"></i> {{ $t('kitchens') }}</router-link
              >
            </li>
            <li>
              <router-link to="/cars"><i class="fa-solid fa-car"></i> {{ $t('cars') }}</router-link>
            </li>
          </ul>
        </li>
        <li>
          <router-link to="/gallery"><i class="fa-solid fa-images"></i> {{ $t('gallery') }}</router-link>
        </li>
        <li>
          <router-link to="/about"><i class="fa-solid fa-users"></i> {{ $t('about') }}</router-link>
        </li>
        <li>
          <router-link to="/contact"
            ><i class="fa-solid fa-phone-alt"></i> {{ $t('contact') }}</router-link
          >
        </li>
      </ul>

      <!-- Header Actions -->
      <div class="header-actions">
        <!-- أيقونة المفضلة -->
        <router-link 
          to="/wishlist" 
          class="header-icon" 
          :title="$t('wishlist')"
          :aria-label="$t('wishlist') + ' (' + wishlistCount + ')'"
        >
          <i class="fa-solid fa-heart" :class="{ 'has-items': wishlistCount > 0 }" aria-hidden="true"></i>
          <span v-if="wishlistCount > 0" class="icon-badge">{{ wishlistCount }}</span>
        </router-link>

        <!-- أيقونة الإشعارات -->
        <NotificationsDropdown />

        <!-- Theme Switcher -->
        <button 
          class="theme-btn" 
          @click="toggleTheme" 
          :title="$t('toggleTheme')"
          :aria-label="$t('toggleTheme')"
        >
          <i :class="isDarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'" aria-hidden="true"></i>
        </button>

        <!-- Language Switcher -->
        <LanguageSwitcher @change-language="changeLanguage" />

        <!-- Login Button -->
        <button
          v-if="!isAuthenticated"
          class="login-icon"
          @click="handleLoginClick"
          :aria-label="t('login')"
        >
          <i class="fa-solid fa-user-circle" aria-hidden="true"></i>
          <span class="login-text">{{ t('login') }}</span>
        </button>

        <router-link
          v-else
          :to="authStore.role === 'admin' ? '/dashboard' : (authStore.role === 'investor' ? '/investor' : '/profile')"
          class="login-icon logged-in"
          :aria-label="userDisplayName"
        >
          <i class="fa-solid fa-check-circle" aria-hidden="true"></i>
          <span class="login-text">{{ userDisplayName }}</span>
        </router-link>

        <!-- Mobile Menu Toggle -->
        <button 
          class="menu-toggle" 
          @click="emit('toggle-mobile-menu')"
          :aria-label="t('openMenu')"
        >
          <i class="fa-solid fa-bars" aria-hidden="true"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { useI18n } from 'vue-i18n';
import NotificationsDropdown from './NotificationsDropdown.vue';
import LanguageSwitcher from './common/LanguageSwitcher.vue';

const props = defineProps({
  isDarkMode: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['toggle-mobile-menu', 'change-language', 'toggle-theme']);

const router = useRouter();
const authStore = useAuthStore();
const { t } = useI18n();

// State
const activeMobileDropdown = ref(null);

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUser = computed(() => authStore.user);
const wishlistCount = computed(() => 0); // TODO: Implement wishlist count in DRF Auth Store

const userDisplayName = computed(() => {
  if (authStore.user) {
    return authStore.user.firstName || authStore.user.username || 'مستخدم';
  }
  return 'ضيف';
});

// Methods
const handleLoginClick = () => {
  console.log('✅ Header: تم النقر على زر تسجيل الدخول - التوجيه لصفحة الدخول المتقدمة');
  router.push('/auth');
};

const changeLanguage = (lang) => {
  emit('change-language', lang);
};

const toggleTheme = () => {
  emit('toggle-theme');
};

const toggleMobileDropdown = (id) => {
  activeMobileDropdown.value = activeMobileDropdown.value === id ? null : id;
};

// Initialize auth store on mount
onMounted(() => {
  authStore.initializeAuth();
});
</script>

<style scoped>
.header-wrap {
  background: rgba(15, 15, 15, 0.98);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 50;
  border-bottom: 1px solid var(--border-subtle);
  width: 100%;
}

body.light-mode .header-wrap {
  background: rgba(255, 255, 255, 0.98);
  border-bottom: 1px solid var(--border-subtle);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height, 80px);
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Logo */
.site-title {
  font-size: 1.5rem;
  font-weight: 800;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.site-title a {
  color: transparent;
}

/* Desktop Navigation */
.desktop-nav {
  display: flex;
  list-style: none;
  gap: 30px;
  margin: 0;
  padding: 0;
}

.desktop-nav a {
  color: var(--text-muted, #888);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.desktop-nav a:hover,
.desktop-nav a.router-link-active {
  color: var(--gold-primary, #d4af37);
}

@media (max-width: 992px) {
  .desktop-nav {
    display: none;
  }
}

/* Dropdown */
.has-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: var(--bg-card, #1a1a2e);
  min-width: 260px;
  border-radius: 15px;
  box-shadow: var(--shadow-soft), 0 10px 30px rgba(212, 175, 55, 0.1);
  padding: 12px 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px) scale(0.95);
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  border: 1px solid var(--border-subtle);
  border-top: 2px solid var(--gold-primary);
  list-style: none;
  z-index: 100;
  backdrop-filter: blur(10px);
}

[dir="rtl"] .dropdown-menu {
  left: auto;
  right: 0;
}

.has-dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(10px) scale(1);
}

.dropdown-menu::before {
  content: '';
  position: absolute;
  top: -8px;
  left: 30px;
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid var(--gold-primary);
}

[dir="rtl"] .dropdown-menu::before {
  left: auto;
  right: 30px;
}

.dropdown-menu li {
  margin: 4px 0;
}

.dropdown-menu a {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: 10px;
  color: var(--text-main, #fff);
  transition: all 0.3s;
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.dropdown-menu a:hover {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-primary, #d4af37);
  transform: translateX(5px);
}

[dir="rtl"] .dropdown-menu a:hover {
  transform: translateX(-5px);
}

.dropdown-menu i {
  width: 20px;
  text-align: center;
  color: var(--gold-primary, #d4af37);
  font-size: 1.1rem;
}

.fa-chevron-down {
  font-size: 0.7rem;
  transition: transform 0.3s ease;
  margin-left: 5px;
}

[dir="rtl"] .fa-chevron-down {
  margin-left: 0;
  margin-right: 5px;
}

.has-dropdown:hover .fa-chevron-down {
  transform: rotate(180deg);
}

/* Header Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-icon, .theme-btn {
  position: relative;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface, rgba(255,255,255,0.05));
  border: 1px solid var(--border-subtle);
  border-radius: 50%;
  color: var(--gold-primary, #d4af37);
  transition: all 0.3s;
  cursor: pointer;
  text-decoration: none;
}

.header-icon:hover, .theme-btn:hover {
  border-color: var(--gold-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
  background: rgba(212, 175, 55, 0.1);
}

.icon-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  font-size: 0.7rem;
  padding: 2px 5px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  font-weight: 700;
  border: 2px solid var(--bg-deep);
}

/* Language Switcher */
.language-switcher {
  position: relative;
}

.lang-btn {
  background: var(--bg-surface, rgba(255,255,255,0.05));
  border: 1px solid var(--border-subtle);
  color: var(--text-main, #fff);
  padding: 8px 15px;
  border-radius: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.lang-btn:hover {
  border-color: var(--gold-primary);
  background: rgba(212, 175, 55, 0.1);
}

.lang-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background: var(--bg-card, #1a1a2e);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  min-width: 150px;
  padding: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all 0.3s;
  z-index: 100;
}

[dir="rtl"] .lang-dropdown {
  right: auto;
  left: 0;
}

.lang-dropdown.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.lang-option {
  padding: 10px 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.lang-option:hover {
  background: rgba(212, 175, 55, 0.1);
  color: var(--gold-primary);
}

.lang-option.active {
  background: var(--gold-primary);
  color: var(--bg-deep);
}

/* Auth Button */
.login-icon {
  background: var(--gold-gradient);
  border: none;
  padding: 8px 18px;
  border-radius: 30px;
  color: #1a1a2e;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  text-decoration: none;
}

.login-icon:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
}

.login-icon.logged-in {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main, #fff);
  border: 1px solid var(--border-subtle);
}

.login-icon.logged-in:hover {
  border-color: var(--gold-primary);
  color: var(--gold-primary);
}

/* Mobile Menu Toggle */
.menu-toggle {
  background: none;
  border: 1px solid var(--border-subtle);
  color: var(--gold-primary);
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
}

@media (max-width: 992px) {
  .menu-toggle {
    display: block;
  }
  .login-text {
    display: none;
  }
  .login-icon {
    padding: 8px;
    border-radius: 50%;
  }
}
</style>
