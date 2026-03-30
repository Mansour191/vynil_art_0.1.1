<template>
  <CategoryTemplate
    :icon="categoryData?.icon || 'fa-solid fa-couch'"
    titleKey="furnitureTitle"
    descriptionKey="furnitureDescription"
    labelKey="furnitureLabel"
    latestLabelKey="featuredFurniture"
    :subCategories="subCategories"
    badgeLabel="furnitureDesign"
  />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import CategoryTemplate from '@/components/CategoryTemplate.vue';
import CategoryService from '@/integration/services/CategoryService';

const categoryData = ref(null);
const subCategories = ref([]);

onMounted(async () => {
  try {
    // جلب بيانات الفئة من قاعدة البيانات
    const category = await CategoryService.getCategoryBySlug('furniture');
    categoryData.value = category;
    
    // جلب الفئات الفرعية
    const subCats = await CategoryService.getSubCategories('furniture');
    subCategories.value = subCats;
    
    console.log('✅ Furniture category loaded:', category);
    console.log('✅ Furniture subcategories loaded:', subCats);
  } catch (error) {
    console.error('❌ Error loading furniture category:', error);
  }
});
</script>
