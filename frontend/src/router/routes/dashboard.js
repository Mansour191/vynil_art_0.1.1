// src/router/routes/dashboard.js

// مسارات لوحة التحكم
export default [
  {
    path: '/dashboard',
    component: () =>
      import(
        /* webpackChunkName: "dashboard" */ '@/views/dashboard/DashboardLayout.vue'
      ),
    meta: {
      requiresAuth: true,
      role: 'admin',
      title: 'لوحة التحكم',
    },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import(/* webpackChunkName: "dashboard" */ '@/views/dashboard/DashboardHome.vue'),
        meta: {
          title: 'نظرة عامة',
          icon: 'fa-solid fa-chart-line',
        },
      },
      {
        path: 'products',
        name: 'DashboardProducts',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-products" */ '@/views/dashboard/products/ProductsManager.vue'
          ),
        meta: {
          title: 'المنتجات',
          icon: 'fa-solid fa-box',
        },
      },
      {
        path: 'orders',
        name: 'DashboardOrders',
        component: () =>
          import(/* webpackChunkName: "dashboard-orders" */ '@/views/dashboard/orders/OrdersManager.vue'),
        meta: {
          title: 'الطلبات',
          icon: 'fa-solid fa-shopping-cart',
        },
      },
      {
        path: 'users',
        name: 'DashboardUsers',
        component: () =>
          import(/* webpackChunkName: "dashboard-admin" */ '@/views/dashboard/users/UsersManager.vue'),
        meta: {
          title: 'المستخدمين',
          icon: 'fa-solid fa-users',
        },
      },
      {
        path: 'designs',
        name: 'DashboardDesigns',
        component: () =>
          import(/* webpackChunkName: "dashboard-products" */ '@/views/dashboard/designs/DesignsManager.vue'),
        meta: {
          title: 'التصاميم',
          icon: 'fa-solid fa-paint-brush',
        },
      },
      {
        path: 'settings',
        name: 'DashboardSettings',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-admin" */ '@/views/dashboard/settings/SettingsManager.vue'
          ),
        meta: {
          title: 'الإعدادات',
          icon: 'fa-solid fa-cog',
        },
      },
      {
        path: 'profile',
        name: 'DashboardProfile',
        component: () => import(/* webpackChunkName: "dashboard" */ '@/views/dashboard/users/Profile.vue'),
        meta: {
          title: 'الملف الشخصي',
          icon: 'fa-solid fa-user-circle',
        },
      },
      {
        path: 'integration',
        name: 'IntegrationDashboard',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-integration" */ '@/views/dashboard/integration/IntegrationDashboard.vue'
          ),
        meta: {
          title: 'لوحة التكامل',
          icon: 'fa-solid fa-plug',
        },
      },
      {
        path: 'integration/settings',
        name: 'ERPNextSettings',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-integration" */ '@/views/dashboard/integration/ERPNextSettings.vue'
          ),
        meta: {
          title: 'إعدادات ERPNext',
          icon: 'fa-solid fa-cog',
        },
      },
      {
        path: 'reports',
        name: 'UnifiedReports',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-analytics" */ '@/views/dashboard/reports/UnifiedReports.vue'
          ),
        meta: {
          title: 'التقارير الموحدة',
          icon: 'fa-solid fa-chart-pie',
        },
      },
      {
        path: 'analytics',
        name: 'AdvancedAnalytics',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-analytics" */ '@/views/dashboard/analytics/AdvancedAnalytics.vue'
          ),
        meta: {
          title: 'التحليلات المتقدمة',
          icon: 'fa-solid fa-chart-line',
        },
      },
      {
        path: 'alerts',
        name: 'AlertsCenter',
        component: () =>
          import(/* webpackChunkName: "dashboard" */ '@/views/dashboard/admin/AlertsCenter.vue'),
        meta: {
          title: 'مركز التنبيهات',
          icon: 'fa-solid fa-bell',
        },
      },
      {
        path: 'automation',
        name: 'AutomationRules',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-admin" */ '@/views/dashboard/admin/AutomationRules.vue'
          ),
        meta: {
          title: 'قواعد الأتمتة',
          icon: 'fa-solid fa-robot',
        },
      },
      {
        path: 'forecasting',
        name: 'forecasting',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-analytics" */ '@/views/dashboard/forecasting/ForecastDashboard.vue'
          ),
        meta: {
          title: 'توقعات المبيعات',
          icon: 'fa-solid fa-chart-line',
          requiresAuth: true,
          permission: 'view_forecast',
        },
      },
      {
        path: 'recommendations',
        name: 'recommendations',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-analytics" */ '@/views/dashboard/analytics/RecommendationsDashboard.vue'
          ),
        meta: {
          title: 'توصيات ذكية',
          icon: 'fa-solid fa-star',
          requiresAuth: true,
        },
      },
      {
        path: 'customerinsights',
        name: 'customerinsights',
        component: () =>
          import(
            /* webpackChunkName: "dashboard-analytics" */ '@/views/dashboard/analytics/CustomerInsights.vue'
          ),
        meta: {
          title: 'تحليل سلوك العملاء',
          icon: 'fa-solid fa-users',
          requiresAuth: true,
        },
      },
    ],
  },
  // مسارات الاختبار والتشخيص
  {
    path: '/test',
    component: () => import(/* webpackChunkName: "test" */ '@/views/dashboard/DashboardLayout.vue'),
    meta: { requiresAuth: true, isAdmin: true },
    children: [
      {
        path: 'erpnext',
        name: 'ERPNextTest',
        component: () => import(/* webpackChunkName: "test" */ '@/views/test/ERPNextTest.vue'),
        meta: { title: 'اختبار ERPNext' }
      },
      {
        path: 'sync-products',
        name: 'ProductSyncTest',
        component: () => import(/* webpackChunkName: "test" */ '@/views/test/ProductSyncTest.vue'),
        meta: { title: 'مزامنة المنتجات' }
      },
      {
        path: 'sync-orders',
        name: 'OrderSyncTest',
        component: () => import(/* webpackChunkName: "test" */ '@/views/test/OrderSyncTest.vue'),
        meta: { title: 'مزامنة الطلبات' }
      },
      {
        path: 'notifications',
        name: 'NotificationsTest',
        component: () => import(/* webpackChunkName: "test" */ '@/views/test/Notifications.vue'),
        meta: { title: 'اختبار الإشعارات' }
      }
    ]
  }
];
