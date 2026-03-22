// src\views\dashboard\DashboardLayout.vue
<template>
  <div class="dashboard-layout">
    <!-- جسيمات متحركة في الخلفية -->
    <div class="particles">
      <div v-for="n in 30" :key="n" class="particle" :style="getParticleStyle(n)"></div>
    </div>

    <div class="dashboard-container">
      <!-- الشريط الجانبي الفاخر -->
      <aside class="dashboard-sidebar" :class="{ collapsed: isSidebarCollapsed }">
        <div class="sidebar-glow"></div>

        <div class="sidebar-header">
          <div class="logo-wrapper">
            <i class="fa-solid fa-paint-roller logo-icon"></i>
            <div class="logo-text-wrapper">
              <h2 class="logo-text">Vinyl<span>Art</span></h2>
              <span class="logo-badge">PRO</span>
            </div>
          </div>
        </div>

        <nav class="sidebar-nav">
          <div v-for="section in navSections" :key="section.title" class="nav-section">
            <p class="nav-section-title" v-if="!isSidebarCollapsed">{{ section.title }}</p>
            <router-link
              v-for="item in section.items"
              :key="item.path"
              :to="item.path"
              class="nav-item"
              active-class="active"
              @click="handleNavClick"
            >
              <div class="nav-icon-wrapper">
                <i :class="item.icon" class="nav-icon"></i>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">{{ item.title }}</span>
              <span v-if="item.badge && !isSidebarCollapsed" class="nav-badge">{{
                item.badge
              }}</span>
            </router-link>
          </div>
        </nav>

        <div class="sidebar-footer">
          <div class="user-card" v-if="!isSidebarCollapsed">
            <img :src="userAvatar" alt="User" class="user-avatar" />
            <div class="user-info">
              <p class="user-name">{{ userName }}</p>
              <p class="user-role">{{ userRoleText }}</p>
            </div>
            <div class="user-status"></div>
          </div>

          <button class="sidebar-toggle" @click="toggleSidebar">
            <i :class="isSidebarCollapsed ? 'fa-solid fa-chevron-right' : 'fa-solid fa-chevron-left'"></i>
          </button>
        </div>
      </aside>

      <!-- المحتوى الرئيسي -->
      <main class="dashboard-main">
        <!-- الهيدر المتطور -->
        <header class="dashboard-header" :class="{ 'header-scrolled': isHeaderScrolled }">
          <div class="header-left">
            <button class="mobile-menu-btn" @click="toggleMobileMenu">
              <i class="fa-solid fa-bars"></i>
            </button>

            <div class="page-title">
              <h1>{{ pageTitle }}</h1>
              <div class="breadcrumbs">
                <router-link to="/dashboard">الرئيسية</router-link>
                <i class="fa-solid fa-chevron-left breadcrumb-icon"></i>
                <span>{{ breadcrumbTitle }}</span>
              </div>
            </div>
          </div>

          <div class="header-right">
            <div class="header-search">
              <i class="fa-solid fa-search search-icon"></i>
              <input
                type="text"
                placeholder="بحث..."
                v-model="searchQuery"
                @focus="isSearchFocused = true"
                @blur="isSearchFocused = false"
                :class="{ focused: isSearchFocused }"
              />
            </div>

            <div class="header-actions">
              <LanguageSwitcher />
              <AlertCenter />
              <CurrencySelector />
              <button class="action-btn notifications-btn" @click="toggleNotifications">
                <i class="fa-solid fa-bell"></i>
                <span class="badge">3</span>
              </button>

              <button class="action-btn messages-btn" @click="toggleMessages">
                <i class="fa-solid fa-envelope"></i>
                <span class="badge">5</span>
                <span class="btn-glow"></span>
              </button>

              <div class="user-menu" @click="toggleUserMenu">
                <img :src="userAvatar" alt="User" class="user-avatar" />
                <i class="fa-solid fa-chevron-down"></i>

                <transition name="slide-down">
                  <div class="user-dropdown" v-if="showUserMenu" @click.stop>
                    <div class="dropdown-header">
                      <img :src="userAvatar" alt="User" />
                      <div>
                        <p class="dropdown-user-name">{{ userName }}</p>
                        <p class="dropdown-user-email">{{ authStore.user?.email || 'user@vinylart.com' }}</p>
                      </div>
                    </div>

                    <div class="dropdown-menu">
                      <router-link to="/dashboard/profile">
                        <i class="fa-solid fa-user"></i>
                        <span>الملف الشخصي</span>
                      </router-link>
                      <router-link to="/dashboard/settings">
                        <i class="fa-solid fa-cog"></i>
                        <span>الإعدادات</span>
                      </router-link>
                      <!-- 👇 أضف الرابط الجديد هنا -->
                      <router-link to="/dashboard/integration/settings">
                        <i class="fa-solid fa-plug"></i>
                        <span>إعدادات ERPNext</span>
                      </router-link>
                      <div class="dropdown-divider"></div>
                      <button @click="logout">
                        <i class="fa-solid fa-sign-out-alt"></i>
                        <span>تسجيل خروج</span>
                      </button>
                    </div>
                  </div>
                </transition>
              </div>
            </div>
          </div>
        </header>

        <!-- محتوى الصفحة -->
        <div class="dashboard-content">
          <ErrorBoundary>
            <transition name="page" mode="out-in">
              <router-view></router-view>
            </transition>
          </ErrorBoundary>
        </div>
      </main>
    </div>

    <!-- قائمة الموبايل -->
    <transition name="slide-right">
      <div class="mobile-sidebar" v-if="mobileMenuOpen">
        <div class="mobile-sidebar-header">
          <h2 class="logo-text">Vinyl<span>Art</span></h2>
          <button class="close-mobile-menu" @click="toggleMobileMenu">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
        
        <nav class="sidebar-nav">
          <div v-for="section in navSections" :key="section.title" class="nav-section">
            <p class="nav-section-title">{{ section.title }}</p>
            <router-link
              v-for="item in section.items"
              :key="item.path"
              :to="item.path"
              class="nav-item"
              active-class="active"
              @click="handleNavClick"
            >
              <div class="nav-icon-wrapper">
                <i :class="item.icon" class="nav-icon"></i>
              </div>
              <span class="nav-text">{{ item.title }}</span>
              <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
            </router-link>
          </div>
        </nav>
        
        <div class="mobile-sidebar-footer">
          <div class="user-card">
            <img :src="userAvatar" alt="User" class="user-avatar" />
            <div class="user-info">
              <p class="user-name">{{ userName }}</p>
              <p class="user-role">{{ userRoleText }}</p>
            </div>
          </div>
          <button class="btn btn-logout-mobile" @click="logout">
            <i class="fa-solid fa-sign-out-alt"></i>
            <span>خروج</span>
          </button>
        </div>
      </div>
    </transition>

    <!-- طبقة التعتيم -->
    <transition name="fade">
      <div class="mobile-overlay" v-if="mobileMenuOpen" @click="toggleMobileMenu"></div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import AlertCenter from '@/components/AlertCenter.vue';
import CurrencySelector from '@/components/CurrencySelector.vue';
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue';
import ErrorBoundary from '@/components/ErrorBoundary.vue';

const router = useRouter();
const route = useRoute();

// State
const isSidebarCollapsed = ref(false);
const mobileMenuOpen = ref(false);
const showUserMenu = ref(false);
const isHeaderScrolled = ref(false);
const isSearchFocused = ref(false);
const searchQuery = ref('');

const authStore = useAuthStore();

const navSections = computed(() => {
  const common = [
    {
      title: 'الرئيسية',
      items: [
        { path: authStore.isAdmin ? '/dashboard' : '/investor', icon: 'fa-solid fa-home', title: 'لوحة التحكم' },
      ],
    }
  ];

  if (authStore.isAdmin) {
    return [
      ...common,
      {
        title: 'الإدارة',
        items: [
          { path: '/dashboard/products', icon: 'fa-solid fa-box', title: 'المنتجات', badge: '12' },
          { path: '/dashboard/orders', icon: 'fa-solid fa-shopping-cart', title: 'الطلبات', badge: '5' },
          { path: '/dashboard/users', icon: 'fa-solid fa-users', title: 'المستخدمين' },
          { path: '/dashboard/designs', icon: 'fa-solid fa-paint-brush', title: 'التصاميم' },
          { path: '/dashboard/integration', icon: 'fa-solid fa-plug', title: 'لوحة التكامل' },
          { path: '/dashboard/settings', icon: 'fa-solid fa-cog', title: 'الإعدادات' },
        ],
      },
      {
        title: 'التحليلات',
        items: [
          { path: '/dashboard/analytics', icon: 'fa-solid fa-chart-pie', title: 'التحليلات المتقدمة' },
          { path: '/dashboard/forecasting', icon: 'fa-solid fa-chart-line', title: 'توقعات المبيعات' },
        ],
      },
      {
        title: 'ركن الممولين',
        items: [
          { path: '/investor', icon: 'fa-solid fa-external-link-alt', title: 'منصة الممولين' },
        ],
      },
    ];
  }

  if (authStore.role === 'investor') {
    return [
      ...common,
      {
        title: 'ركن الممولين',
        items: [
          { path: '/investor', icon: 'fa-solid fa-chart-line', title: 'لوحة الممول الرئيسية' },
          { path: '/investor/reports', icon: 'fa-solid fa-file-invoice-dollar', title: 'التقارير المالية للممول' },
          { path: '/investor/ai-insights', icon: 'fa-solid fa-brain', title: 'تحليلات AI للممول' },
        ],
      },
    ];
  }

  return common;
});

// Computed
const pageTitle = computed(() => route.meta?.title || 'لوحة التحكم');
const breadcrumbTitle = computed(() => route.meta?.title || '');
const userName = computed(() => {
  const user = authStore.user;
  if (user?.firstName && user?.lastName) {
    return `${user.firstName} ${user.lastName}`;
  } else if (user?.firstName) {
    return user.firstName;
  } else if (user?.lastName) {
    return user.lastName;
  } else if (user?.username) {
    return user.username;
  } else {
    return 'مستخدم';
  }
});
const userAvatar = computed(() => `https://ui-avatars.com/api/?name=${userName.value}&background=d4af37&color=fff&size=100`);
const userRoleText = computed(() => {
  const roles = { admin: 'مدير النظام', investor: 'ممول استراتيجي', customer: 'عميل مميز' };
  return roles[authStore.role] || 'زائر';
});

// Methods
const getParticleStyle = (n) => {
  return {
    left: Math.random() * 100 + '%',
    animationDelay: Math.random() * 20 + 's',
    animationDuration: 15 + Math.random() * 10 + 's',
    width: Math.random() * 3 + 1 + 'px',
    height: Math.random() * 3 + 1 + 'px',
    background: `rgba(212, 175, 55, ${0.2 + Math.random() * 0.3})`,
    filter: `blur(${Math.random() * 2}px)`,
  };
};

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
  localStorage.setItem('sidebarCollapsed', isSidebarCollapsed.value);
};

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const toggleNotifications = () => {
  console.log('Toggle notifications');
};

const toggleMessages = () => {
  console.log('Toggle messages');
};

const handleNavClick = () => {
  if (mobileMenuOpen.value) {
    mobileMenuOpen.value = false;
  }
};

const logout = () => {
  authStore.logout();
  router.push('/');
};

const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 50;
};

const handleClickOutside = (event) => {
  if (!event.target.closest('.user-menu')) {
    showUserMenu.value = false;
  }
};

// Lifecycle
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  document.addEventListener('click', handleClickOutside);
  const saved = localStorage.getItem('sidebarCollapsed');
  if (saved) isSidebarCollapsed.value = saved === 'true';
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
  document.removeEventListener('click', handleClickOutside);
});

// Watch
watch(isSidebarCollapsed, (val) => {
  localStorage.setItem('sidebarCollapsed', val);
});
</script>

<style scoped>
@import '@/assets/theme.css';
/* تحسينات الخط في DashboardLayout */

/* تحسين الشعار */
.logo-text {
  font-family: var(--font-heading);
  font-size: var(--text-2xl);
  font-weight: var(--font-black);
  letter-spacing: -0.02em;
}

.logo-text span {
  font-weight: var(--font-extrabold);
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* تحسين القائمة */
.nav-item {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.nav-section-title {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* تحسين معلومات المستخدم */
.user-name {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
}

.user-role {
  font-size: var(--text-xs);
  font-weight: var(--font-normal);
}

/* تحسين عنوان الصفحة */
.page-title h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
}

.breadcrumbs {
  font-size: var(--text-sm);
}

/* تحسين البحث */
.header-search input {
  font-size: var(--text-sm);
}

/* تحسين القائمة المنسدلة */
.dropdown-user-name {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
}

.dropdown-user-email {
  font-size: var(--text-xs);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-layout {
  min-height: 100vh;
  background: var(--bg-deep);
  font-family: 'Cairo', sans-serif;
  position: relative;
  overflow: hidden;
}

/* جسيمات الخلفية */
.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  border-radius: 50%;
  animation: floatParticle 20s infinite linear;
  opacity: 0;
}

@keyframes floatParticle {
  0% {
    transform: translateY(100vh) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100px) translateX(100px) rotate(360deg);
    opacity: 0;
  }
}

.dashboard-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

/* ===== الشريط الجانبي الفاخر ===== */
.dashboard-sidebar {
  width: 300px;
  background: var(--bg-sidebar);
  border-left: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  transition: var(--transition-bounce);
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  z-index: 100;
  box-shadow: var(--shadow-xl);
  backdrop-filter: blur(10px);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--gold-1) var(--bg-secondary);
}

.dashboard-sidebar::-webkit-scrollbar {
  width: 5px;
}

.dashboard-sidebar::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.dashboard-sidebar::-webkit-scrollbar-thumb {
  background: var(--gold-1);
  border-radius: 10px;
}

.dashboard-sidebar.collapsed {
  width: 90px;
}

/* تأثير التوهج على الشريط الجانبي */
.sidebar-glow {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 0% 50%, var(--gold-glow), transparent 70%);
  pointer-events: none;
  opacity: 0.1;
  animation: glowPulse 4s ease infinite;
}

@keyframes glowPulse {
  0%,
  100% {
    opacity: 0.1;
  }
  50% {
    opacity: 0.2;
  }
}

/* الهيدر */
.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid var(--border-light);
  position: relative;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  font-size: 2.2rem;
  color: var(--gold-1);
  animation: logoFloat 3s ease infinite;
  filter: drop-shadow(var(--gold-glow));
}

@keyframes logoFloat {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-5px) rotate(5deg);
  }
}

.logo-text-wrapper {
  transition: opacity 0.3s;
}

.collapsed .logo-text-wrapper {
  opacity: 0;
  width: 0;
}

.logo-text {
  font-size: 1.6rem;
  font-weight: 800;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.logo-text span {
  background: none;
  -webkit-text-fill-color: var(--gold-1);
  font-weight: 900;
}

.logo-badge {
  position: absolute;
  top: 20px;
  right: 70px;
  background: var(--gold-gradient);
  color: var(--bg-deep);
  font-size: 0.6rem;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 700;
  letter-spacing: 1px;
  animation: badgePulse 2s ease infinite;
}

@keyframes badgePulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

/* القائمة */
.sidebar-nav {
  flex: 1;
  padding: 25px 15px;
}

.nav-section {
  margin-bottom: 30px;
}

.nav-section-title {
  color: var(--text-dim);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 15px;
  padding-right: 15px;
  opacity: 0.8;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 16px;
  margin-bottom: 8px;
  transition: var(--transition-smooth);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: var(--gold-gradient);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  opacity: 0.1;
}

.nav-item:hover::before {
  width: 300px;
  height: 300px;
}

.nav-item:hover {
  transform: translateX(-5px);
  color: var(--gold-1);
}

.nav-item.active {
  background: var(--gold-gradient-soft);
  border: 1px solid var(--border-glow);
  box-shadow: var(--shadow-gold);
  color: var(--gold-1);
}

.nav-item.active .nav-icon {
  color: var(--gold-1);
  transform: scale(1.1);
}

.nav-icon-wrapper {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(212, 175, 55, 0.1);
  margin-left: 12px;
  transition: var(--transition-smooth);
}

.nav-item:hover .nav-icon-wrapper {
  background: rgba(212, 175, 55, 0.2);
  transform: rotate(5deg);
}

.nav-icon {
  font-size: 1.2rem;
  color: var(--gold-1);
  transition: var(--transition-smooth);
}

.nav-text {
  flex: 1;
  font-weight: 500;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

.nav-badge {
  background: var(--danger);
  color: white;
  padding: 3px 8px;
  border-radius: 30px;
  font-size: 0.7rem;
  font-weight: 600;
  box-shadow: var(--danger-glow);
  animation: badgePulse 2s ease infinite;
}

/* الفوتر */
.sidebar-footer {
  padding: 25px 20px;
  border-top: 1px solid var(--border-light);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-card);
  border-radius: 20px;
  margin-bottom: 15px;
  position: relative;
  border: 1px solid var(--border-light);
  transition: var(--transition-smooth);
}

.user-card:hover {
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
  transform: translateY(-2px);
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  border: 2px solid var(--gold-1);
  box-shadow: var(--gold-glow);
  transition: var(--transition-smooth);
}

.user-card:hover .user-avatar {
  transform: rotate(5deg) scale(1.05);
}

.user-info {
  flex: 1;
}

.user-name {
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 3px;
}

.user-role {
  color: var(--gold-1);
  font-size: 0.8rem;
  opacity: 0.9;
}

.user-status {
  width: 10px;
  height: 10px;
  background: var(--success);
  border-radius: 50%;
  box-shadow: var(--success-glow);
  animation: statusPulse 2s ease infinite;
}

@keyframes statusPulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

.sidebar-toggle {
  width: 100%;
  padding: 15px;
  background: transparent;
  border: 1px solid var(--border-glow);
  color: var(--gold-1);
  border-radius: 16px;
  cursor: pointer;
  transition: var(--transition-smooth);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.sidebar-toggle::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: var(--gold-gradient);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  opacity: 0.1;
}

.sidebar-toggle:hover::before {
  width: 300px;
  height: 300px;
}

.sidebar-toggle:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold-strong);
}

/* ===== المحتوى الرئيسي ===== */
.dashboard-main {
  flex: 1;
  margin-right: 300px;
  transition: margin-right 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  background: var(--bg-primary);
  position: relative;
}

.collapsed + .dashboard-main {
  margin-right: 90px;
}

/* الهيدر المتطور */
.dashboard-header {
  background: var(--bg-header);
  padding: 15px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-light);
  position: sticky;
  top: 0;
  z-index: 90;
  backdrop-filter: blur(20px);
  transition: var(--transition-smooth);
}

.header-scrolled {
  box-shadow: var(--shadow-lg);
  border-bottom-color: var(--gold-1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 25px;
}

.mobile-menu-btn {
  display: none;
  width: 45px;
  height: 45px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  color: var(--gold-1);
  font-size: 1.3rem;
  cursor: pointer;
  transition: var(--transition-smooth);
  position: relative;
  overflow: hidden;
}

.mobile-menu-btn:hover {
  background: var(--gold-1);
  color: var(--bg-deep);
  transform: rotate(90deg);
}

.page-title h1 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 5px;
  font-weight: 700;
  letter-spacing: 0.5px;
  background: linear-gradient(135deg, #fff 0%, var(--gold-1) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-dim);
  font-size: 0.9rem;
}

.breadcrumbs a {
  color: var(--gold-1);
  text-decoration: none;
  transition: var(--transition-soft);
  position: relative;
}

.breadcrumbs a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--gold-gradient);
  transition: width 0.3s;
}

.breadcrumbs a:hover::after {
  width: 100%;
}

.breadcrumb-icon {
  font-size: 0.7rem;
  opacity: 0.5;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 25px;
}

.header-search {
  position: relative;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim);
  transition: var(--transition-soft);
  z-index: 1;
}

.header-search input {
  width: 320px;
  padding: 14px 45px 14px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 30px;
  color: white;
  font-size: 0.95rem;
  transition: var(--transition-smooth);
}

.header-search input:hover {
  border-color: var(--gold-1);
}

.header-search input:focus,
.header-search input.focused {
  outline: none;
  border-color: var(--gold-1);
  box-shadow: var(--shadow-gold);
  width: 380px;
}

.header-search input.focused + .search-icon {
  color: var(--gold-1);
  transform: translateY(-50%) scale(1.1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.action-btn {
  position: relative;
  width: 48px;
  height: 48px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: var(--gold-1);
  font-size: 1.2rem;
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, var(--gold-glow), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.action-btn:hover .btn-glow {
  opacity: 1;
}

.action-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  border-color: transparent;
  transform: translateY(-3px) scale(1.05);
  box-shadow: var(--shadow-gold-strong);
}

.action-btn .badge {
  position: absolute;
  top: -5px;
  left: -5px;
  background: var(--danger);
  color: white;
  font-size: 0.65rem;
  padding: 3px 7px;
  border-radius: 30px;
  min-width: 20px;
  font-weight: 600;
  box-shadow: var(--danger-glow);
  animation: badgePulse 2s ease infinite;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 20px;
  transition: var(--transition-smooth);
}

.user-menu:hover {
  background: var(--bg-card);
}

.user-menu .user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  border: 2px solid transparent;
  transition: var(--transition-smooth);
}

.user-menu:hover .user-avatar {
  border-color: var(--gold-1);
  transform: rotate(5deg) scale(1.05);
}

/* القائمة المنسدلة */
.user-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 280px;
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 24px;
  margin-top: 15px;
  box-shadow: var(--shadow-xl), var(--shadow-gold);
  z-index: 100;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.slide-down-enter,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.dropdown-header {
  padding: 20px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 15px;
}

.dropdown-header img {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  border: 2px solid var(--gold-1);
  box-shadow: var(--gold-glow);
}

.dropdown-user-name {
  color: white;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 3px;
}

.dropdown-user-email {
  color: var(--text-dim);
  font-size: 0.8rem;
}

.dropdown-menu {
  padding: 10px;
}

.dropdown-menu a,
.dropdown-menu button {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 15px;
  color: var(--text-secondary);
  text-decoration: none;
  width: 100%;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 16px;
  transition: var(--transition-smooth);
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.dropdown-menu a::before,
.dropdown-menu button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: var(--gold-gradient);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  opacity: 0.1;
}

.dropdown-menu a:hover::before,
.dropdown-menu button:hover::before {
  width: 300px;
  height: 300px;
}

.dropdown-menu a:hover,
.dropdown-menu button:hover {
  background: var(--bg-primary);
  color: var(--gold-1);
  transform: translateX(-5px);
}

.dropdown-divider {
  height: 1px;
  background: var(--border-light);
  margin: 10px 0;
}

/* محتوى الصفحة */
.dashboard-content {
  padding: 30px;
  flex: 1;
  animation: contentFadeIn 0.6s ease;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* تأثيرات الانتقال */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}

.page-enter {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.slide-right-enter,
.slide-right-leave-to {
  transform: translateX(-100%);
}

/* استجابة للشاشات الصغيرة */
@media (max-width: 1200px) {
  .header-search input {
    width: 250px;
  }

  .header-search input:focus {
    width: 300px;
  }
}

@media (max-width: 992px) {
  .dashboard-sidebar {
    display: none;
  }

  .dashboard-main {
    margin-right: 0 !important;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .header-search {
    display: none;
  }

  .dashboard-header {
    padding: 15px 20px;
  }

  .page-title h1 {
    font-size: 1.4rem;
  }
}

@media (max-width: 768px) {
  .header-actions .messages-btn,
  .header-actions .notifications-btn,
  .header-actions .currency-selector-wrapper {
    display: none;
  }

  .dashboard-content {
    padding: 20px 15px;
  }

  .page-title {
    display: none;
  }
}

/* Mobile Sidebar Styles */
.mobile-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  background: var(--bg-sidebar);
  z-index: 1001;
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(15px);
  padding: 20px;
}

.mobile-sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-light);
}

.close-mobile-menu {
  background: none;
  border: none;
  color: var(--gold-1);
  font-size: 1.5rem;
  cursor: pointer;
}

.mobile-sidebar-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.btn-logout-mobile {
  width: 100%;
  margin-top: 15px;
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.2);
  border-radius: 12px;
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-logout-mobile:hover {
  background: #f44336;
  color: white;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  z-index: 1000;
}

/* Transitions fix */
.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
}

.slide-right-enter-to,
.slide-right-leave-from {
  transform: translateX(0);
}
</style>
