<template>
  <div class="dashboard-layout investor-theme">
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
            <i class="fa-solid fa-crown logo-icon"></i>
            <div class="logo-text-wrapper">
              <h2 class="logo-text">Premium<span>Hub</span></h2>
              <span class="logo-badge">PRO</span>
            </div>
          </div>
        </div>

        <nav class="sidebar-nav">
          <div class="nav-section">
            <p class="nav-section-title" v-if="!isSidebarCollapsed">التحليل الاستراتيجي</p>
            
            <router-link :to="{ name: 'InvestorHub' }" class="nav-item" exact-active-class="active">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-table-cells-large nav-icon"></i>
                <div class="icon-glow"></div>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">نظرة عامة</span>
            </router-link>

            <router-link :to="{ name: 'AIInsights' }" class="nav-item" active-class="active">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-brain nav-icon"></i>
                <div class="icon-glow"></div>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">ذكاء الأعمال</span>
            </router-link>

            <router-link :to="{ name: 'CreativeVoting' }" class="nav-item" active-class="active">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-fingerprint nav-icon"></i>
                <div class="icon-glow"></div>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">مختبر الابتكار</span>
            </router-link>

            <router-link :to="{ name: 'InvestorReports' }" class="nav-item" active-class="active">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-chart-pie nav-icon"></i>
                <div class="icon-glow"></div>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">التقارير الذكية</span>
            </router-link>
          </div>

          <div class="nav-section">
            <p class="nav-section-title" v-if="!isSidebarCollapsed">الوصول السريع</p>
            <router-link to="/" class="nav-item">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-arrow-up-right-from-square nav-icon"></i>
              </div>
              <span class="nav-text" v-if="!isSidebarCollapsed">المتجر الرئيسي</span>
            </router-link>
          </div>
        </nav>

        <div class="sidebar-footer">
          <div class="user-card" v-if="!isSidebarCollapsed">
            <img :src="userAvatar" alt="User" class="user-avatar" />
            <div class="user-info">
              <p class="user-name">{{ userName }}</p>
              <p class="user-role">ممول استراتيجي</p>
            </div>
            <div class="user-status"></div>
          </div>

          <div class="footer-actions" v-if="!isSidebarCollapsed">
            <button @click="logout" class="logout-btn-premium">
              <i class="fa-solid fa-right-from-bracket"></i>
              <span>تسجيل خروج</span>
            </button>
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
                <router-link to="/investor">ركن الممولين</router-link>
                <i class="fa-solid fa-chevron-left breadcrumb-icon"></i>
                <span>{{ breadcrumbTitle }}</span>
              </div>
            </div>
          </div>

          <div class="header-right">
            <div class="header-actions">
              <LanguageSwitcher />
              <button class="action-btn search-btn">
                <i class="fa-solid fa-magnifying-glass"></i>
              </button>

              <button class="action-btn notifications-btn">
                <div class="icon-with-badge">
                  <i class="fa-solid fa-bell"></i>
                  <span class="badge-dot"></span>
                </div>
                <span class="btn-glow"></span>
              </button>

              <div class="header-divider"></div>

              <div class="user-menu" @click="toggleUserMenu">
                <img :src="userAvatar" alt="User" class="user-avatar" />
                <i class="fa-solid fa-chevron-down"></i>

                <transition name="slide-down">
                  <div class="user-dropdown" v-if="showUserMenu" @click.stop>
                    <div class="dropdown-header">
                      <img :src="userAvatar" alt="User" />
                      <div>
                        <p class="dropdown-user-name">{{ userName }}</p>
                        <p class="dropdown-user-email">investor@vinylart.com</p>
                      </div>
                    </div>

                    <div class="dropdown-menu">
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
          <h2 class="logo-text">Premium<span>Hub</span></h2>
          <button class="close-mobile-menu" @click="toggleMobileMenu">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>

        <nav class="sidebar-nav">
          <div class="nav-section">
            <p class="nav-section-title">التحليل الاستراتيجي</p>
            
            <router-link :to="{ name: 'InvestorHub' }" class="nav-item" exact-active-class="active" @click="toggleMobileMenu">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-table-cells-large nav-icon"></i>
              </div>
              <span class="nav-text">نظرة عامة</span>
            </router-link>

            <router-link :to="{ name: 'AIInsights' }" class="nav-item" active-class="active" @click="toggleMobileMenu">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-brain nav-icon"></i>
              </div>
              <span class="nav-text">ذكاء الأعمال</span>
            </router-link>

            <router-link :to="{ name: 'CreativeVoting' }" class="nav-item" active-class="active" @click="toggleMobileMenu">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-fingerprint nav-icon"></i>
              </div>
              <span class="nav-text">مختبر الابتكار</span>
            </router-link>

            <router-link :to="{ name: 'InvestorReports' }" class="nav-item" active-class="active" @click="toggleMobileMenu">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-chart-pie nav-icon"></i>
              </div>
              <span class="nav-text">التقارير الذكية</span>
            </router-link>
          </div>

          <div class="nav-section">
            <p class="nav-section-title">الوصول السريع</p>
            <router-link to="/" class="nav-item" @click="toggleMobileMenu">
              <div class="nav-icon-wrapper">
                <i class="fa-solid fa-arrow-up-right-from-square nav-icon"></i>
              </div>
              <span class="nav-text">المتجر الرئيسي</span>
            </router-link>
          </div>
        </nav>

        <div class="mobile-sidebar-footer">
          <div class="user-card">
            <img :src="userAvatar" alt="User" class="user-avatar" />
            <div class="user-info">
              <p class="user-name">{{ userName }}</p>
              <p class="user-role">ممول استراتيجي</p>
            </div>
          </div>
          <button @click="logout" class="logout-btn-premium w-100 mt-3">
            <i class="fa-solid fa-right-from-bracket"></i>
            <span>تسجيل خروج</span>
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
import ErrorBoundary from '@/components/ErrorBoundary.vue';
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// State
const isSidebarCollapsed = ref(false);
const mobileMenuOpen = ref(false);
const showUserMenu = ref(false);
const isHeaderScrolled = ref(false);

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
    return 'ممول';
  }
});
const userAvatar = computed(() => `https://ui-avatars.com/api/?name=${userName.value}&background=d4af37&color=fff&size=100`);
const pageTitle = computed(() => route.meta?.title || 'منصة الممول');
const breadcrumbTitle = computed(() => route.meta?.title || '');

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
};

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const logout = () => {
  authStore.logout();
  router.push('/');
};

const handleScroll = () => {
  isHeaderScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
@import '@/assets/theme.css';

/* تخصيص الثيم الخاص بالممولين ليكون أكثر فخامة */
.investor-theme {
  --gold-glow: 0 0 20px rgba(212, 175, 55, 0.3);
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
  0% { transform: translateY(100vh) translateX(0) rotate(0deg); opacity: 0; }
  10% { opacity: 0.8; }
  90% { opacity: 0.6; }
  100% { transform: translateY(-100px) translateX(100px) rotate(360deg); opacity: 0; }
}

.dashboard-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

/* Sidebar */
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
}

.dashboard-sidebar.collapsed {
  width: 90px;
}

.sidebar-glow {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 0% 50%, var(--gold-glow), transparent 70%);
  pointer-events: none;
  opacity: 0.1;
}

.sidebar-header {
  padding: 30px 20px;
  border-bottom: 1px solid var(--border-light);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-icon {
  font-size: 2.2rem;
  color: var(--gold-1);
  filter: drop-shadow(var(--gold-glow));
}

.logo-text {
  font-size: 1.6rem;
  font-weight: 800;
  background: var(--gold-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-text span {
  -webkit-text-fill-color: var(--gold-1);
}

.logo-badge {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  font-size: 0.6rem;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 700;
  margin-right: 10px;
}

/* Nav Items */
.sidebar-nav {
  flex: 1;
  padding: 25px 15px;
}

.nav-section-title {
  color: var(--text-dim);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 15px;
  padding-right: 15px;
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
}

.nav-item:hover, .nav-item.active {
  background: var(--gold-gradient-soft);
  color: var(--gold-1);
  border: 1px solid var(--border-glow);
}

.nav-item:hover .nav-icon, .nav-item.active .nav-icon {
  transform: scale(1.2);
  color: #fff;
}

.nav-icon-wrapper {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(212, 175, 55, 0.1);
  margin-left: 12px;
  position: relative;
  transition: all 0.3s ease;
}

.icon-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(212, 175, 55, 0.5), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.nav-item:hover .icon-glow, .nav-item.active .icon-glow {
  opacity: 1;
}

.nav-icon {
  font-size: 1.2rem;
  color: var(--gold-1);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.nav-text {
  flex: 1;
  font-weight: 500;
}

/* Header Styles */
.header-divider {
  width: 1px;
  height: 30px;
  background: var(--border-light);
  margin: 0 10px;
}

.icon-with-badge {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 10px;
  height: 10px;
  background: #e74c3c;
  border: 2px solid var(--bg-header);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(231, 76, 60, 0.5);
}

.action-btn i {
  transition: all 0.3s ease;
}

.action-btn:hover i {
  transform: scale(1.1);
}

/* Main */
.dashboard-main {
  flex: 1;
  margin-right: 300px;
  transition: margin-right 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
  background: var(--bg-primary);
}

.collapsed + .dashboard-main {
  margin-right: 90px;
}

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
}

.page-title h1 {
  font-size: 1.8rem;
  color: white;
  margin-bottom: 5px;
  background: var(--gold-gradient);
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
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.action-btn {
  width: 48px;
  height: 48px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  color: var(--gold-1);
  cursor: pointer;
  transition: var(--transition-smooth);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.action-btn:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
  transform: translateY(-3px);
  box-shadow: var(--shadow-gold-strong);
}

.action-btn .badge {
  position: absolute;
  top: -5px;
  left: -5px;
  background: var(--gold-1);
  color: var(--bg-deep);
  font-size: 0.65rem;
  padding: 3px 7px;
  border-radius: 30px;
  font-weight: bold;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.user-menu .user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  border: 2px solid var(--gold-1);
}

.dashboard-content {
  padding: 30px;
  flex: 1;
}

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
  margin-bottom: 10px;
  border: 1px solid var(--border-light);
}

.logout-btn-premium {
  width: 100%;
  padding: 12px;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
  transition: var(--transition-smooth);
}

.logout-btn-premium:hover {
  background: #e74c3c;
  color: white;
  box-shadow: 0 0 20px rgba(231, 76, 60, 0.4);
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
}

.sidebar-toggle:hover {
  background: var(--gold-gradient);
  color: var(--bg-deep);
}

/* User Dropdown */
.user-dropdown {
  position: absolute;
  top: 100%;
  left: 30px;
  width: 250px;
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: 20px;
  box-shadow: var(--shadow-xl);
  z-index: 100;
  padding: 10px;
}

.dropdown-header {
  padding: 15px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 10px;
}

.dropdown-header img {
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.dropdown-menu button {
  width: 100%;
  padding: 12px;
  background: transparent;
  border: none;
  color: white;
  text-align: right;
  cursor: pointer;
  border-radius: 10px;
  transition: var(--transition-smooth);
}

.dropdown-menu button:hover {
  background: var(--gold-gradient-soft);
  color: var(--gold-1);
}

/* Animations */
.page-enter-active, .page-leave-active { transition: opacity 0.4s, transform 0.4s; }
.page-enter-from { opacity: 0; transform: translateY(20px); }
.page-leave-to { opacity: 0; transform: translateY(-20px); }

/* Responsive Styles */
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

  .dashboard-header {
    padding: 15px 20px;
  }

  .page-title h1 {
    font-size: 1.4rem;
  }
}

@media (max-width: 768px) {
  .header-actions .search-btn,
  .header-actions .notifications-btn {
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

.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
}

.slide-right-enter-to,
.slide-right-leave-from {
  transform: translateX(0);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
