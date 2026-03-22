// src/router/routes/customer.js
// Customer-specific routes including profile
export default [
  {
    path: '/profile',
    name: 'CustomerProfile',
    component: () => import('@/views/customer/Profile.vue'),
    meta: {
      requiresAuth: true,
      title: 'الملف الشخصي',
      icon: 'fa-solid fa-user-circle',
    },
  },
  {
    path: '/profile/orders',
    name: 'CustomerOrders',
    component: () => import('@/views/customer/Orders.vue'),
    meta: {
      requiresAuth: true,
      title: 'طلباتي',
      icon: 'fa-solid fa-shopping-bag',
    },
  },
  {
    path: '/profile/wishlist',
    name: 'CustomerWishlist',
    component: () => import('@/views/customer/Wishlist.vue'),
    meta: {
      requiresAuth: true,
      title: 'المفضلة',
      icon: 'fa-solid fa-heart',
    },
  },
  {
    path: '/profile/settings',
    name: 'CustomerSettings',
    component: () => import('@/views/customer/Settings.vue'),
    meta: {
      requiresAuth: true,
      title: 'الإعدادات',
      icon: 'fa-solid fa-cog',
    },
  },
  {
    path: '/profile/addresses',
    name: 'CustomerAddresses',
    component: () => import('@/views/customer/Addresses.vue'),
    meta: {
      requiresAuth: true,
      title: 'العناوين',
      icon: 'fa-solid fa-map-marker-alt',
    },
  },
  {
    path: '/profile/payments',
    name: 'CustomerPayments',
    component: () => import('@/views/customer/Payments.vue'),
    meta: {
      requiresAuth: true,
      title: 'طرق الدفع',
      icon: 'fa-solid fa-credit-card',
    },
  },
  {
    path: '/profile/notifications',
    name: 'CustomerNotifications',
    component: () => import('@/views/customer/Notifications.vue'),
    meta: {
      requiresAuth: true,
      title: 'الإشعارات',
      icon: 'fa-solid fa-bell',
    },
  },
];
