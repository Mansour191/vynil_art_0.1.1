<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="rail"
    permanent
    @click="rail = false"
    class="sidebar-royal border-0"
    theme="dark"
    width="300"
  >
    <v-list-item class="pa-4 mb-2">
      <template v-slot:prepend>
        <v-avatar color="primary" rounded="lg" size="45" class="elevation-4">
          <v-icon icon="mdi-paint-roller" color="white"></v-icon>
        </v-avatar>
      </template>
      <v-list-item-title class="text-h6 font-weight-black gold-text">
        PACLOS
      </v-list-item-title>
      <v-list-item-subtitle class="text-caption opacity-60">
        لوحة التحكم الفاخرة
      </v-list-item-subtitle>
      
      <template v-slot:append>
        <v-btn
          variant="text"
          icon="mdi-chevron-right"
          @click.stop="rail = !rail"
        ></v-btn>
      </template>
    </v-list-item>

    <v-divider class="mx-4 opacity-10"></v-divider>

    <v-list nav density="comfortable" class="pa-4">
      <template v-for="(item, index) in menuItems" :key="index">
        
        <v-list-group v-if="item.items" :value="item.label">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              :prepend-icon="item.icon"
              :title="item.label"
              class="rounded-lg mb-1"
            ></v-list-item>
          </template>

          <v-list-item
            v-for="(sub, subIdx) in item.items"
            :key="subIdx"
            :title="sub.label"
            :prepend-icon="sub.icon"
            :to="sub.to"
            rounded="lg"
            class="mb-1 ps-8"
            active-color="primary"
          ></v-list-item>
        </v-list-group>

        <v-list-item
          v-else
          :prepend-icon="item.icon"
          :title="item.label"
          :to="item.to"
          rounded="lg"
          class="mb-1"
          active-color="primary"
        ></v-list-item>
      </template>
    </v-list>

    <template v-slot:append>
      <div class="pa-4">
        <v-card variant="tonal" color="rgba(212, 175, 55, 0.1)" class="rounded-xl pa-2 mb-4" v-if="!rail">
          <v-list-item
            :prepend-avatar="user?.avatar || '/default-avatar.png'"
            :title="user?.username || 'المدير'"
            subtitle="مسؤول النظام"
          >
          </v-list-item>
        </v-card>
        
        <v-btn
          block
          color="error"
          variant="flat"
          rounded="pill"
          prepend-icon="mdi-logout"
          @click="handleLogout"
          :icon="rail"
        >
          <span v-if="!rail">تسجيل الخروج</span>
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
// import { useAuthStore } from '@/stores/auth';

const router = useRouter();
// const authStore = useAuthStore();
const drawer = ref(true);
const rail = ref(false);

const user = ref({ username: 'Remadna', avatar: null }); // مثال

const menuItems = computed(() => {
  const common = [
    { label: 'الرئيسية', icon: 'mdi-view-dashboard-outline', to: '/admin' },
    { label: 'الطلبات', icon: 'mdi-cart-outline', to: '/admin/orders' },
    { label: 'الكتالوج (50 تصميم)', icon: 'mdi-format-list-bulleted', to: '/admin/catalog' },
  ];

  // إضافة ركن الممولين (Investors) كما في الكود الأصلي
  const investorItems = {
    label: 'ركن الممولين',
    icon: 'mdi-trending-up',
    items: [
      { label: 'لوحة الممول', icon: 'mdi-chart-arc', to: '/investor' },
      { label: 'التقارير المالية', icon: 'mdi-cash-register', to: '/investor/reports' },
      { label: 'تحليلات AI', icon: 'mdi-brain', to: '/investor/ai-insights' },
    ]
  };

  return [...common, investorItems];
});

const handleLogout = () => {
  console.log('Logging out...');
  router.push('/login');
};
</script>

<style scoped>
.sidebar-royal {
  background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%) !important;
}

.gold-text {
  color: #d4af37;
  letter-spacing: 1.5px;
}

:deep(.v-list-group__items .v-list-item) {
  padding-inline-start: 16px !important;
}

:deep(.v-list-item--active) {
  background: rgba(212, 175, 55, 0.1) !important;
  color: #d4af37 !important;
}

:deep(.v-navigation-drawer__content) {
  scrollbar-width: none; /* Firefox */
}
:deep(.v-navigation-drawer__content::-webkit-scrollbar) {
  display: none; /* Chrome/Safari */
}
</style>
