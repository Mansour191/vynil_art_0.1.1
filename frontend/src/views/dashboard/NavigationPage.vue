// src/views/dashboard/NavigationPage.vue
<template>
  <div class="navigation-page">
    <div class="page-header">
      <h1 class="page-title">خريطة الموقع</h1>
      <p class="page-description">جميع الروابط والأقسام المتاحة في الموقع</p>
    </div>

    <div class="navigation-grid">
      <!-- الصفحات الرئيسية -->
      <div class="nav-section">
        <h2 class="section-title">
          <i class="fa-solid fa-home section-icon"></i>
          الصفحات الرئيسية
        </h2>
        <div class="nav-items">
          <router-link to="/" class="nav-item">
            <i class="fa-solid fa-home item-icon"></i>
            <div class="item-content">
              <span class="item-title">الرئيسية</span>
              <span class="item-description">الصفحة الرئيسية للموقع</span>
            </div>
          </router-link>
          <router-link to="/about" class="nav-item">
            <i class="fa-solid fa-info-circle item-icon"></i>
            <div class="item-content">
              <span class="item-title">من نحن</span>
              <span class="item-description">معلومات عن الشركة</span>
            </div>
          </router-link>
          <router-link to="/contact" class="nav-item">
            <i class="fa-solid fa-phone item-icon"></i>
            <div class="item-content">
              <span class="item-title">اتصل بنا</span>
              <span class="item-description">طرق التواصل معنا</span>
            </div>
          </router-link>
          <router-link to="/gallery" class="nav-item">
            <i class="fa-solid fa-images item-icon"></i>
            <div class="item-content">
              <span class="item-title">معرض الأعمال</span>
              <span class="item-description">صور ومشاريع سابقة</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- المنتجات والفئات -->
      <div class="nav-section">
        <h2 class="section-title">
          <i class="fa-solid fa-box section-icon"></i>
          المنتجات والفئات
        </h2>
        <div class="nav-items">
          <router-link to="/shop" class="nav-item">
            <i class="fa-solid fa-store item-icon"></i>
            <div class="item-content">
              <span class="item-title">المتجر</span>
              <span class="item-description">جميع المنتجات المتاحة</span>
            </div>
          </router-link>
          <router-link to="/furniture" class="nav-item">
            <i class="fa-solid fa-couch item-icon"></i>
            <div class="item-content">
              <span class="item-title">الأثاث</span>
              <span class="item-description">أثاث فاخر ومميز</span>
            </div>
          </router-link>
          <router-link to="/doors" class="nav-item">
            <i class="fa-solid fa-door-open item-icon"></i>
            <div class="item-content">
              <span class="item-title">الأبواب</span>
              <span class="item-description">مجموعة متنوعة من الأبواب</span>
            </div>
          </router-link>
          <router-link to="/walls" class="nav-item">
            <i class="fa-solid fa-paint-roller item-icon"></i>
            <div class="item-content">
              <span class="item-title">الجدران</span>
              <span class="item-description">ديكورات وتشطيبات الجدران</span>
            </div>
          </router-link>
          <router-link to="/ceilings" class="nav-item">
            <i class="fa-solid fa-arrow-up item-icon"></i>
            <div class="item-content">
              <span class="item-title">الأسقف</span>
              <span class="item-description">تصاميم أسقف مبتكرة</span>
            </div>
          </router-link>
          <router-link to="/tiles" class="nav-item">
            <i class="fa-solid fa-border-all item-icon"></i>
            <div class="item-content">
              <span class="item-title">البلاط</span>
              <span class="item-description">بلاط فاخر بأنواعه</span>
            </div>
          </router-link>
          <router-link to="/kitchens" class="nav-item">
            <i class="fa-solid fa-utensils item-icon"></i>
            <div class="item-content">
              <span class="item-title">المطابخ</span>
              <span class="item-description">تصاميم مطابخ عصرية</span>
            </div>
          </router-link>
          <router-link to="/cars" class="nav-item">
            <i class="fa-solid fa-car item-icon"></i>
            <div class="item-content">
              <span class="item-title">السيارات</span>
              <span class="item-description">تعديلات وتجميل السيارات</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- لوحات التحكم -->
      <div class="nav-section">
        <h2 class="section-title">
          <i class="fa-solid fa-dashboard section-icon"></i>
          لوحات التحكم
        </h2>
        <div class="nav-items">
          <router-link to="/dashboard" class="nav-item">
            <i class="fa-solid fa-tachometer-alt item-icon"></i>
            <div class="item-content">
              <span class="item-title">لوحة التحكم الرئيسية</span>
              <span class="item-description">إدارة الموقع والمنتجات</span>
            </div>
          </router-link>
          <router-link to="/dashboard/products" class="nav-item">
            <i class="fa-solid fa-box item-icon"></i>
            <div class="item-content">
              <span class="item-title">إدارة المنتجات</span>
              <span class="item-description">إضافة وتعديل المنتجات</span>
            </div>
          </router-link>
          <router-link to="/dashboard/analytics" class="nav-item">
            <i class="fa-solid fa-chart-line item-icon"></i>
            <div class="item-content">
              <span class="item-title">التحليلات</span>
              <span class="item-description">إحصائيات وتقارير الموقع</span>
            </div>
          </router-link>
          <router-link to="/dashboard/ai" class="nav-item">
            <i class="fa-solid fa-brain item-icon"></i>
            <div class="item-content">
              <span class="item-title">الذكاء الاصطناعي</span>
              <span class="item-description">أدوات وتحليلات ذكية</span>
            </div>
          </router-link>
          <router-link to="/investor" class="nav-item">
            <i class="fa-solid fa-chart-line item-icon"></i>
            <div class="item-content">
              <span class="item-title">منصة المستثمرين</span>
              <span class="item-description">تقارير واستثمارات</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- الخدمات الإضافية -->
      <div class="nav-section">
        <h2 class="section-title">
          <i class="fa-solid fa-cogs section-icon"></i>
          الخدمات الإضافية
        </h2>
        <div class="nav-items">
          <router-link to="/cart" class="nav-item">
            <i class="fa-solid fa-shopping-cart item-icon"></i>
            <div class="item-content">
              <span class="item-title">سلة التسوق</span>
              <span class="item-description">المنتجات المختارة</span>
            </div>
          </router-link>
          <router-link to="/wishlist" class="nav-item">
            <i class="fa-solid fa-heart item-icon"></i>
            <div class="item-content">
              <span class="item-title">قائمة الرغبات</span>
              <span class="item-description">المنتجات المفضلة</span>
            </div>
          </router-link>
          <router-link to="/search" class="nav-item">
            <i class="fa-solid fa-search item-icon"></i>
            <div class="item-content">
              <span class="item-title">البحث المتقدم</span>
              <span class="item-description">بحث في جميع المحتويات</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Page data
const searchQuery = ref('')

// Statistics (mock data for now)
const stats = ref({
  totalProducts: 156,
  totalCategories: 8,
  totalPages: 24,
  totalUsers: 1234
})
</script>

<style scoped>
.navigation-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background: var(--color-bg-primary);
  min-height: 100vh;
  color: var(--color-text-primary);
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-description {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  opacity: 0.8;
}

.navigation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.nav-section {
  background: var(--color-bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.nav-section:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-border);
}

.section-icon {
  color: var(--color-primary);
  font-size: 1.2rem;
}

.nav-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: 0.75rem;
  text-decoration: none;
  color: var(--color-text-primary);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--color-hover), transparent);
  transition: left 0.5s ease;
}

.nav-item:hover::before {
  left: 100%;
}

.nav-item:hover {
  transform: translateX(8px);
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.item-icon {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-hover);
  border-radius: 0.75rem;
  color: var(--color-primary);
  font-size: 1.2rem;
  flex-shrink: 0;
}

.item-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.item-description {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  opacity: 0.8;
}

/* Dark mode adjustments */
.my-app-dark .nav-section {
  background: var(--color-bg-surface);
  border-color: var(--color-border);
}

.my-app-dark .nav-item {
  background: var(--color-bg-surface);
  border-color: var(--color-border);
}

.my-app-dark .nav-item:hover {
  border-color: var(--color-primary);
}

/* Responsive design */
@media (max-width: 768px) {
  .navigation-page {
    padding: 1rem;
  }
  
  .navigation-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .nav-item {
    padding: 0.75rem;
  }
  
  .item-icon {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1rem;
  }
}
</style>
