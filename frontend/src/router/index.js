// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import routes from './routes'; // استيراد المسارات من مجلد routes

console.log('📦 المسارات القادمة من routes:', routes);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, left: 0 };
    }
  },
});

console.log('🚀 الراوتر بعد الإنشاء:', router);

// حماية المسارات
import { useAuthStore } from '@/store/auth';

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiredRole = to.meta.role;
  const requiresAdmin = to.matched.some(record => record.meta.isAdmin) || requiredRole === 'admin';

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if (requiresAdmin && !authStore.isAdmin) {
    next('/');
  } else if (requiresAuth && requiredRole && authStore.role !== requiredRole && !authStore.isAdmin) {
    // توجيه المستخدم إذا لم يكن لديه الصلاحية المطلوبة (باستثناء المدير)
    if (authStore.role === 'investor') next('/investor');
    else next('/');
  } else {
    next();
  }
});

export default router;
