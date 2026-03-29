// src/router/routes/profile.js
export default [
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile/ProfileLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '/dashboard/profile',
        name: 'DashboardProfile',
        component: () => import('@/views/dashboard/Profile.vue'),
        meta: {
          requiresAuth: true,
          title: 'الملف الشخصي',
          icon: 'fa-solid fa-user-circle',
        },
      },
      {
        path: '',
        name: 'ProfileOverview',
        component: () => import('@/views/Profile/Overview.vue'),
        meta: { title: 'نظرة عامة' },
      },
      {
        path: 'orders',
        name: 'ProfileOrders',
        component: () => import('@/views/Profile/Orders.vue'),
        meta: { title: 'طلباتي' },
      },
      {
        path: 'wishlist',
        name: 'ProfileWishlist',
        component: () => import('@/views/Profile/Wishlist.vue'),
        meta: { title: 'المفضلة' },
      },
      {
        path: 'settings',
        name: 'ProfileSettings',
        component: () => import('@/views/Profile/Settings.vue'),
        meta: { title: 'الإعدادات' },
      },
    ],
  },
];
