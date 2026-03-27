<template>
  <div class="royal-dashboard-layout marble-bg min-h-screen">
    <!-- Particles Background -->
    <div class="particles">
      <div
        v-for="n in 30"
        :key="n"
        class="particle"
        :style="getParticleStyle(n)"
      ></div>
    </div>

    <!-- Header -->
    <header class="dashboard-header glass sticky top-0 z-40">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo & Title -->
          <div class="flex items-center space-x-4">
            <button
              @click="toggleSidebar"
              class="lg:hidden p-2 rounded-xl bg-charcoal/80 backdrop-blur-sm text-off-white hover:bg-charcoal/60 transition-colors"
            >
              <i class="fas fa-bars"></i>
            </button>
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-to-r from-royal-600 to-gold-500 rounded-xl flex items-center justify-center">
                <i class="fas fa-paint-roller text-white"></i>
              </div>
              <div>
                <h1 class="text-xl font-bold text-white">VinylArt</h1>
                <p class="text-royal-200 text-sm">Dashboard</p>
              </div>
            </div>
          </div>

          <!-- Search & Actions -->
          <div class="flex items-center space-x-4">
            <!-- Search -->
            <div class="hidden md:flex items-center bg-charcoal/80 backdrop-blur-sm rounded-xl px-4 py-2">
              <i class="fas fa-search text-off-white/60 mr-3"></i>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="بحث في لوحة التحكم..."
                class="bg-transparent text-white placeholder-white/60 border-0 outline-none w-64"
              />
            </div>

            <!-- Notifications -->
            <div class="relative">
              <button class="p-2 rounded-xl bg-charcoal/80 backdrop-blur-sm text-off-white hover:bg-charcoal/60 transition-colors">
                <i class="fas fa-bell"></i>
                <span class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </button>
            </div>

            <!-- User Menu -->
            <div class="flex items-center space-x-3">
              <Avatar
                :image="userAvatar"
                shape="circle"
                size="large"
                class="ring-2 ring-gold-500"
              />
              <div class="hidden lg:block">
                <p class="text-white font-medium">{{ userName }}</p>
                <p class="text-royal-200 text-sm">{{ userRole }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Layout -->
    <div class="flex">
      <!-- Sidebar -->
      <RoyalSidebar
        :visible="sidebarVisible"
        @hide="sidebarVisible = false"
      />

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <!-- Breadcrumb -->
        <nav class="mb-6">
          <ol class="flex items-center space-x-2 text-sm">
            <li>
              <router-link
                to="/dashboard"
                class="text-royal-600 hover:text-royal-700 transition-colors"
              >
                <i class="fas fa-home mr-1"></i>
                الرئيسية
              </router-link>
            </li>
            <li class="text-marble-400">/</li>
            <li class="text-marble-600 font-medium">{{ breadcrumbTitle }}</li>
          </ol>
        </nav>

        <!-- Page Content -->
        <div
          class="page-content"
          v-motion="{
            initial: { opacity: 0, y: 20 },
            enter: { 
              opacity: 1, 
              y: 0,
              transition: { duration: 500 }
            }
          }"
        >
          <router-view />
        </div>
      </main>
    </div>

    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="sidebarVisible"
      class="fixed inset-0 bg-black/50 z-30 lg:hidden"
      @click="sidebarVisible = false"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import RoyalSidebar from '@/components/ui/RoyalSidebar.vue';

const route = useRoute();
const authStore = useAuthStore();

const sidebarVisible = ref(false);
const searchQuery = ref('');

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

const userRole = computed(() => {
  const roles = { admin: 'مدير النظام', investor: 'ممول استراتيجي', customer: 'عميل مميز' };
  return roles[authStore.role] || 'زائر';
});

const userAvatar = computed(() => {
  return `https://ui-avatars.com/api/?name=${userName.value}&background=d4af37&color=fff&size=100`;
});

const breadcrumbTitle = computed(() => {
  return route.meta?.title || 'لوحة التحكم';
});

const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
};

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

onMounted(() => {
  // Close sidebar on route change (mobile)
  if (window.innerWidth < 1024) {
    sidebarVisible.value = false;
  }
});
</script>

<style scoped>
.royal-dashboard-layout {
  font-family: 'Inter', system-ui, sans-serif;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-20px) translateX(10px);
  }
  50% {
    transform: translateY(10px) translateX(-10px);
  }
  75% {
    transform: translateY(-10px) translateX(5px);
  }
}

.dashboard-header {
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.page-content {
  min-height: calc(100vh - 200px);
}

/* Search input styling */
input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
  }
  
  .search-input {
    display: none;
  }
}

/* Animation classes */
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Glass effect */
.glass {
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Marble background */
.marble-bg {
  background: linear-gradient(135deg, 
    #fafafa 0%, 
    #f4f4f5 25%, 
    #e4e4e7 50%, 
    #f4f4f5 75%, 
    #fafafa 100%);
  background-size: 400% 400%;
  animation: marble-shift 15s ease infinite;
}

@keyframes marble-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
