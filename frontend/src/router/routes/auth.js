// src/router/routes/auth.js

export default [
  {
    path: '/auth',
    name: 'Auth',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/AuthAdvanced.vue'),
    meta: {
      title: 'تسجيل الدخول',
      guest: true,
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/Login.vue'),
    meta: {
      title: 'تسجيل الدخول',
      guest: true,
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/Register.vue'),
    meta: {
      title: 'إنشاء حساب جديد',
      guest: true,
    },
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/ForgotPassword.vue'),
    meta: {
      title: 'استعادة كلمة المرور',
      guest: true,
    },
  },
  {
    path: '/reset-password/:token',
    name: 'ResetPassword',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/ResetPassword.vue'),
    meta: {
      title: 'إعادة تعيين كلمة المرور',
      guest: true,
    },
  },
  {
    path: '/verify-email/:token',
    name: 'VerifyEmail',
    component: () => import(/* webpackChunkName: "auth" */ '@/views/auth/VerifyEmail.vue'),
    meta: {
      title: 'تفعيل البريد الإلكتروني',
      guest: true,
    },
  },
];
