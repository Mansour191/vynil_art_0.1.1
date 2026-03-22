// src/router/routes/categories.js

// مسارات التصنيفات - منظمة في مصفوفة واحدة
const categories = [
  { path: 'furniture', name: 'Furniture', component: 'Furniture', title: 'الأثاث', icon: 'couch' },
  { path: 'doors', name: 'Doors', component: 'Doors', title: 'الأبواب', icon: 'door-open' },
  { path: 'walls', name: 'Walls', component: 'Walls', title: 'الجدران', icon: 'paint-roller' },
  { path: 'ceilings', name: 'Ceilings', component: 'Ceilings', title: 'الأسقف', icon: 'arrow-up' },
  { path: 'tiles', name: 'Tiles', component: 'Tiles', title: 'البلاط', icon: 'border-all' },
  { path: 'kitchens', name: 'Kitchens', component: 'Kitchens', title: 'المطابخ', icon: 'utensils' },
  { path: 'cars', name: 'Cars', component: 'Cars', title: 'السيارات', icon: 'car' },
];

// إنشاء المسارات ديناميكياً مع Lazy Loading
export default categories.map((cat) => ({
  path: `/${cat.path}`,
  name: cat.name,
  component: () => import(/* webpackChunkName: "categories" */ `@/views/categories/${cat.component}.vue`),
  meta: {
    title: cat.title,
    icon: cat.icon,
    category: cat.path,
  },
}));
