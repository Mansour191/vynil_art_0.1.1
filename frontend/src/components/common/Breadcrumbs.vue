<template>
  <nav class="breadcrumbs-nav" aria-label="Breadcrumb">
    <ol class="breadcrumb">
      <li class="breadcrumb-item">
        <router-link to="/">
          <i class="fa-solid fa-home"></i>
          {{ $t('home') }}
        </router-link>
      </li>
      <li 
        v-for="(crumb, index) in breadcrumbs" 
        :key="index" 
        class="breadcrumb-item"
        :class="{ active: index === breadcrumbs.length - 1 }"
      >
        <router-link v-if="index < breadcrumbs.length - 1" :to="crumb.path">
          {{ crumb.label }}
        </router-link>
        <span v-else aria-current="page">{{ crumb.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';

const route = useRoute();
const { t } = useI18n();

const breadcrumbs = computed(() => {
  const pathArray = route.path.split('/').filter(p => p);
  const crumbs = [];
  let currentPath = '';

  pathArray.forEach((path, index) => {
    currentPath += `/${path}`;
    
    // محاولة الحصول على الترجمة للمسار
    // إذا كان المسار رقمي (ID منتج مثلاً) نحاول الحصول على اسم من الـ meta أو نتركه كما هو
    let label = t(path) || path;
    
    // حالات خاصة للترجمة إذا لم تكن موجودة في ملفات اللغة مباشرة
    if (route.meta && route.meta.title && index === pathArray.length - 1) {
      label = route.meta.title;
    }

    crumbs.push({
      label,
      path: currentPath
    });
  });

  return crumbs;
});
</script>

<style scoped>
.breadcrumbs-nav {
  padding: 15px 0;
  margin-bottom: 20px;
}

.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 10px;
  align-items: center;
  font-size: 0.9rem;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  color: var(--text-muted, #888);
}

.breadcrumb-item a {
  color: var(--text-muted, #888);
  text-decoration: none;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.breadcrumb-item a:hover {
  color: var(--gold-primary, #d4af37);
}

.breadcrumb-item + .breadcrumb-item::before {
  content: "\f105";
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  margin-right: 10px;
  font-size: 0.8rem;
  opacity: 0.5;
}

[dir="rtl"] .breadcrumb-item + .breadcrumb-item::before {
  content: "\f104";
  margin-right: 0;
  margin-left: 10px;
}

.breadcrumb-item.active {
  color: var(--gold-primary, #d4af37);
  font-weight: 600;
}

.breadcrumb-item i {
  font-size: 0.85rem;
}
</style>
