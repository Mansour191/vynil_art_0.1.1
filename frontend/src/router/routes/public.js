// router/routes/public.js
// المسارات العامة (لا تحتاج تسجيل دخول)

export default [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Home.vue'),
    meta: { title: 'الرئيسية' },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/About.vue'),
    meta: { title: 'من نحن' },
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Contact.vue'),
    meta: { title: 'اتصل بنا' },
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Gallery.vue'),
    meta: { title: 'معرض الأعمال' },
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Blog.vue'),
    meta: { title: 'المدونة' },
  },
  {
    path: '/post/:id/:slug?',
    name: 'Post',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Post.vue'),
    meta: { title: 'تفاصيل المقال' },
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Privacy.vue'),
    meta: { title: 'سياسة الخصوصية' },
  },
  {
    path: '/terms',
    name: 'Terms',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Terms.vue'),
    meta: { title: 'الشروط والأحكام' },
  },
  {
    path: '/how-to-order',
    name: 'HowToOrder',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/HowToOrder.vue'),
    meta: { title: 'كيف أطلب' },
  },
  {
    path: '/shipping-policy',
    name: 'ShippingPolicy',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/ShippingPolicy.vue'),
    meta: { title: 'سياسة الشحن' },
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/FAQ.vue'),
    meta: { title: 'الأسئلة الشائعة' },
  },
  {
    path: '/user-guide',
    name: 'UserGuide',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/UserGuide.vue'),
    meta: { title: 'دليل المستخدم' },
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/Notifications.vue'),
    meta: { title: 'الإشعارات', requiresAuth: true },
  },
  {
    path: '/shop',
    name: 'Shop',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/products/Shop.vue'),
    meta: { title: 'المتجر' },
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/products/Shop.vue'),
    meta: { title: 'المنتجات' },
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/products/ProductDetail.vue'),
    meta: { title: 'تفاصيل المنتج', requiresAuth: false },
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/shop/Cart.vue'),
    meta: { title: 'سلة التسوق' },
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/shop/Checkout.vue'),
    meta: { title: 'إتمام الشراء' },
  },
  {
    path: '/order-success/:orderId',
    name: 'OrderSuccess',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/shop/OrderSuccess.vue'),
    meta: { title: 'نجاح الطلب' },
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/products/Search.vue'),
    meta: { title: 'البحث' },
  },
  {
    path: '/search/label/:label',
    name: 'Label',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/Home.vue'),
    meta: { title: 'التصنيفات' },
  },
  {
    path: '/wishlist',
    name: 'Wishlist',
    component: () => import(/* webpackChunkName: "shop" */ '@/views/products/Wishlist.vue'),
    meta: {
      title: 'المفضلة',
      requiresAuth: true,
    },
  },
  {
    path: '/getlocation',
    name: 'GetLocation',
    component: () => import(/* webpackChunkName: "test" */ '@/views/test/GetLocation.vue'),
    meta: { 
      title: 'اختبار تحديد الموقع',
      requiresAuth: false,
      isPublic: true
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/NotFound.vue'),
    meta: { title: 'الصفحة غير موجودة' },
  },
];
